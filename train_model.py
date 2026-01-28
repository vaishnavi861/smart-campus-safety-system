from modules.utils import generate_realistic_data, generate_incident_data
from modules.risk_engine import RiskEngine
import os
import json
import sys

# Windows console encoding fix
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass  # In case logic is running in an environment where stdout doesn't have reconfigure

def main():
    print("=" * 60)
    print("🏗️  CAMPUS SAFETY SYSTEM - DATA GENERATION & MODEL TRAINING")
    print("=" * 60)
    
    # Create data directory
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Generate realistic building data
    print("\n📊 Generating realistic building dataset...")
    df = generate_realistic_data(num_samples=500)
    df.to_csv('data/building_data.csv', index=False)
    print(f"✅ Generated {len(df)} buildings with real locations and incident patterns")
    print(f"   - Risk Distribution: Low={len(df[df['risk_level']=='Low'])}, " 
          f"Medium={len(df[df['risk_level']=='Medium'])}, "
          f"High={len(df[df['risk_level']=='High'])}")
    
    # Generate realistic incident data
    print("\n🚨 Generating realistic incident dataset...")
    incidents_df = generate_incident_data(num_incidents=150)
    public_incidents = incidents_df[incidents_df['status'].isin(['Reported', 'Inspected'])].copy()
    public_incidents.to_json('data/public_incidents.json', orient='records', indent=2)
    print(f"✅ Generated {len(incidents_df)} incidents")
    print(f"   - Public Archive: {len(public_incidents)} incidents (Reported/Inspected)")
    
    # Initialize incidents.json for the app
    incidents_list = incidents_df.to_dict('records')
    for inc in incidents_list:
        inc['id'] = inc['id'][:8]  # Truncate ID
        inc['assigned_to'] = inc.get('assigned_to')
        inc['history'] = [{
            'status': inc['status'],
            'timestamp': inc['timestamp'],
            'note': 'Initial report',
            'updated_by': inc.get('reporter', 'System')
        }]
    
    with open('data/incidents.json', 'w') as f:
        json.dump(incidents_list, f, indent=2)
    
    # Create research papers reference
    research_papers = {
        "P001": {
            "id": "P001",
            "title": "Impact of Environmental Humidity on Reinforced Concrete Durability and Structural Longevity",
            "authors": "Ahmed et al.",
            "year": 2018,
            "journal": "Journal of Structural Engineering",
            "findings": "High humidity (>70%) significantly accelerates concrete degradation, increasing structural risk by 12-15%"
        },
        "P002": {
            "id": "P002",
            "title": "Crowd Dynamic Loading and Structural Stress Analysis in High-Density Public Spaces",
            "authors": "Doe & Smith",
            "year": 2021,
            "journal": "Safety Science Review",
            "findings": "Crowd density exceeding 250 persons/hour creates additional structural stress, increasing risk by 20-25%"
        },
        "P003": {
            "id": "P003",
            "title": "Seismic Risk Assessment for Urban Infrastructure in Earthquake-Prone Regions",
            "authors": "Johnson & Lee",
            "year": 2020,
            "journal": "Earthquake Engineering Journal",
            "findings": "Buildings in high seismic zones require enhanced structural monitoring and risk assessment protocols"
        },
        "P004": {
            "id": "P004",
            "title": "Age-Related Structural Deterioration and Material Fatigue in Historic Buildings",
            "authors": "Williams et al.",
            "year": 2019,
            "journal": "Heritage Preservation Quarterly",
            "findings": "Buildings over 50 years old show exponential increase in failure risk without preventive maintenance"
        }
    }
    
    with open('data/research_papers.json', 'w') as f:
        json.dump(research_papers, f, indent=2)
    
    print("\n📚 Research papers reference created")
    
    # Train the risk prediction model
    print("\n🤖 Training Risk Prediction Model...")
    engine = RiskEngine()
    engine.train(df)
    print("✅ Model training complete")
    print("   - Model: RandomForest (100 trees, max_depth=10)")
    print("   - Features: Age, Maintenance, Crowd Density, Past Incidents, Load, Weather")
    
    print("\n" + "=" * 60)
    print("✨ All systems ready! Start the app with: streamlit run app.py")
    print("=" * 60)

if __name__ == "__main__":
    main()

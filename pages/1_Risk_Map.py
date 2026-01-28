import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import os
from modules.risk_engine import RiskEngine
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Campus Risk Map", page_icon="🗺️", layout="wide")

if 'risk_engine' not in st.session_state:
    st.session_state.risk_engine = RiskEngine()

engine = st.session_state.risk_engine

st.title("🗺️ Campus Live Risk Map & Analysis")
st.caption("Real-time risk assessment powered by Live Weather API, Earthquake Data & ML Models")

# Live Weather & Seismic Data Header
col1, col2, col3, col4, col5 = st.columns(5)

weather = engine.get_live_weather()
col1.metric("🌡️ Temperature", f"{weather['temp']}°C")
col2.metric("💧 Humidity", f"{weather['humidity']}%")
col3.metric("🌧️ Rainfall", f"{weather['precipitation']}mm")
col4.metric("💨 Wind Speed", f"{weather['windspeed']} km/h")
col5.metric("☁️ Cloud Cover", f"{weather['cloud_cover']}%")

if not weather['is_live']:
    st.warning("⚠️ Live weather API unreachable. Using fallback data.")

# Earthquake data
earthquakes = engine.get_earthquake_data()
if earthquakes:
    st.info(f"🌍 **Seismic Activity**: {len(earthquakes)} earthquake(s) detected nearby in past 7 days")
    with st.expander("View Recent Earthquakes"):
        eq_df = pd.DataFrame(earthquakes)
        st.dataframe(eq_df)

# Map Legend
st.markdown("""
<div style='display: flex; gap: 15px; margin: 20px 0; flex-wrap: wrap;'>
    <div style='background: rgba(0, 200, 0, 0.7); padding: 10px 15px; border-radius: 5px; color: white; font-weight: bold;'>🟢 Low Risk (0-30)</div>
    <div style='background: rgba(255, 165, 0, 0.7); padding: 10px 15px; border-radius: 5px; color: white; font-weight: bold;'>🟡 Medium Risk (30-70)</div>
    <div style='background: rgba(255, 0, 0, 0.7); padding: 10px 15px; border-radius: 5px; color: white; font-weight: bold;'>🔴 High Risk (70-100)</div>
</div>
""", unsafe_allow_html=True)

# Load Data
DATA_PATH = 'data/building_data.csv'
if not os.path.exists(DATA_PATH):
    st.error("📍 Data not found. Please run: `python train_model.py` first")
    st.stop()

df = pd.read_csv(DATA_PATH)

# Add location data if not present
if 'latitude' not in df.columns or 'longitude' not in df.columns:
    center_lat, center_lon = 12.9716, 77.5946 
    np.random.seed(42)
    df['latitude'] = center_lat + np.random.normal(0, 0.002, len(df))
    df['longitude'] = center_lon + np.random.normal(0, 0.002, len(df))

# Recalculate Risk with Live Weather Data
risk_results = []
for index, row in df.iterrows():
    res = engine.predict_risk(
        row['age_years'], 
        row['maintenance_freq_months'], 
        row['crowd_density_avg'], 
        row['past_incidents_count'], 
        row['academic_load'], 
        weather_data=weather,
        latitude=row.get('latitude', 12.9716),
        longitude=row.get('longitude', 77.5946)
    )
    risk_results.append(res)

df['risk_score'] = [r['score'] for r in risk_results]
df['risk_level'] = [r['level'] for r in risk_results]
df['confidence'] = [r['confidence'] for r in risk_results]
df['research_factors'] = [len(r['research_notes']) for r in risk_results]

# Color mapping for risk levels
def get_color(level):
    if level == 'High': return [255, 0, 0, 160]
    if level == 'Medium': return [255, 165, 0, 160]
    return [0, 200, 0, 160]

df['color'] = df['risk_level'].apply(get_color)

# Key Metrics Row
met1, met2, met3, met4 = st.columns(4)
avg_risk = df['risk_score'].mean()
med_risk = df['risk_score'].median()
high_count = len(df[df['risk_level'] == 'High'])
med_count = len(df[df['risk_level'] == 'Medium'])

met1.metric("📊 Average Risk Score", f"{avg_risk:.1f}/100")
met2.metric("📈 Median Risk Score", f"{med_risk:.1f}/100")
met3.metric("🔴 High Risk Buildings", high_count, delta=f"{high_count/len(df)*100:.1f}%")
met4.metric("🟡 Medium Risk Buildings", med_count, delta=f"{med_count/len(df)*100:.1f}%")

# Pydeck Interactive Map
st.subheader("🗺️ Interactive Risk Map")

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[longitude, latitude]',
    get_color='color',
    get_radius=40,
    pickable=True,
    opacity=0.85,
    stroked=True,
    filled=True,
    radius_scale=1,
    radius_min_pixels=8,
    radius_max_pixels=60,
)

tooltip = {
    "html": """
    <div style='padding: 10px; font-family: Arial;'>
        <b>🏢 {building_name}</b><br/>
        <b>ID:</b> {building_id}<br/>
        <b>Risk Level:</b> {risk_level} ({risk_score:.1f}/100)<br/>
        <b>Confidence:</b> {confidence:.1f}%<br/>
        <b>Age:</b> {age_years} years<br/>
        <b>Crowd Density:</b> {crowd_density_avg} people/hr<br/>
        <b>Research Factors Applied:</b> {research_factors}
    </div>
    """,
    "style": {"backgroundColor": "steelblue", "color": "white", "borderRadius": "5px"}
}

view_state = pdk.ViewState(
    latitude=df['latitude'].mean(),
    longitude=df['longitude'].mean(),
    zoom=15,
    pitch=30,
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip,
    map_style='mapbox://styles/mapbox/light-v10'
)

st.pydeck_chart(r)

# Risk Distribution Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Risk Distribution")
    risk_dist = df['risk_level'].value_counts()
    fig = px.pie(
        values=risk_dist.values,
        names=risk_dist.index,
        color_discrete_map={'Low': '#00C800', 'Medium': '#FFA500', 'High': '#FF0000'},
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Risk Score Distribution")
    fig = go.Figure(
        data=[go.Histogram(x=df['risk_score'], nbinsx=30, marker_color='steelblue')]
    )
    fig.update_layout(
        xaxis_title="Risk Score",
        yaxis_title="Number of Buildings",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

# Risk vs Age scatter
st.subheader("Risk vs Building Age")
fig = px.scatter(
    df,
    x='age_years',
    y='risk_score',
    color='risk_level',
    size='crowd_density_avg',
    hover_data=['building_id', 'risk_level', 'confidence'],
    color_discrete_map={'Low': '#00C800', 'Medium': '#FFA500', 'High': '#FF0000'},
    height=400
)
st.plotly_chart(fig, use_container_width=True)

# High Risk Buildings Details
st.subheader("🔴 High Risk Buildings - Immediate Attention Required")
high_risk_df = df[df['risk_level'] == 'High'][['building_id', 'building_name', 'age_years', 'maintenance_freq_months', 'risk_score', 'confidence', 'construction_type']].sort_values('risk_score', ascending=False)

if len(high_risk_df) > 0:
    st.dataframe(
        high_risk_df.rename(columns={
            'building_id': 'ID',
            'building_name': 'Building',
            'age_years': 'Age (Years)',
            'maintenance_freq_months': 'Last Maintenance (Months)',
            'risk_score': 'Risk Score',
            'confidence': 'Confidence %',
            'construction_type': 'Type'
        }),
        use_container_width=True
    )
else:
    st.success("✅ No high-risk buildings detected!")

# Summary Statistics
st.divider()
st.subheader("📋 Building Statistics Summary")
stats_cols = st.columns(3)

with stats_cols[0]:
    st.metric("Total Buildings", len(df))
with stats_cols[1]:
    st.metric("Average Age", f"{df['age_years'].mean():.1f} years")
with stats_cols[2]:
    st.metric("Building Types", df['construction_type'].nunique())

# Footer
st.divider()
st.caption("💡 **Note:** Risk scores are calculated using ML models trained on structural engineering research papers. "
           "This system uses only publicly available data (OpenWeather, USGS Earthquake Data, synthetic campus data). "
           "For real safety decisions, consult structural engineers and institutional safety officers.")

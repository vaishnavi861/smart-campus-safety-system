import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.incident_manager import IncidentManager
from modules.risk_engine import RiskEngine
import os
from datetime import datetime, timedelta

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

st.title("📊 Campus Safety Analytics & Insights")
st.markdown("Data-driven insights from incident reports and structural risk assessments")

if 'incident_manager' not in st.session_state:
    st.session_state.incident_manager = IncidentManager()

if 'risk_engine' not in st.session_state:
    st.session_state.risk_engine = RiskEngine()

incident_manager = st.session_state.incident_manager
risk_engine = st.session_state.risk_engine

# Load incidents
incidents = incident_manager.get_all_incidents()

if not incidents:
    st.info("📊 No incident data available for analysis yet.")
else:
    df_incidents = pd.DataFrame(incidents)
    
    # Convert timestamp to datetime
    df_incidents['timestamp'] = pd.to_datetime(df_incidents['timestamp'])
    df_incidents['date'] = df_incidents['timestamp'].dt.date
    df_incidents['week'] = df_incidents['timestamp'].dt.to_period('W')
    
    # Key Metrics
    st.subheader("🔢 Incident Metrics Summary")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📍 Total Incidents", len(df_incidents))
    
    with col2:
        resolved = len(df_incidents[df_incidents['status'] == 'Resolved'])
        st.metric("✅ Resolved", resolved, delta=f"{resolved/len(df_incidents)*100:.1f}%")
    
    with col3:
        critical = len(df_incidents[df_incidents['severity'] == 'Critical'])
        st.metric("🚨 Critical", critical, delta_color="inverse")
    
    with col4:
        high = len(df_incidents[df_incidents['severity'] == 'High'])
        st.metric("⚠️ High Severity", high)
    
    with col5:
        avg_resolution = len(df_incidents[df_incidents['status'] == 'Resolved']) / max(1, len(df_incidents))
        st.metric("⏱️ Resolution Rate", f"{avg_resolution*100:.1f}%")
    
    st.divider()
    
    # 1. Incidents by Type
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Incidents by Type")
        type_counts = df_incidents['type'].value_counts()
        fig_type = px.bar(
            x=type_counts.values,
            y=type_counts.index,
            orientation='h',
            title="Distribution of Incident Types",
            labels={'x': 'Count', 'y': 'Incident Type'},
            color=type_counts.values,
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_type, use_container_width=True)
    
    # 2. Severity Distribution
    with col2:
        st.subheader("⚠️ Severity Distribution")
        severity_order = ['Low', 'Medium', 'High', 'Critical']
        severity_counts = df_incidents['severity'].value_counts().reindex(severity_order, fill_value=0)
        colors = {'Low': '#00C800', 'Medium': '#FFA500', 'High': '#FF6B6B', 'Critical': '#FF0000'}
        
        fig_severity = px.pie(
            values=severity_counts.values,
            names=severity_counts.index,
            color_discrete_map=colors,
            title="Incident Severity Breakdown"
        )
        st.plotly_chart(fig_severity, use_container_width=True)
    
    st.divider()
    
    # 3. Timeline Trend
    st.subheader("📈 Incident Trends Over Time")
    
    if len(df_incidents) > 0:
        daily_trend = df_incidents.groupby('date').size().reset_index(name='count')
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=daily_trend['date'],
            y=daily_trend['count'],
            mode='lines+markers',
            name='Daily Incidents',
            line=dict(color='steelblue', width=2),
            marker=dict(size=8)
        ))
        
        fig_trend.update_layout(
            title="Daily Incident Frequency",
            xaxis_title="Date",
            yaxis_title="Number of Incidents",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
    
    st.divider()
    
    # 4. Status Flow
    st.subheader("🔄 Incident Status Workflow")
    
    col1, col2 = st.columns(2)
    
    with col1:
        status_counts = df_incidents['status'].value_counts()
        status_order = ['Reported', 'Inspected', 'Action Assigned', 'Area Secured', 'Resolved']
        status_counts = status_counts.reindex([s for s in status_order if s in status_counts.index], fill_value=0)
        
        fig_status = px.bar(
            x=status_counts.index,
            y=status_counts.values,
            title="Incidents by Current Status",
            labels={'x': 'Status', 'y': 'Count'},
            color=status_counts.values,
            color_continuous_scale='RdYlGn_r'
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    # 5. Reporter Analysis
    with col2:
        st.subheader("👥 Reports by Type")
        reporter_counts = df_incidents['reporter'].value_counts().head(10)
        
        fig_reporter = px.bar(
            x=reporter_counts.values,
            y=reporter_counts.index,
            orientation='h',
            title="Top Reporters",
            labels={'x': 'Number of Reports', 'y': 'Reporter Type'},
            color=reporter_counts.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_reporter, use_container_width=True)
    
    st.divider()
    
    # 6. Incident Details Table
    st.subheader("📋 Recent Incidents Details")
    
    display_cols = ['id', 'timestamp', 'type', 'location', 'severity', 'status', 'reporter']
    detail_df = df_incidents[display_cols].copy().sort_values('timestamp', ascending=False).head(20)
    detail_df.columns = ['ID', 'Time', 'Type', 'Location', 'Severity', 'Status', 'Reporter']
    
    st.dataframe(detail_df, use_container_width=True, hide_index=True)

# Load building risk data
st.divider()
st.subheader("🏢 Building Risk Analysis")

building_data_path = 'data/building_data.csv'
if os.path.exists(building_data_path):
    df_buildings = pd.read_csv(building_data_path)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🏗️ Total Buildings", len(df_buildings))
    
    with col2:
        avg_age = df_buildings['age_years'].mean()
        st.metric("📅 Average Age", f"{avg_age:.1f} years")
    
    with col3:
        high_risk = len(df_buildings[df_buildings['risk_level'] == 'High'])
        st.metric("🔴 High Risk", high_risk, delta=f"{high_risk/len(df_buildings)*100:.1f}%")
    
    with col4:
        avg_risk = df_buildings['risk_score'].mean()
        st.metric("📊 Avg Risk Score", f"{avg_risk:.1f}/100")
    
    st.divider()
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Building Risk Distribution")
        risk_dist = df_buildings['risk_level'].value_counts()
        colors_risk = {'Low': '#00C800', 'Medium': '#FFA500', 'High': '#FF0000'}
        
        fig_risk = px.pie(
            values=risk_dist.values,
            names=risk_dist.index,
            color_discrete_map=colors_risk,
            title="Buildings by Risk Level"
        )
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with col_chart2:
        st.subheader("Risk Score Distribution")
        fig_hist = go.Figure(
            data=[go.Histogram(x=df_buildings['risk_score'], nbinsx=30, marker_color='steelblue')]
        )
        fig_hist.update_layout(
            xaxis_title="Risk Score",
            yaxis_title="Number of Buildings",
            title="Risk Score Histogram",
            height=400
        )
        st.plotly_chart(fig_hist, use_container_width=True)

st.divider()
st.caption("💡 **Analytics Updates**: Data is refreshed as new incidents are reported and buildings are assessed. "
           "All data is derived from public sources and campus management systems.")

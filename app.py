import streamlit as st
from modules.risk_engine import RiskEngine
from modules.incident_manager import IncidentManager
from modules.cctv_manager import CCTVManager
import os
import cv2
import threading
import time
from datetime import datetime
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from modules.email_sender import send_emergency_email

# Configure page
st.set_page_config(
    page_title="Smart Campus Safety System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Professional CSS Styling
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main {
        padding: 1rem;
    }
    
    h1 {
        color: #1a1a1a;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    h2 {
        color: #2d3748;
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.3rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0.3rem 0;
    }
    
    .metric-label {
        font-size: 0.8rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .alert-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 10px rgba(245, 87, 108, 0.3);
    }
    
    .success-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.8rem 0;
    }
    
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.8rem 0;
    }
    
    .button-group {
        display: flex;
        gap: 0.8rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    
    .emergency-btn {
        background: linear-gradient(135deg, #f5576c 0%, #ff6b9d 100%) !important;
        color: white !important;
        padding: 0.8rem 1.5rem !important;
        border-radius: 6px !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(245, 87, 108, 0.3) !important;
    }
    
    .emergency-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(245, 87, 108, 0.4) !important;
    }
    
    .incident-card {
        background: white;
        border-left: 4px solid;
        padding: 1rem;
        border-radius: 6px;
        margin: 0.8rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .incident-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .severity-critical {
        border-left-color: #f5576c;
        background: linear-gradient(90deg, rgba(245,87,108,0.05) 0%, transparent 100%);
    }
    
    .severity-high {
        border-left-color: #ffa500;
        background: linear-gradient(90deg, rgba(255,165,0,0.05) 0%, transparent 100%);
    }
    
    .severity-low {
        border-left-color: #38ef7d;
        background: linear-gradient(90deg, rgba(56,239,125,0.05) 0%, transparent 100%);
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    .status-triggered {
        background: #f5576c;
        color: white;
    }
    
    .status-resolved {
        background: #38ef7d;
        color: white;
    }
    
    .status-pending {
        background: #ffa500;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'risk_engine' not in st.session_state:
    st.session_state.risk_engine = RiskEngine()
    
if 'incident_manager' not in st.session_state:
    st.session_state.incident_manager = IncidentManager()

if 'cctv_manager' not in st.session_state:
    st.session_state.cctv_manager = CCTVManager()

if 'video_running' not in st.session_state:
    st.session_state.video_running = False

if 'video_frames' not in st.session_state:
    st.session_state.video_frames = []

# Header
st.markdown("""
<div style='text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; margin-bottom: 2rem; box-shadow: 0 8px 16px rgba(0,0,0,0.2);'>
    <h1 style='color: white; margin: 0; font-size: 3rem;'>🛡️ Smart Campus Safety System</h1>
    <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 0.5rem;'>Real-time Incident Management & CCTV Monitoring</p>
</div>
""", unsafe_allow_html=True)

# Get stats
stats = st.session_state.incident_manager.get_stats()
cctv_status = st.session_state.cctv_manager.get_camera_status()

# Dashboard Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Total Incidents</div>
        <div class='metric-value'>{stats['Total']}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Active Incidents</div>
        <div class='metric-value'>{stats['Total'] - stats['Resolved']}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>High Severity</div>
        <div class='metric-value'>{stats['High Severity']}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>CCTV Recordings</div>
        <div class='metric-value'>{cctv_status['total_recordings']}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Emergency Alert Section
st.markdown("### 🚨 Emergency Alert System")
alert_col1, alert_col2, alert_col3 = st.columns([2, 1, 1])

with alert_col1:
    st.markdown("""
    <div class='alert-box'>
        ⚠️ <strong>EMERGENCY RESPONSE READY</strong><br>
        Press the button below to trigger an immediate campus-wide alert. Security teams will be notified instantly.
    </div>
    """, unsafe_allow_html=True)

with alert_col2:
    if st.button("🔴 TRIGGER ALERT", use_container_width=True):
        alert_id = st.session_state.incident_manager.trigger_emergency("Campus-Wide Emergency")
        
        # UI Feedback
        st.error(f"🚨 EMERGENCY SIGNAL BROADCASTED! Alert ID: {alert_id}")
        st.markdown(":rotating_light:" * 10)
        
        # Email Automation
        with st.spinner("Sending emergency notifications..."):
             email_subject = f"URGENT: Campus Emergency Alert {alert_id}"
             email_body = f"EMERGENCY TRIGGERED\n\nID: {alert_id}\nTime: {datetime.now()}\nLocation: Campus-Wide\n\nPlease activate emergency protocols immediately."
             success, message = send_emergency_email(email_subject, email_body)
             
             if success:
                 st.success(f"📧 {message}")
             else:
                 st.warning(f"⚠️ Email alert issue: {message}")

with alert_col3:
    active_incidents = st.session_state.incident_manager.get_all_incidents()
    active_emergencies = [i for i in active_incidents if i['status'] == 'Triggered']
    st.metric("Active Alerts", len(active_emergencies))

st.divider()

# CCTV Section
st.markdown("### 📹 Live CCTV Feed")
cctv_col1, cctv_col2 = st.columns([3, 1])

with cctv_col1:
    cctv_placeholder = st.empty()
    status_placeholder = st.empty()

with cctv_col2:
    if st.button("🎥 Start Camera"):
        st.session_state.cctv_manager.start_camera(0)
        st.success("Camera started!")
    
    if st.button("⏹️ Stop Camera"):
        st.session_state.cctv_manager.stop_camera()
        st.info("Camera stopped")
    
    st.metric("Camera Status", "🟢 Active" if cctv_status['active'] else "🔴 Inactive")
    st.metric("Frames Buffered", cctv_status['frames_captured'])

st.divider()

# Real-time Data Section
st.markdown("### 📊 Real-Time Incident Data")

tab1, tab2, tab3 = st.tabs(["Recent Incidents", "By Severity", "By Status"])

incidents = st.session_state.incident_manager.get_all_incidents()

with tab1:
    if incidents:
        for inc in incidents[:5]:
            severity_class = f"severity-{inc['severity'].lower()}"
            status_class = f"status-{inc['status'].lower().replace(' ', '-')}"
            st.markdown(f"""
            <div class='incident-card {severity_class}'>
                <strong>{inc['type']}</strong> - {inc['id']}<br>
                📍 <strong>Location:</strong> {inc['location']}<br>
                📅 <strong>Time:</strong> {inc['timestamp']}<br>
                <span class='status-badge {status_class}'>{inc['status']}</span>
                <span class='status-badge' style='background: #667eea; color: white;'>Severity: {inc['severity']}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No incidents recorded yet.")

with tab2:
    severity_counts = {}
    for inc in incidents:
        severity = inc['severity']
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
    
    if severity_counts:
        fig = go.Figure(data=[go.Pie(labels=list(severity_counts.keys()), values=list(severity_counts.values()), hole=0.3)])
        fig.update_layout(title="Incidents by Severity", height=400)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    status_counts = {}
    for inc in incidents:
        status = inc['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    if status_counts:
        fig = px.bar(x=list(status_counts.keys()), y=list(status_counts.values()), 
                     title="Incidents by Status", labels={'x': 'Status', 'y': 'Count'})
        st.plotly_chart(fig, use_container_width=True)

st.divider()

# Additional Features
st.markdown("### 🎯 Quick Actions")
action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("📋 View All Incidents", use_container_width=True):
        st.write(pd.DataFrame(incidents))

with action_col2:
    if st.button("🗺️ Risk Map", use_container_width=True):
        st.info("Risk map visualization will display here")

with action_col3:
    if st.button("📊 Analytics", use_container_width=True):
        st.info("Detailed analytics dashboard will display here")

# Footer
st.markdown("""
<div style='text-align: center; padding: 2rem; margin-top: 3rem; border-top: 2px solid #667eea;'>
    <p style='color: #666; font-size: 0.9rem;'>
        Smart Campus Safety System v1.0 | 
        <strong>CCTV Streams:</strong> {0} | 
        <strong>Active Locations:</strong> {1}<br>
        Last Updated: {2}
    </p>
</div>
""".format(cctv_status['total_recordings'], len(set(inc['location'] for inc in incidents)), datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

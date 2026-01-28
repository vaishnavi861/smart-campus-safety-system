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

# Configure page (Must be the first Streamlit command)
st.set_page_config(
    page_title="Smart Campus Safety System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    # Initialize Session State early
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

    # UI Feedback
    st.title("🛡️ Smart Campus Safety System")

    # Simplified CSS for Cloud compatibility
    st.markdown("""
    <style>
        .metric-card {
            background: #f0f2f6;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            border-left: 5px solid #667eea;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: #1f77b4;
        }
        .metric-label {
            font-size: 0.9rem;
            color: #666;
            text-transform: uppercase;
        }
    </style>
    """, unsafe_allow_html=True)

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
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Total Incidents</div><div class='metric-value'>{stats['Total']}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Active Incidents</div><div class='metric-value'>{stats['Total'] - stats['Resolved']}</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>High Severity</div><div class='metric-value'>{stats['High Severity']}</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>CCTV Recordings</div><div class='metric-value'>{cctv_status['total_recordings']}</div></div>", unsafe_allow_html=True)

    st.divider()

    # Emergency Alert Section
    st.markdown("### 🚨 Emergency Alert System")
    alert_col1, alert_col2, alert_col3 = st.columns([2, 1, 1])

    with alert_col1:
        st.info("⚠️ **EMERGENCY RESPONSE READY**: Press the button to trigger an immediate campus-wide alert.")

    with alert_col2:
        if st.button("🔴 TRIGGER EMERGENCY", use_container_width=True):
            alert_id = st.session_state.incident_manager.trigger_emergency("Campus-Wide Emergency")
            st.error(f"🚨 EMERGENCY SIGNAL BROADCASTED! Alert ID: {alert_id}")
            
            with st.spinner("Sending emergency notifications..."):
                 email_subject = f"URGENT: Campus Emergency Alert {alert_id}"
                 email_body = f"EMERGENCY TRIGGERED\n\nID: {alert_id}\nTime: {datetime.now()}\nLocation: Campus-Wide\n\nPlease activate emergency protocols immediately."
                 success, message = send_emergency_email(email_subject, email_body)
                 if success: st.success(f"📧 {message}")
                 else: st.warning(f"⚠️ Email alert issue: {message}")

    with alert_col3:
        active_incidents = st.session_state.incident_manager.get_all_incidents()
        active_emergencies = [i for i in active_incidents if i['status'] == 'Triggered']
        st.metric("Active Alerts", len(active_emergencies))

    st.divider()

    # CCTV Section
    st.markdown("### 📹 Live CCTV Feed")
    cctv_col1, cctv_col2 = st.columns([3, 1])

    with cctv_col1:
        st.info("CCTV Feed visualization is optimized for local systems. On cloud, please refer to recorded clips.")
        if cctv_status['active']:
            st.image("https://via.placeholder.com/640x480.png?text=Live+CCTV+Stream+Active", caption="Live Stream Visualization")

    with cctv_col2:
        if st.button("🎥 Start Camera"):
            st.session_state.cctv_manager.start_camera(0)
            st.success("Camera initiated")
        
        if st.button("⏹️ Stop Camera"):
            st.session_state.cctv_manager.stop_camera()
            st.info("Camera stopped")
        
        st.metric("Camera Status", "🟢 Active" if cctv_status['active'] else "🔴 Inactive")

    st.divider()

    # Real-time Data Section
    st.markdown("### 📊 Real-Time Incident Data")
    tab1, tab2, tab3 = st.tabs(["Recent Incidents", "By Severity", "By Status"])
    incidents = st.session_state.incident_manager.get_all_incidents()

    with tab1:
        if incidents:
            for inc in incidents[:5]:
                st.write(f"**{inc['type']}** - {inc['id']} | 📍 {inc['location']} | {inc['status']}")
        else:
            st.info("No incidents recorded yet.")

    with tab2:
        severity_counts = {}
        for inc in incidents:
            severity = inc['severity']
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        if severity_counts:
            fig = go.Figure(data=[go.Pie(labels=list(severity_counts.keys()), values=list(severity_counts.values()), hole=0.3)])
            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Footer
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem; margin-top: 3rem; border-top: 2px solid #667eea;'>
        <p style='color: #666; font-size: 0.9rem;'>
            Smart Campus Safety System v1.0 | 
            Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </p>
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"🚨 Critical Application Error: {e}")
    st.exception(e)
    st.info("Please check the Streamlit Cloud logs for more detailed information.")

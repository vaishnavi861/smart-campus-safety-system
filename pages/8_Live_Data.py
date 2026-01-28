import streamlit as st
from modules.risk_engine import RiskEngine
from modules.incident_manager import IncidentManager
from modules.cctv_manager import CCTVManager
import pandas as pd
import plotly.express as px
import cv2
import time
import os

st.set_page_config(page_title="Live Data & Streaming", layout="wide")

st.markdown("""
<style>
    .block-container { padding: 1rem; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Live Data & Video Stream")

# Initialize Session State Managers
if 'risk_engine' not in st.session_state:
    st.session_state.risk_engine = RiskEngine()
    
if 'incident_manager' not in st.session_state:
    st.session_state.incident_manager = IncidentManager()

if 'cctv_manager' not in st.session_state:
    st.session_state.cctv_manager = CCTVManager()

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["📹 Video Stream", "📊 Real Data", "🎥 Recordings"])

with tab1:
    st.subheader("Live Camera Feed")
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
        start_btn = st.button("▶ Start Stream", key="start_stream")
    with col2:
        stop_btn = st.button("⏹ Stop & Save", key="stop_stream")
    
    video_placeholder = st.empty()
    status = st.empty()
    
    # Handle Start
    if start_btn:
        st.session_state.video_running = True
        if not st.session_state.cctv_manager.camera:
            st.session_state.cctv_manager.start_camera(0)
        
        # Start recording to file immediately when stream starts (mimicking previous behavior)
        st.session_state.cctv_manager.start_recording_to_file(incident_id="live_stream", location="Live Data Tab")
    
    # Handle Stop
    if stop_btn:
        st.session_state.video_running = False
        saved_file = st.session_state.cctv_manager.stop_recording_to_file()
        if saved_file:
            status.success(f"✅ Video saved: {saved_file}")
        else:
            status.info("Stream stopped.")
    
    # Display Loop
    if st.session_state.get('video_running', False):
        status.info("🔴 Recording in progress...")
        
        # Check if camera is actually running
        cam_status = st.session_state.cctv_manager.get_camera_status()
        if not cam_status['active']:
             result = st.session_state.cctv_manager.start_camera(0)
             if not result:
                 st.error("Could not start camera. Please check connection.")
                 st.session_state.video_running = False
        
        # We need a loop to update the image
        # Note: In Streamlit, a long running loop prevents other interactions.
        # Ideally, we rely on rerun, but for smooth video we loop.
        # Users can click 'Stop & Save' which will register on next run, 
        # BUT we need to break the loop to process that click?
        # Actually, Streamlit buttons inside a loop are tricky.
        # We will use a lightweight loop that runs for a short burst or rely on autorefresh?
        # A common pattern is `while True` and breaking if a UI element changes, but UI elements don't update inside loop.
        # So we will run the loop. To stop, the user might need to click 'Stop' which triggers a rerun.
        # But while looping, Streamlit is busy. 
        # Better approach: Loop for a few frames then rerun? No, that flickers.
        # We will run a loop and check for a placeholder button? No.
        # The 'Stop & Save' button above handles the logic on Re-Run.
        # So inside the loop, we are blind to the button click until the script restarts?
        # No, actually the script handles the click BEFORE entering this block.
        # So if we are in this block, 'Stop' was NOT clicked this run.
        # We need a way to break the loop. 
        # Streamlit doesn't interpret events while in a loop.
        # So we will rely on a "st.stop" or similar?
        # Actually, if we loop forever, the user CANNOT click stop.
        # So we shouldn't loop forever.
        # We can loop using `streamlit-autorefresh` (not available) or `st.empty` update.
        # The best we can do without custom components is to display the LATEST frame
        # and rely on the script re-running.
        # But standard Streamlit script doesn't re-run 30 times a second automatically.
        # We can use `st.rerun()` at the end of the block?
        # Let's try `st.rerun()` pattern.
        
        frame = st.session_state.cctv_manager.get_latest_frame()
        if frame is not None:
             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
             video_placeholder.image(frame_rgb, use_container_width=True)
        else:
             video_placeholder.warning("Waiting for camera...")
        
        time.sleep(0.05)
        st.rerun()

with tab2:
    st.subheader("Real Building Data Analysis")
    
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
        # Check for cached data
        if 'real_data_analysis' in st.session_state:
            cached_data = st.session_state['real_data_analysis']
            age = time.time() - cached_data['timestamp']
            if age < 300: # 5 minutes
                 st.info(f"Showing cached analysis from {int(age)}s ago (Expires in {300-int(age)}s)")
                 building_risks = cached_data['data']
            else:
                 del st.session_state['real_data_analysis']
                 building_risks = None
        else:
            building_risks = None

        if st.button("🔄 Execute Real Data", key="execute_data"):
            with st.spinner("Analyzing..."):
                building_risks = st.session_state.risk_engine.execute_real_data_analysis()
                st.session_state['real_data_analysis'] = {
                    'data': building_risks,
                    'timestamp': time.time()
                }
        
        if building_risks:
            df_display = pd.DataFrame(building_risks)
            st.dataframe(df_display, use_container_width=True)
            
            # Chart
            fig = px.bar(df_display.head(10), x='building', y='risk_score', 
                        color='risk_level', title="Top Risk Buildings")
            st.plotly_chart(fig, use_container_width=True)
            
            if st.button("🗑️ Clear Results"):
                if 'real_data_analysis' in st.session_state:
                    del st.session_state['real_data_analysis']
                    st.rerun()
        else:
            if 'real_data_analysis' not in st.session_state:
                st.warning("No data available. Click Execute to analyze.")
    
    with col2:
        if st.button("🌡️ Live Weather", key="weather_data"):
            weather = st.session_state.risk_engine.get_live_weather()
            col_w1, col_w2 = st.columns(2)
            with col_w1:
                st.metric("Temperature", f"{weather['temp']}°C")
                st.metric("Humidity", f"{weather['humidity']}%")
            with col_w2:
                st.metric("Wind Speed", f"{weather['windspeed']} km/h")
                st.metric("Condition", weather['condition'])
    
    # Incidents in real-time
    st.subheader("Real-Time Incidents")
    if st.button("📋 Refresh Incidents", key="refresh_incidents"):
        incidents = st.session_state.incident_manager.get_all_incidents()
        if incidents:
            df_inc = pd.DataFrame(incidents[-20:])
            st.dataframe(df_inc[['id', 'location', 'status', 'severity', 'timestamp']], 
                        use_container_width=True, height=300)
        else:
            st.info("No incidents recorded yet")

with tab3:
    st.subheader("Video Recordings Archive")
    
    # Use CCTVManager's recordings
    recordings = st.session_state.cctv_manager.get_all_recordings()
    
    if recordings:
        for rec in recordings:
            col_r1, col_r2, col_r3 = st.columns([3, 1, 1])
            with col_r1:
                st.text(f"📹 {rec['filename']} (Duration: {rec.get('duration', '?')}s)")
            with col_r2:
                if st.button("Play", key=f"play_{rec['filename']}"):
                    if os.path.exists(rec['path']):
                        video_file = open(rec['path'], 'rb')
                        st.video(video_file)
                    else:
                        st.error("File not found on disk")
            with col_r3:
                if st.button("🗑️ Delete", key=f"del_LD_{rec['filename']}"):
                    if st.session_state.cctv_manager.delete_recording(rec['filename']):
                        st.success("Deleted!")
                        st.rerun()
                    else:
                        st.error("Failed to delete")

    else:
        st.info("No recordings yet. Start recording from the Stream tab.")

# Footer
st.divider()
st.caption("🛡️ Smart Campus Safety - Live Data System | Real-time execution enabled")

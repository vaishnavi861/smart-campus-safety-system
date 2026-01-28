import streamlit as st
import cv2
import numpy as np
from modules.cctv_manager import CCTVManager
from modules.incident_manager import IncidentManager
import threading
import time

st.set_page_config(
    page_title="CCTV Live Feed",
    page_icon="📹",
    layout="wide"
)

st.markdown("""
<style>
    .block-container {
        padding: 1rem;
        max-width: 100%;
    }
    h1, h2 { margin: 0.5rem 0; }
</style>
""", unsafe_allow_html=True)

# Initialize managers
if 'cctv_manager' not in st.session_state:
    st.session_state.cctv_manager = CCTVManager()

if 'incident_manager' not in st.session_state:
    st.session_state.incident_manager = IncidentManager()

st.title("📹 CCTV Live Feed & Recordings")

# Sidebar controls
with st.sidebar:
    st.header("Camera Controls")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎥 Start Camera"):
            if st.session_state.cctv_manager.start_camera(0):
                st.success("Camera started!")
            else:
                st.error("Could not start camera")
    
    with col2:
        if st.button("⏹️ Stop Camera"):
            st.session_state.cctv_manager.stop_camera()
            st.info("Camera stopped")
    
    st.divider()
    
    st.header("Recording Controls")
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        if st.button("🔴 Record"):
            if st.session_state.cctv_manager.start_recording_to_file(incident_id="manual", location="CCTV Feed"):
                st.success("Recording started!")
            else:
                st.error("Start camera first!")
                
    with col_rec2:
        if st.button("⏹️ Stop Rec"):
            path = st.session_state.cctv_manager.stop_recording_to_file()
            if path:
                st.success(f"Saved: {os.path.basename(path)}")
            else:
                st.info("Not recording")

    st.divider()
    
    # Camera Status
    status = st.session_state.cctv_manager.get_camera_status()
    st.metric("Camera Status", "🟢 Active" if status['active'] else "🔴 Inactive")
    st.metric("Recording", "🔴 YES" if getattr(st.session_state.cctv_manager, 'file_recording', False) else "⚫ NO")
    st.metric("Frames Buffered", status['frames_captured'])
    st.metric("Total Recordings", len(st.session_state.cctv_manager.recordings))

# Main content
tab1, tab2, tab3 = st.tabs(["Live Feed", "Recordings", "Incident Mapping"])

with tab1:
    st.subheader("Live CCTV Feed")
    col_feed, col_info = st.columns([3, 1])
    
    with col_feed:
        frame_placeholder = st.empty()
        status_placeholder = st.empty()
        
        # Auto-refresh loop
        while True:
            frame = st.session_state.cctv_manager.get_latest_frame()
            
            if frame is not None:
                # Convert BGR to RGB for display
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_placeholder.image(frame_rgb, use_container_width=True)
                status_placeholder.success("📹 Live Feed Active")
            else:
                frame_placeholder.warning("⚠️ No camera feed available. Click 'Start Camera' in sidebar.")
                status_placeholder.info("Camera not started")
            
            time.sleep(0.1)  # Update every 100ms
    
    with col_info:
        st.info("📊 Feed Info")
        status = st.session_state.cctv_manager.get_camera_status()
        st.write(f"**Status**: {'Active' if status['active'] else 'Inactive'}")
        st.write(f"**Resolution**: 640x480")
        st.write(f"**FPS**: 30")

with tab2:
    st.subheader("📹 Video Recordings")
    
    recordings = st.session_state.cctv_manager.get_all_recordings()
    
    if recordings:
        # Display recordings in a table
        st.write(f"**Total Recordings**: {len(recordings)}")
        
        for rec in recordings:
            with st.expander(f"📹 {rec['filename']} - {rec['location']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Incident ID**: {rec['id']}")
                    st.write(f"**Location**: {rec['location']}")
                    st.write(f"**Timestamp**: {rec['timestamp']}")
                
                with col2:
                    st.write(f"**Duration**: {rec.get('duration', '?')}s")
                    st.write(f"**File**: {rec['filename']}")
                    if st.button(f"🗑️ Delete", key=f"del_CCTV_{rec['filename']}"):
                        if st.session_state.cctv_manager.delete_recording(rec['filename']):
                            st.success("Recording deleted")
                            st.rerun()
                        else:
                            st.error("Failed to delete")
    else:
        st.info("No recordings yet. Start camera and trigger an incident to create recordings.")

with tab3:
    st.subheader("🗺️ Incidents with CCTV Footage")
    
    incidents = st.session_state.incident_manager.get_all_incidents()
    
    if incidents:
        # Filter incidents with potential CCTV footage
        for incident in incidents[:10]:  # Show first 10
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.write(f"**{incident['type']}**")
                st.write(f"Location: {incident['location']}")
            
            with col2:
                st.write(f"Severity: {incident['severity']}")
                st.write(f"Status: {incident['status']}")
            
            with col3:
                cctv_recordings = st.session_state.cctv_manager.get_recordings_by_incident(incident['id'])
                if cctv_recordings:
                    st.success(f"📹 {len(cctv_recordings)} videos")
                else:
                    st.caption("No CCTV")
    else:
        st.info("No incidents recorded yet.")

    st.divider()
    st.subheader("📂 Manual Recordings (Unassigned)")
    # Filter for manual recordings
    all_recordings = st.session_state.cctv_manager.get_all_recordings()
    manual_recordings = [r for r in all_recordings if r['id'] == 'manual' or r['id'] == 'live_stream']
    
    if manual_recordings:
         for rec in manual_recordings:
             col_m1, col_m2 = st.columns([3, 1])
             with col_m1:
                 st.info(f"📹 {rec['filename']} | Location: {rec['location']} | Time: {rec['timestamp']}")
             with col_m2:
                  st.caption(f"Duration: {rec.get('duration','?')}s")
    else:
        st.caption("No manual recordings found.")

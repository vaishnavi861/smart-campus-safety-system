import streamlit as st
from modules.incident_manager import IncidentManager

st.set_page_config(page_title="Report Incident", page_icon="📝")

st.title("📝 Report Safety Incident")
st.markdown("Submit a new incident report. Critical reports trigger immediate alerts.")

if 'incident_manager' not in st.session_state:
    st.session_state.incident_manager = IncidentManager()

with st.form("report_form"):
    col1, col2 = st.columns(2)
    with col1:
        inc_type = st.selectbox("Incident Type", ["Structural Damage", "Fire Hazard", "Medical Emergency", "Crowd Control", "Security Breach"])
        location = st.text_input("Location (Building/Zone)", placeholder="e.g. Main Entrance, Building B")
    with col2:
        severity = st.select_slider("Severity Level", options=["Low", "Medium", "High", "Critical"])
        reporter = st.text_input("Reported By (Optional)", placeholder="Name or ID")
        
    description = st.text_area("Description of Incident", height=100)
    
    submitted = st.form_submit_button("Submit Report")
    
    if submitted:
        if not location or not description:
            st.error("Please fill in location and description.")
        else:
            inc_id = st.session_state.incident_manager.report_incident(
                inc_type, location, severity, description, reporter or "Anonymous"
            )
            st.success(f"Incident Reported Successfully! ID: {inc_id}")
            
            if severity in ["High", "Critical"]:
                st.error(f"🚨 ALERT TRIGGERED: High severity incident reported at {location}!")

import streamlit as st
from modules.incident_manager import IncidentManager, VALID_STATUS_TRANSITIONS
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Incident Tracker", page_icon="📋", layout="wide")

st.title("📋 Incident Tracking & Resolution Workflow")
st.markdown("Track and manage the lifecycle of reported incidents from initial report to final resolution.")

if 'incident_manager' not in st.session_state:
    st.session_state.incident_manager = IncidentManager()

incidents = st.session_state.incident_manager.get_all_incidents()

if not incidents:
    st.info("✅ No incidents reported yet. The campus is safe!")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame(incidents)

# Sidebar Filters
st.sidebar.header("🔍 Filters")
status_options = sorted(df['status'].unique())
severity_options = sorted(df['severity'].unique())

status_filter = st.sidebar.multiselect(
    "Filter by Status",
    status_options,
    default=status_options
)

severity_filter = st.sidebar.multiselect(
    "Filter by Severity",
    severity_options,
    default=severity_options
)

# Apply filters
filtered_df = df[
    (df['status'].isin(status_filter)) & 
    (df['severity'].isin(severity_filter))
].copy()

# Display summary
summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

with summary_col1:
    st.metric("📍 Total Incidents", len(filtered_df))
with summary_col2:
    resolved = len(filtered_df[filtered_df['status'] == 'Resolved'])
    st.metric("✅ Resolved", resolved, delta=f"{resolved/len(filtered_df)*100:.1f}%" if len(filtered_df) > 0 else "0%")
with summary_col3:
    pending = len(filtered_df[filtered_df['status'] != 'Resolved'])
    st.metric("⏳ Pending Action", pending)
with summary_col4:
    critical = len(filtered_df[filtered_df['severity'] == 'Critical'])
    st.metric("🚨 Critical Priority", critical, delta_color="inverse")

st.divider()

# Incidents Table
st.subheader("Incident Overview")

display_df = filtered_df[['id', 'timestamp', 'type', 'location', 'severity', 'status', 'reporter', 'assigned_to']].copy()
display_df.columns = ['ID', 'Reported', 'Type', 'Location', 'Severity', 'Status', 'Reporter', 'Assigned To']

# Color code severity
def severity_color(severity):
    colors = {'Critical': '🔴', 'High': '🟠', 'Medium': '🟡', 'Low': '🟢'}
    return colors.get(severity, '⚪')

display_df['Severity'] = display_df['Severity'].apply(lambda x: f"{severity_color(x)} {x}")

st.dataframe(
    display_df.sort_values('Reported', ascending=False),
    use_container_width=True,
    hide_index=True
)

st.divider()

# Incident Management Panel
st.subheader("🛠️ Manage Incident Workflow")

col1, col2 = st.columns([1, 2])

with col1:
    incident_ids = filtered_df['id'].tolist()
    if not incident_ids:
        st.warning("No incidents to manage with current filters.")
        st.stop()
    
    selected_id = st.selectbox("Select Incident ID", incident_ids)

if selected_id:
    incident = st.session_state.incident_manager.get_incident(selected_id)
    
    with col2:
        st.write(f"**🔔 Current Status:** `{incident['status']}`")
        st.write(f"**📝 Type:** {incident['type']}")
        st.write(f"**📍 Location:** {incident['location']}")
        st.write(f"**⚠️ Severity:** {incident['severity']}")
        st.write(f"**📄 Description:** {incident['description']}")
        st.write(f"**👤 Reported By:** {incident['reporter']}")
        st.write(f"**⏰ Reported At:** {incident['timestamp']}")
        
        if incident.get('assigned_to'):
            st.write(f"**👨‍💼 Assigned To:** {incident['assigned_to']}")
    
    st.divider()
    
    # Status Update Form
    current_status = incident['status']
    next_steps = VALID_STATUS_TRANSITIONS.get(current_status, [])
    
    st.subheader("📋 Update Incident Status")
    
    with st.form("status_update_form"):
        col_form1, col_form2 = st.columns(2)
        
        with col_form1:
            if next_steps:
                new_status = st.selectbox(
                    "New Status",
                    next_steps,
                    help=f"Valid transitions from '{current_status}'"
                )
            else:
                st.info(f"✅ Status '{current_status}' is terminal (Resolved). No further updates allowed.")
                new_status = current_status
        
        with col_form2:
            assignee = st.text_input(
                "Assign To (Team/Person)",
                value=incident.get('assigned_to', ''),
                placeholder="e.g., Structural Team, John Doe"
            )
        
        note = st.text_area(
            "Resolution/Update Note",
            placeholder="e.g., Inspection completed. Minor repairs scheduled for next week.",
            height=100
        )
        
        update_btn = st.form_submit_button("✅ Update Status", type="primary")
        
        if update_btn:
            if new_status != current_status:
                success, msg = st.session_state.incident_manager.update_status(
                    selected_id, new_status, note, assignee
                )
                if success:
                    st.success(f"✅ Status updated to: **{new_status}**")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")
            else:
                st.warning("No status change made.")
    
    # Timeline View
    st.divider()
    st.subheader("📅 Incident Timeline")
    st.caption("Complete history of status changes and updates")
    
    for event in sorted(incident['history'], key=lambda x: x['timestamp']):
        status_badge = {
            'Reported': '🔴',
            'Inspected': '🟠',
            'Action Assigned': '🟡',
            'Area Secured': '🔵',
            'Resolved': '🟢'
        }.get(event['status'], '⚪')
        
        st.write(f"**{status_badge} {event['status']}** — {event['timestamp']}")
        st.write(f"└─ {event['note']}")
        st.write(f"└─ *Updated by: {event.get('updated_by', 'System')}*")
        st.divider()

import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="Public Incident Archive", page_icon="📰", layout="wide")

st.title("📰 Public Incident Archive")
st.markdown("""
**Transparency Notice**: This archive contains incidents sourced from **internally reported and publicly available data**. 
It is maintained for historical tracking and institutional transparency. 
The system uses only **synthetic/anonymized data** for demonstration purposes.
""")

DATA_PATH = 'data/public_incidents.json'

def load_public_incidents():
    """Load incident data from public archive."""
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

incidents = load_public_incidents()

if not incidents:
    st.info("📊 No public incident records available yet. Check back as incidents are resolved and made public.")
else:
    # Convert to DataFrame for easier analysis
    df_incidents = pd.DataFrame(incidents)
    
    # Ensure all required columns exist
    if 'severity' not in df_incidents.columns:
        df_incidents['severity'] = 'Medium'  # Default severity
    if 'status' not in df_incidents.columns:
        df_incidents['status'] = 'Reported'  # Default status
    
    # Summary Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📍 Total Incidents", len(df_incidents))
    
    with col2:
        resolved = len(df_incidents[df_incidents['status'] == 'Resolved'])
        st.metric("✅ Resolved", resolved)
    
    with col3:
        critical = len(df_incidents[df_incidents['severity'] == 'Critical'])
        st.metric("🚨 Critical", critical)
    
    with col4:
        inspection = len(df_incidents[df_incidents['status'] == 'Inspected'])
        st.metric("🔍 Inspected", inspection)
    
    st.divider()
    
    # Filters
    st.subheader("🔍 Filter & Search")
    
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        selected_types = st.multiselect(
            "Incident Types",
            options=sorted(df_incidents['type'].unique()),
            default=sorted(df_incidents['type'].unique())
        )
    
    with filter_col2:
        selected_severity = st.multiselect(
            "Severity Levels",
            options=['Low', 'Medium', 'High', 'Critical'],
            default=['Low', 'Medium', 'High', 'Critical']
        )
    
    with filter_col3:
        selected_status = st.multiselect(
            "Status",
            options=sorted(df_incidents['status'].unique()),
            default=sorted(df_incidents['status'].unique())
        )
    
    # Apply filters
    filtered_df = df_incidents[
        (df_incidents['type'].isin(selected_types)) &
        (df_incidents['severity'].isin(selected_severity)) &
        (df_incidents['status'].isin(selected_status))
    ].copy()
    
    st.divider()
    
    # Display filtered incidents
    st.subheader(f"📋 Public Incidents ({len(filtered_df)} records)")
    
    if len(filtered_df) == 0:
        st.info("No incidents match the selected filters.")
    else:
        # Ensure timestamp column exists
        if 'timestamp' in filtered_df.columns:
            filtered_df = filtered_df.sort_values('timestamp', ascending=False)
        else:
            filtered_df = filtered_df.sort_index(ascending=False)
        
        # Display as table first
        # Only select columns that exist in the DataFrame
        available_cols = ['id', 'timestamp', 'type', 'location', 'severity', 'status', 'reporter']
        existing_cols = [col for col in available_cols if col in filtered_df.columns]
        
        # Add defaults for missing columns
        for col in available_cols:
            if col not in filtered_df.columns:
                if col == 'timestamp':
                    filtered_df[col] = 'N/A'
                elif col == 'reporter':
                    filtered_df[col] = 'Anonymous'
        
        display_df = filtered_df[available_cols].copy()
        display_df.columns = ['ID', 'Reported', 'Type', 'Location', 'Severity', 'Status', 'Reporter']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Detailed view with expanders
        st.subheader("📄 Detailed Incident Records")
        
        for idx, (_, inc) in enumerate(filtered_df.iterrows()):
            # Status badge
            status_icon = {
                'Reported': '🔴',
                'Inspected': '🟠',
                'Action Assigned': '🟡',
                'Area Secured': '🔵',
                'Resolved': '🟢'
            }.get(inc.get('status', 'Reported'), '⚪')
            
            severity_icon = {
                'Low': '🟢',
                'Medium': '🟡',
                'High': '🟠',
                'Critical': '🔴'
            }.get(inc.get('severity', 'Medium'), '⚪')
            
            with st.expander(f"{status_icon} {severity_icon} **ID: {inc.get('id', 'N/A')}** | {inc.get('type', 'Unknown')} @ {inc.get('location', 'Unknown')} ({inc.get('timestamp', 'N/A')[:10] if isinstance(inc.get('timestamp'), str) else 'N/A'})"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Incident details
                    st.write(f"**Incident Type:** {inc.get('type', 'Unknown')}")
                    st.write(f"**Location:** {inc.get('location', 'Unknown')}")
                    st.write(f"**Severity:** {severity_icon} {inc.get('severity', 'Unknown')}")
                    st.write(f"**Status:** {status_icon} {inc.get('status', 'Unknown')}")
                    st.write(f"**Reported By:** {inc.get('reporter', 'Anonymous')}")
                    st.write(f"**Reported At:** {inc.get('timestamp', 'N/A')}")
                    
                    st.markdown("---")
                    
                    st.write(f"**Description:**\n{inc.get('description', 'N/A')}")
                    
                    if inc.get('assigned_to'):
                        st.write(f"**Assigned To:** {inc['assigned_to']}")
                    
                    # History
                    if 'history' in inc and inc['history']:
                        st.markdown("**Status History:**")
                        for event in sorted(inc['history'], key=lambda x: x.get('timestamp', '')):
                            st.caption(f"• {event.get('timestamp', 'N/A')} - {event.get('status', 'N/A')}: {event.get('note', 'N/A')}")
                
                with col2:
                    st.metric("Incident ID", inc.get('id', 'N/A'))
                    st.write("")
                    st.info(f"**Status:** {inc.get('status', 'Unknown')}\n\n**Severity:** {inc.get('severity', 'Unknown')}")

st.divider()

# Privacy Statement
st.markdown("""
---
### 🔐 Data Privacy & Transparency

This Public Archive contains only **non-confidential incident data** and uses **anonymized/synthetic information**:

✅ **What's Included:**
- Incident types and general descriptions
- Status and resolution information
- Public safety insights

❌ **What's Excluded:**
- Personal identifying information
- Confidential institutional data
- Sensitive medical or security details

📋 **Purpose**: Institutional transparency, incident trend analysis, and safety improvement planning.

For detailed institutional reports, contact Campus Safety & Security Administration.
""")

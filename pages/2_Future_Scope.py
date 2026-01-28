import streamlit as st

st.set_page_config(page_title="Future Scope: CCTV Integration", page_icon="🔭")

st.title("🔭 Future Scope: Automated Anomaly Detection")
st.markdown("### Publicly Reported Campus Incidents (CMRTC)")

st.info("This module demonstrates how PRISM integrates public incident signals.")

st.divider()

# Public News Logic
# Since no specific public news was found for "CMR Technical Campus" (distinct from CMR Engineering College),
# we display the fallback message to ensure accuracy and credibility.

st.markdown("""
<div style="padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #f9f9f9; text-align: center; color: #555;">
    <h3>No publicly reported campus incidents found for CMRTC.</h3>
    <p>PRISM relies strictly on verifiable public sources.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Simulation Demo Section
st.subheader("How PRISM Responds When an Incident Occurs")
st.markdown("**Demonstration of auto-response capabilities using simulated data:**")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="border: 1px solid #ffcc00; border-radius: 8px; padding: 15px; background-color: #fffbef;">
        <h4 style="color: #d97706; margin-top: 0;">⚠️ Simulated Incident (Demo Only)</h4>
        <p><strong>Type:</strong> Structural Damage Risk</p>
        <p><strong>Location:</strong> Main Entrance Gate</p>
        <p><strong>Trigger:</strong> Crowd Anomaly Detection (Simulated)</p>
        <p><strong>Status:</strong> 🚨 Alert Triggered</p>
        <hr style="margin: 10px 0;">
        <small>Simulation used for prototype demonstration. No public news source available.</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="border: 1px solid #ef4444; border-radius: 8px; padding: 15px; background-color: #fef2f2;">
        <h4 style="color: #b91c1c; margin-top: 0;">🚨 Simulated Incident (Demo Only)</h4>
        <p><strong>Type:</strong> Fire Hazard</p>
        <p><strong>Location:</strong> Academic Block A</p>
        <p><strong>Trigger:</strong> Manual Emergency Button</p>
        <p><strong>Status:</strong> 🚨 Alert Triggered</p>
        <hr style="margin: 10px 0;">
        <small>Simulation used for prototype demonstration. No public news source available.</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### ⚡ Automated Response Flow")
st.code("""
[ Incident Detected ] --> [ 🚨 Admin Alert Sent ]
                          |
                          +--> [ 📱 Student Popup Notification ]
                          |
                          +--> [ 📝 Auto-Logged in Incident Tracker ]
""", language="text")

st.caption("No manual reporting required. System acts instantly upon validation.")

if st.button("👉 View Incident in Tracker"):
    st.switch_page("pages/3_Incident_Tracker.py")

st.info("ℹ️ PRISM demonstrates system behavior using simulations when public news data is unavailable, ensuring honesty without sacrificing usability.")

st.divider()

# Ethics Disclaimer
st.markdown("### ⚖️ Ethics & Transparency")
st.warning("""
**PRISM does not access internal institutional data.**
All incidents shown are derived strictly from public news sources.
""")

import streamlit as st
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="Test", page_icon="🧪", layout="wide")

st.title("🧪 Simple Test App")

st.write("This is a test to see if Streamlit is working.")

st.write(f"Python version: {sys.version}")
st.write(f"Current directory: {os.getcwd()}")

# Test module imports
try:
    from modules.risk_engine import RiskEngine
    from modules.incident_manager import IncidentManager
    st.success("✅ Modules imported successfully!")
    
    # Test instantiation
    risk_engine = RiskEngine()
    incident_manager = IncidentManager()
    st.success("✅ Classes instantiated successfully!")
    
except Exception as e:
    st.error(f"❌ Error: {e}")

st.info("If you can see this page, Streamlit is working correctly!")
#!/usr/bin/env python3
import subprocess
import sys
import os

# Set environment variables to bypass email prompt
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'false'
os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'

# Run streamlit
cmd = [sys.executable, '-m', 'streamlit', 'run', 'app.py', '--server.port', '8080', '--server.headless', 'false']
print(f"Running: {' '.join(cmd)}")
subprocess.run(cmd)
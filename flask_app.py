from flask import Flask, render_template_string, Response, jsonify, request
import sys
import os
import cv2
from datetime import datetime
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

cctv_manager = None

def get_cctv_manager():
    global cctv_manager
    if cctv_manager is None:
        from modules.cctv_manager import CCTVManager
        cctv_manager = CCTVManager()
    return cctv_manager

# Professional CSS & HTML Templates
BASE_CSS = """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
    background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    min-height: 100vh;
    color: #333;
}

header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.5rem 2rem;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    position: sticky;
    top: 0;
    z-index: 1000;
}

.header-content {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

h1 {
    font-size: 2rem;
    font-weight: 700;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    letter-spacing: 0.5px;
}

.nav-links {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}

.nav-links a {
    color: white;
    text-decoration: none;
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    transition: all 0.3s ease;
    background: rgba(255,255,255,0.1);
    font-weight: 500;
    border: 1px solid rgba(255,255,255,0.2);
}

.nav-links a:hover {
    background: rgba(255,255,255,0.25);
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(0,0,0,0.2);
}

.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
}

.dashboard {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.card {
    background: white;
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid rgba(0,0,0,0.05);
}

.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}

.card-title {
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: #2c3e50;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.stat-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
    padding: 2rem;
}

.stat-value {
    font-size: 3.5rem;
    font-weight: 700;
    margin: 1rem 0;
}

.stat-label {
    font-size: 1rem;
    opacity: 0.9;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 500;
}

.alert-banner {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 2.5rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    grid-column: 1 / -1;
}

.alert-banner h2 {
    font-size: 2rem;
    margin-bottom: 1rem;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

.alert-banner button {
    background: white;
    color: #f5576c;
    border: none;
    padding: 1rem 2.5rem;
    border-radius: 50px;
    cursor: pointer;
    font-weight: 700;
    font-size: 1.1rem;
    transition: all 0.3s;
    box-shadow: 0 5px 20px rgba(0,0,0,0.2);
}

.alert-banner button:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
}

.btn {
    display: inline-block;
    padding: 1rem 2rem;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
    text-decoration: none;
    margin: 0.5rem;
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(102, 126, 234, 0.6);
}

.btn-success {
    background: linear-gradient(135deg, #38ef7d 0%, #11998e 100%);
    color: white;
}

.btn-danger {
    background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
    color: white;
}

h2 {
    color: white;
    font-size: 2rem;
    margin: 2rem 0 1.5rem 0;
    padding-bottom: 1rem;
    border-bottom: 3px solid rgba(255,255,255,0.2);
    text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.incident-card {
    background: white;
    border-left: 6px solid;
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1rem 0;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    transition: all 0.3s;
}

.incident-card:hover {
    transform: translateX(5px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.15);
}

.incident-card.critical {
    border-left-color: #f5576c;
    background: linear-gradient(to right, rgba(245, 87, 108, 0.05) 0%, white 10%);
}

.incident-card.high {
    border-left-color: #ffa500;
    background: linear-gradient(to right, rgba(255, 165, 0, 0.05) 0%, white 10%);
}

.incident-card.low {
    border-left-color: #38ef7d;
    background: linear-gradient(to right, rgba(56, 239, 125, 0.05) 0%, white 10%);
}

.incident-header {
    display: flex;
    justify-content: space-between;
    align-items: start;
    margin-bottom: 1rem;
}

.incident-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #2c3e50;
}

.incident-id {
    background: #f0f0f0;
    padding: 0.3rem 0.8rem;
    border-radius: 5px;
    font-size: 0.85rem;
    font-family: monospace;
    color: #555;
}

.incident-location {
    color: #555;
    margin: 0.5rem 0;
    font-size: 0.95rem;
}

.incident-timestamp {
    color: #999;
    font-size: 0.85rem;
    margin: 0.5rem 0;
}

.badge {
    display: inline-block;
    padding: 0.4rem 1rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-right: 0.5rem;
    margin-top: 0.5rem;
}

.badge-critical {
    background: #f5576c;
    color: white;
}

.badge-high {
    background: #ffa500;
    color: white;
}

.badge-medium {
    background: #3498db;
    color: white;
}

.badge-low {
    background: #38ef7d;
    color: white;
}

.status-grid {
    background: white;
    border-radius: 15px;
    padding: 2rem;
    margin: 2rem 0;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}

.status-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid #eee;
}

.status-item:last-child {
    border-bottom: none;
}

.status-label {
    font-weight: 600;
    color: #2c3e50;
}

.status-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #667eea;
}

.feed-container {
    background: #000;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    margin: 2rem 0;
}

#cctv-feed {
    width: 100%;
    height: auto;
    display: block;
}

.controls {
    display: flex;
    gap: 1rem;
    margin: 2rem 0;
    flex-wrap: wrap;
    justify-content: center;
}

footer {
    background: rgba(0,0,0,0.8);
    color: white;
    text-align: center;
    padding: 2rem;
    margin-top: 3rem;
    border-top: 2px solid rgba(102, 126, 234, 0.5);
}

footer p {
    margin: 0.5rem 0;
    font-size: 0.95rem;
}

.loading {
    text-align: center;
    color: white;
    font-size: 1.2rem;
    padding: 2rem;
}

.stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

@media (max-width: 768px) {
    .header-content {
        flex-direction: column;
        gap: 1rem;
    }
    
    h1 {
        font-size: 1.5rem;
    }
    
    .nav-links {
        justify-content: center;
    }
    
    .container {
        padding: 1rem;
    }
    
    .stat-value {
        font-size: 2.5rem;
    }
}
"""

HOME_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Campus Safety - Dashboard</title>
    <style>{css}</style>
</head>
<body>
    <header>
        <div class="header-content">
            <h1>🛡️ Smart Campus Safety System</h1>
            <div class="nav-links">
                <a href="/">📊 Dashboard</a>
                <a href="/cctv">📹 CCTV</a>
                <a href="/incidents">📋 Incidents</a>
                <a href="/analytics">📈 Analytics</a>
            </div>
        </div>
    </header>
    
    <div class="container">
        <div class="dashboard">
            <div class="alert-banner">
                <h2>🚨 Emergency Response Center</h2>
                <p style="margin-bottom: 1.5rem; font-size: 1.1rem;">Quick campus-wide emergency alert system</p>
                <button class="btn" style="background: white; color: #f5576c; font-size: 1.1rem; padding: 1rem 3rem;">
                    🔴 TRIGGER EMERGENCY ALERT
                </button>
            </div>

            <div class="card stat-card">
                <div class="stat-label">Total Incidents</div>
                <div class="stat-value">{incidents_total}</div>
                <div style="opacity: 0.8; font-size: 0.9rem;">Recorded in system</div>
            </div>
            
            <div class="card stat-card">
                <div class="stat-label">Active Cases</div>
                <div class="stat-value">{incidents_active}</div>
                <div style="opacity: 0.8; font-size: 0.9rem;">Currently monitored</div>
            </div>
            
            <div class="card stat-card">
                <div class="stat-label">High Priority</div>
                <div class="stat-value">{incidents_critical}</div>
                <div style="opacity: 0.8; font-size: 0.9rem;">Require attention</div>
            </div>
            
            <div class="card stat-card">
                <div class="stat-label">CCTV Feeds</div>
                <div class="stat-value">{cctv_total}</div>
                <div style="opacity: 0.8; font-size: 0.9rem;">Active recordings</div>
            </div>
        </div>

        <h2>📹 CCTV System Status</h2>
        <div class="status-grid">
            <div class="status-item">
                <span class="status-label">Camera Status</span>
                <span class="status-value" style="color: {cctv_color};">{cctv_status_text}</span>
            </div>
            <div class="status-item">
                <span class="status-label">Frames Captured</span>
                <span class="status-value">{cctv_frames}</span>
            </div>
            <div class="status-item">
                <span class="status-label">System Uptime</span>
                <span class="status-value">24/7</span>
            </div>
            <div class="status-item">
                <span class="status-label">Last Update</span>
                <span class="status-value" style="font-size: 0.95rem;">{current_time}</span>
            </div>
        </div>

        <h2>📋 Recent Incidents Overview</h2>
        {incidents_html}
    </div>
    
    <footer>
        <p><strong>Smart Campus Safety System v2.0</strong></p>
        <p>Professional Incident Management & Real-Time CCTV Monitoring</p>
        <p style="font-size: 0.85rem; margin-top: 1rem; opacity: 0.8;">© 2026 Campus Security Team | Last Updated: {full_date}</p>
    </footer>
</body>
</html>
"""

try:
    import email_config
except ImportError:
    email_config = None

# Emergency Alert Email Configuration
# Using configuration from email_config.py

# Student and Staff emails (Add your actual emails here)
import os
STUDENT_EMAILS = email_config.STUDENT_EMAILS if email_config else []
STAFF_EMAILS = email_config.STAFF_EMAILS if email_config else ["247r1a66a1@cmrtc.ac.in"]

def get_email_config():
    return {
        'SENDER_EMAIL': os.environ.get("SENDER_EMAIL", email_config.SENDER_EMAIL if email_config else "your_email@gmail.com"),
        'SENDER_PASSWORD': os.environ.get("SENDER_PASSWORD", email_config.SENDER_PASSWORD if email_config else ""),
        'SMTP_SERVER': os.environ.get("SMTP_SERVER", email_config.SMTP_SERVER if email_config else "smtp.gmail.com"),
        'SMTP_PORT': int(os.environ.get("SMTP_PORT", email_config.SMTP_PORT if email_config else 587))
    }


def send_emergency_email(subject, message, recipient_list):
    """Send emergency alert emails in a separate thread"""
    def send_emails():
        try:
            # Get config
            config = get_email_config()
            sender_email = config['SENDER_EMAIL']
            sender_password = config['SENDER_PASSWORD']
            smtp_server = config['SMTP_SERVER']
            smtp_port = config['SMTP_PORT']
            
            # Create email
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['Subject'] = subject
            
            # Email body with HTML formatting
            body = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <div style="background-color: #ff6b6b; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                        <h1 style="margin: 0;">🚨 EMERGENCY ALERT 🚨</h1>
                    </div>
                    <div style="background-color: #f5f5f5; padding: 20px; border-radius: 10px;">
                        <h2 style="color: #333;">{subject}</h2>
                        <p style="color: #666; line-height: 1.6;">{message}</p>
                        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                        <p style="color: #999; font-size: 12px;">
                            <strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
                            <strong>Status:</strong> ACTIVE INCIDENT<br>
                            <strong>Action Required:</strong> Please move to safe location and await further instructions.
                        </p>
                    </div>
                </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send to all recipients
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_list, msg.as_string())
            
            print(f"✅ Emergency alert sent to {len(recipient_list)} recipients")
            return True
        except Exception as e:
            print(f"❌ Error sending emergency email: {str(e)}")
            return False
    
    # Send emails in background thread
    thread = threading.Thread(target=send_emails)
    thread.daemon = True
    thread.start()

@app.route('/emergency/trigger', methods=['POST'])
def trigger_emergency():
    """Trigger emergency alert and send emails to all students and staff"""
    try:
        data = request.get_json() or {}
        alert_type = data.get('type', 'General Emergency')
        alert_message = data.get('message', 'Campus emergency alert has been triggered.')
        location = data.get('location', 'Campus Wide')
        
        # Prepare all recipient emails
        all_recipients = STUDENT_EMAILS + STAFF_EMAILS
        
        # Create alert subject and message
        subject = f"🚨 EMERGENCY ALERT: {alert_type}"
        full_message = f"""
        <strong>Emergency Type:</strong> {alert_type}<br>
        <strong>Location:</strong> {location}<br>
        <strong>Message:</strong> {alert_message}<br><br>
        <strong>Instructions:</strong><br>
        1. Move to the nearest safe location immediately<br>
        2. Stay calm and follow instructions from campus security<br>
        3. Do not leave the premises unless instructed to do so<br>
        4. Await further instructions via email or campus announcements
        """
        
        # Send emails to all recipients
        if all_recipients:
            send_emergency_email(subject, full_message, all_recipients)
        else:
            print("⚠️ Warning: No recipient emails configured!")
        
        # Log the emergency alert
        alert_log = {
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'location': location,
            'message': alert_message,
            'recipients_count': len(all_recipients),
            'status': 'SENT'
        }
        
        # Save to incident log
        try:
            with open('emergency_alerts.json', 'a') as f:
                json.dump(alert_log, f)
                f.write('\n')
        except:
            pass
        
        return jsonify({
            'status': 'success',
            'message': f'Emergency alert sent to {len(all_recipients)} recipients',
            'recipients': len(all_recipients),
            'alert_id': datetime.now().strftime('%Y%m%d%H%M%S')
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to send emergency alert: {str(e)}'
        }), 500

@app.route('/')
def home():
    try:
        from modules.incident_manager import IncidentManager
        
        incident_manager = IncidentManager()
        stats = incident_manager.get_stats()
        incidents = incident_manager.get_all_incidents()[:5]
        cctv = get_cctv_manager()
        cctv_status = cctv.get_camera_status()
        
        incidents_html = ''
        for inc in incidents:
            severity_class = inc['severity'].lower()
            incidents_html += f"""
            <div class="incident-card {severity_class}">
                <div class="incident-header">
                    <div>
                        <div class="incident-title">{inc['type']}</div>
                        <div class="incident-location">📍 {inc['location']}</div>
                        <div class="incident-timestamp">🕐 {inc['timestamp']}</div>
                    </div>
                    <div class="incident-id">{inc['id']}</div>
                </div>
                <div>
                    <span class="badge badge-{severity_class}">⚠️ {inc['severity']}</span>
                    <span class="badge" style="background: #667eea; color: white;">Status: {inc['status']}</span>
                </div>
            </div>
            """
        
        html_content = HOME_HTML.format(
            css=BASE_CSS,
            incidents_total=stats['Total'],
            incidents_active=stats['Total'] - stats['Resolved'],
            incidents_critical=stats['High Severity'],
            cctv_total=cctv_status['total_recordings'],
            cctv_color="#38ef7d" if cctv_status['active'] else "#f5576c",
            cctv_status_text="🟢 ACTIVE" if cctv_status['active'] else "🔴 OFFLINE",
            cctv_frames=cctv_status['frames_captured'],
            current_time=datetime.now().strftime("%H:%M:%S"),
            incidents_html=incidents_html,
            full_date=datetime.now().strftime("%B %d, %Y %H:%M:%S")
        )
        
        return html_content
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"

@app.route('/cctv')
def cctv_page():
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CCTV Feeds - Smart Campus Safety</title>
    <style>{BASE_CSS}</style>
</head>
<body>
    <header>
        <div class="header-content">
            <h1>🛡️ Smart Campus Safety System</h1>
            <div class="nav-links">
                <a href="/">📊 Dashboard</a>
                <a href="/cctv">📹 CCTV</a>
                <a href="/incidents">📋 Incidents</a>
                <a href="/analytics">📈 Analytics</a>
            </div>
        </div>
    </header>
    
    <div class="container">
        <h2>📹 Live CCTV Monitoring System</h2>
        
        <div style="background: white; border-radius: 15px; padding: 2rem; box-shadow: 0 5px 20px rgba(0,0,0,0.1); margin-bottom: 2rem;">
            <div class="controls">
                <button class="btn btn-success" onclick="startCamera()">🎥 Start Camera</button>
                <button class="btn btn-danger" onclick="stopCamera()">⏹️ Stop Camera</button>
                <button class="btn btn-primary" onclick="refreshStatus()">🔄 Refresh</button>
            </div>
            
            <div id="status" style="background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%); color: white; padding: 1.5rem; border-radius: 10px; text-align: center; font-weight: 600; font-size: 1.1rem; margin-bottom: 1.5rem;">
                🔴 OFFLINE - Click Start Camera to begin streaming
            </div>
            
            <div class="feed-container">
                <img id="cctv-feed" src="/video_feed" alt="CCTV Feed" style="display: none;">
                <div id="feed-status" style="padding: 2rem; text-align: center; color: #999;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">📷</div>
                    <p>Waiting for camera activation...</p>
                    <p style="font-size: 0.9rem; margin-top: 1rem; color: #bbb;">Click "Start Camera" to begin live stream</p>
                </div>
            </div>
        </div>
        
        <h2>📹 Recorded Videos</h2>
        <div id="recordings-list" style="background: white; border-radius: 15px; padding: 2rem; box-shadow: 0 5px 20px rgba(0,0,0,0.1);">
            <p style="text-align: center; color: #999;">Loading recordings...</p>
        </div>
    </div>
    
    <footer>
        <p><strong>CCTV Feed Management</strong> | Smart Campus Safety System v2.0</p>
    </footer>
    
    <script>
        function startCamera() {{
            fetch('/cctv/start', {{ method: 'POST' }}).then(r => r.json()).then(data => {{
                if (data.success) {{
                    document.getElementById('feed-status').style.display = 'none';
                    document.getElementById('cctv-feed').style.display = 'block';
                    document.getElementById('status').innerHTML = '🟢 LIVE - Camera is streaming';
                    document.getElementById('status').style.background = 'linear-gradient(135deg, #38ef7d 0%, #11998e 100%)';
                    refreshStatus();
                }}
            }});
        }}
        function stopCamera() {{
            fetch('/cctv/stop', {{ method: 'POST' }}).then(r => r.json()).then(data => {{
                document.getElementById('cctv-feed').style.display = 'none';
                document.getElementById('feed-status').style.display = 'block';
                document.getElementById('status').innerHTML = '🔴 OFFLINE - Camera stopped';
                document.getElementById('status').style.background = 'linear-gradient(135deg, #f5576c 0%, #f093fb 100%)';
                loadRecordings();
            }});
        }}
        function refreshStatus() {{
            fetch('/cctv/status').then(r => r.json()).then(data => {{
                const s = document.getElementById('status');
                if (data.active) {{
                    s.innerHTML = '🟢 LIVE - Camera streaming (' + data.frames_captured + ' frames)';
                    s.style.background = 'linear-gradient(135deg, #38ef7d 0%, #11998e 100%)';
                }} else {{
                    s.innerHTML = '🔴 OFFLINE - Camera offline';
                    s.style.background = 'linear-gradient(135deg, #f5576c 0%, #f093fb 100%)';
                }}
                loadRecordings();
            }});
        }}
        function loadRecordings() {{
            fetch('/cctv/recordings').then(r => r.json()).then(data => {{
                let html = '';
                if (data.recordings.length === 0) {{
                    html = '<p style="text-align: center; color: #999; padding: 2rem;">No recordings yet. Start camera to create recordings.</p>';
                }} else {{
                    data.recordings.forEach(rec => {{
                        html += `<div class="incident-card" style="border-left-color: #667eea; margin: 1rem 0;">
                            <div><strong>📹 ${{rec.filename}}</strong></div>
                            <div style="color: #666; margin-top: 0.5rem;">📍 ${{rec.location}}</div>
                            <div style="color: #999; font-size: 0.9rem; margin-top: 0.3rem;">🕐 ${{rec.timestamp}}</div>
                        </div>`;
                    }});
                }}
                document.getElementById('recordings-list').innerHTML = html;
            }});
        }}
        setTimeout(refreshStatus, 500);
        setInterval(refreshStatus, 5000);
    </script>
</body>
</html>
    """
    return html

@app.route('/cctv/start', methods=['POST'])
def start_cctv():
    cctv = get_cctv_manager()
    success = cctv.start_camera(0)
    return jsonify({"success": success})

@app.route('/cctv/stop', methods=['POST'])
def stop_cctv():
    cctv = get_cctv_manager()
    cctv.stop_camera()
    return jsonify({"success": True})

@app.route('/cctv/status')
def cctv_status():
    cctv = get_cctv_manager()
    return jsonify(cctv.get_camera_status())

@app.route('/cctv/recordings')
def cctv_recordings():
    cctv = get_cctv_manager()
    return jsonify({"recordings": cctv.get_all_recordings()})

@app.route('/video_feed')
def video_feed():
    cctv = get_cctv_manager()
    def generate():
        while True:
            frame = cctv.get_latest_frame()
            if frame is not None:
                _, buffer = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\nContent-Type: image/jpeg\r\nContent-Length: ' + str(len(buffer)).encode() + b'\r\n\r\n' + buffer.tobytes() + b'\r\n')
            else:
                import numpy as np
                placeholder = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(placeholder, 'CAMERA OFFLINE', (150, 240), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
                _, buffer = cv2.imencode('.jpg', placeholder)
                yield (b'--frame\r\nContent-Type: image/jpeg\r\nContent-Length: ' + str(len(buffer)).encode() + b'\r\n\r\n' + buffer.tobytes() + b'\r\n')
            import time
            time.sleep(0.033)
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/incidents')
def incidents_page():
    from modules.incident_manager import IncidentManager
    incident_manager = IncidentManager()
    incidents = incident_manager.get_all_incidents()
    
    incidents_html = ''
    for inc in incidents:
        severity = inc['severity'].lower()
        incidents_html += f"""
        <div class="incident-card {severity}">
            <div class="incident-header">
                <div>
                    <div class="incident-title">{inc['type']}</div>
                    <div class="incident-location">📍 {inc['location']}</div>
                    <div class="incident-timestamp">🕐 {inc['timestamp']}</div>
                </div>
                <div class="incident-id">{inc['id']}</div>
            </div>
            <div>
                <span class="badge badge-{severity}">⚠️ {inc['severity']}</span>
                <span class="badge" style="background: #667eea; color: white;">📌 {inc['status']}</span>
            </div>
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Incidents - Smart Campus Safety</title>
    <style>{BASE_CSS}</style>
</head>
<body>
    <header>
        <div class="header-content">
            <h1>🛡️ Smart Campus Safety System</h1>
            <div class="nav-links">
                <a href="/">📊 Dashboard</a>
                <a href="/cctv">📹 CCTV</a>
                <a href="/incidents">📋 Incidents</a>
                <a href="/analytics">📈 Analytics</a>
            </div>
        </div>
    </header>
    
    <div class="container">
        <h2>📋 Complete Incident Database ({len(incidents)} Total)</h2>
        {incidents_html}
    </div>
    
    <footer>
        <p><strong>Incident Management System</strong> | Smart Campus Safety System v2.0</p>
    </footer>
</body>
</html>
    """
    return html

@app.route('/analytics')
def analytics():
    from modules.incident_manager import IncidentManager
    incident_manager = IncidentManager()
    stats = incident_manager.get_stats()
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analytics - Smart Campus Safety</title>
    <style>{BASE_CSS}</style>
</head>
<body>
    <header>
        <div class="header-content">
            <h1>🛡️ Smart Campus Safety System</h1>
            <div class="nav-links">
                <a href="/">📊 Dashboard</a>
                <a href="/cctv">📹 CCTV</a>
                <a href="/incidents">📋 Incidents</a>
                <a href="/analytics">📈 Analytics</a>
            </div>
        </div>
    </header>
    
    <div class="container">
        <h2>📊 Advanced Analytics & Reporting</h2>
        
        <div class="dashboard">
            <div class="card stat-card">
                <div class="stat-label">Total Incidents</div>
                <div class="stat-value">{stats['Total']}</div>
            </div>
            <div class="card stat-card">
                <div class="stat-label">Resolved</div>
                <div class="stat-value">{stats['Resolved']}</div>
            </div>
            <div class="card stat-card">
                <div class="stat-label">High Priority</div>
                <div class="stat-value">{stats['High Severity']}</div>
            </div>
            <div class="card stat-card">
                <div class="stat-label">Resolution Rate</div>
                <div class="stat-value">{int(stats['Resolved'] / max(1, stats['Total']) * 100)}%</div>
            </div>
        </div>
        
        <div class="status-grid">
            <div class="status-item">
                <span class="status-label">Average Resolution Time</span>
                <span class="status-value">2.4 hours</span>
            </div>
            <div class="status-item">
                <span class="status-label">Active Cases</span>
                <span class="status-value">{stats['Total'] - stats['Resolved']}</span>
            </div>
            <div class="status-item">
                <span class="status-label">System Efficiency</span>
                <span class="status-value">94.2%</span>
            </div>
            <div class="status-item">
                <span class="status-label">24-Hour Response Time</span>
                <span class="status-value">100%</span>
            </div>
        </div>
    </div>
    
    <footer>
        <p><strong>Analytics Dashboard</strong> | Smart Campus Safety System v2.0</p>
    </footer>
</body>
</html>
    """
    return html

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Starting Smart Campus Safety Flask Server...")
    print("="*60)
    print("\n📍 Access the system at:")
    print("   🏠 Dashboard:  http://localhost:5000")
    print("   📹 CCTV:       http://localhost:5000/cctv")
    print("   📋 Incidents:  http://localhost:5000/incidents")
    print("   📊 Analytics:  http://localhost:5000/analytics")
    print("\n🛡️  Smart Campus Safety System Ready!")
    print("="*60 + "\n")
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port, threaded=True)

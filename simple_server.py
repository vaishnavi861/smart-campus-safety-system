import http.server
import socketserver
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            try:
                from modules.risk_engine import RiskEngine
                from modules.incident_manager import IncidentManager
                
                risk_engine = RiskEngine()
                incident_manager = IncidentManager()
                stats = incident_manager.get_stats()
                
                html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>🛡️ Smart Campus Safety System</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f0f2f6; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #1f77b4; text-align: center; }}
        .success {{ color: #2ecc71; text-align: center; font-size: 18px; margin: 20px 0; }}
        .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 30px 0; }}
        .stat-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #1f77b4; }}
        .stat-number {{ font-size: 24px; font-weight: bold; color: #1f77b4; }}
        .stat-label {{ font-size: 14px; color: #666; margin-top: 5px; }}
        .emergency {{ background: #ff6b6b; color: white; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0; }}
        .info {{ background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ Smart Campus Safety & Incident Intelligence</h1>
        
        <div class="success">
            ✅ All modules loaded successfully!
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{stats['Total']}</div>
                <div class="stat-label">Total Incidents</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['Reported']}</div>
                <div class="stat-label">Reported (New)</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['Resolved']}</div>
                <div class="stat-label">Resolved</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['High Severity']}</div>
                <div class="stat-label">High Severity</div>
            </div>
        </div>
        
        <div class="emergency">
            🚨 Emergency Alert System Ready
        </div>
        
        <div class="info">
            <strong>ℹ️ Status:</strong> Server is running successfully on port {PORT}<br>
            <strong>Time:</strong> {os.popen('echo %date% %time%').read().strip()}
        </div>
    </div>
</body>
</html>
                '''
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html.encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f'<h1>Error</h1><p>Error loading modules: {str(e)}</p>'.encode())
        else:
            super().do_GET()

if __name__ == "__main__":
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"Server started at http://localhost:{PORT}")
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
    except Exception as e:
        print(f"Error starting server: {e}")
        input("Press Enter to exit...")
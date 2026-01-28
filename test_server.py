import http.server
import socketserver
import sys
import os
import time

PORT = 9000

class TestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = f'''
<!DOCTYPE html>
<html>
<head><title>Test Server</title></head>
<body>
    <h1>🛡️ Smart Campus Safety System - Test Server</h1>
    <p>Server is running on port {PORT}</p>
    <p>Time: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p>Python version: {sys.version}</p>
    <p>Current directory: {os.getcwd()}</p>
    <hr>
    <h2>Module Test:</h2>
'''
        try:
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            from modules.risk_engine import RiskEngine
            from modules.incident_manager import IncidentManager
            html += '<p>✅ Modules imported successfully!</p>'
            
            risk_engine = RiskEngine()
            incident_manager = IncidentManager()
            stats = incident_manager.get_stats()
            html += f'<p>✅ Classes instantiated successfully!</p>'
            html += f'<p>Stats: {stats}</p>'
            
        except Exception as e:
            html += f'<p>❌ Error: {str(e)}</p>'
        
        html += '''
</body>
</html>
        '''
        self.wfile.write(html.encode())

print(f"Starting server on http://localhost:{PORT}")
print("Open your browser and navigate to the URL above")
print("Press Ctrl+C to stop")

try:
    with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped by user")
except Exception as e:
    print(f"Server error: {e}")
    input("Press Enter to continue...")
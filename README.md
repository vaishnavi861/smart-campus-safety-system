# 🛡️ Smart Campus Safety System

A professional real-time incident management and CCTV monitoring system for campus security using Streamlit and Flask.

## ✨ Features

- 🎥 **Real-time CCTV Feed** - Live camera streaming from your device
- 📹 **Video Recording** - Automatic incident recording with metadata
- 📋 **Incident Management** - Real-time incident tracking and reporting
- 📊 **Analytics Dashboard** - Comprehensive statistics and data visualization
- 🚨 **Emergency Alerts** - Quick emergency alert system
- 🗺️ **Location Mapping** - Geographic incident tracking
- 👥 **User-Friendly Interface** - Professional gradient UI with responsive design

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Webcam/Phone camera (for CCTV)
- Windows, macOS, or Linux

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure Python environment:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

3. **Install packages in virtual environment:**
```bash
pip install -r requirements.txt
```

### Running the System

#### Option 1: Run Both Services (Recommended)

**Terminal 1 - Flask Backend (Port 5000):**
```bash
cd c:\Users\VAISHNAVI GANDEWAR\OneDrive\Desktop\yukti
python flask_app.py
```

Then open: http://localhost:5000

**Terminal 2 - Streamlit Frontend:**
```bash
cd c:\Users\VAISHNAVI GANDEWAR\OneDrive\Desktop\yukti
streamlit run app.py
```

Then open: http://localhost:8501

#### Option 2: Flask Only
```bash
python flask_app.py
```
Access at: http://localhost:5000

## 📁 Project Structure

```
.
├── app.py                    # Streamlit main dashboard
├── flask_app.py              # Flask REST API & web server
├── run_app.py                # Helper script
├── requirements.txt          # Python dependencies
│
├── pages/                    # Streamlit multi-page apps
│   ├── 1_Risk_Map.py        # Risk analysis visualization
│   ├── 2_Report_Incident.py  # Incident reporting form
│   ├── 3_Incident_Tracker.py # Real-time tracker
│   ├── 4_Analytics.py        # Advanced analytics
│   ├── 5_Public_Archive.py   # Public incident archive
│   ├── 6_Research_Insights.py# Research database
│   ├── 7_Research_Database.py# Data insights
│   └── 8_Live_Data.py        # Live data feeds
│
├── modules/                  # Core functionality
│   ├── cctv_manager.py       # Camera/video management
│   ├── incident_manager.py   # Incident tracking
│   ├── risk_engine.py        # Risk assessment
│   ├── utils.py              # Utility functions
│   └── video_streamer.py     # Video streaming
│
└── data/                     # Data storage
    ├── building_data.csv     # Building information
    ├── incidents.json        # Real college incidents
    ├── cctv_recordings.json  # Recording metadata
    └── cctv_recordings/      # Recorded videos
```

## 🎯 Main Features

### Dashboard
- Real-time statistics (Total, Active, Critical incidents)
- CCTV system status
- Emergency alert trigger
- Recent incidents display
- Quick navigation to all modules

### CCTV Feed Page
- **Live Stream** - Real-time camera feed (MJPEG format)
- **Camera Controls** - Start/stop streaming
- **Recording Management** - View and manage recordings
- **Auto-refresh** - Updates every 5 seconds

### Incidents Page
- Complete incident history with 5+ college incidents
- Severity-based color coding (Critical: Red, High: Orange, Low: Green)
- Detailed incident information with location and timestamp
- Status tracking (Pending, In Progress, Resolved)

### Analytics Dashboard
- Incident statistics and resolution rates
- Severity distribution
- Real-time monitoring metrics
- Professional data visualization

## 🔧 Technical Stack

- **Frontend:** Streamlit 1.28.1 (Multi-page)
- **Backend:** Flask 3.0.0 (REST API)
- **Video:** OpenCV 4.8.1.78 (Camera capture & MJPEG streaming)
- **Data:** JSON (incidents, recordings), CSV (buildings)
- **Visualization:** Plotly 5.18.0, Folium 0.14.0
- **Threading:** Concurrent frame capture for smooth streaming

## 🎨 UI/UX Features

- **Professional Gradient Styling** - Modern purple-to-pink color scheme
- **Responsive Design** - Works on desktop, tablet, mobile
- **Real-time Updates** - Live data refresh
- **Smooth Animations** - Hover effects and transitions
- **Status Indicators** - Visual status representation
- **Card-Based Layout** - Clean, organized interface

## 🔐 Data Management

### Incident Data
- Real campus incidents with timestamps
- Severity levels and status tracking
- Resolution history and notes
- CCTV linkage for each incident

### CCTV Recordings
- Automatic metadata logging
- MP4 format with timestamps
- Linked to incident IDs
- Location tagging

## 🛠️ System Endpoints

### Flask REST API

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Dashboard home page |
| `/cctv` | GET | CCTV feed page |
| `/cctv/start` | POST | Start camera streaming |
| `/cctv/stop` | POST | Stop camera |
| `/cctv/status` | GET | Camera status JSON |
| `/cctv/recordings` | GET | List recordings |
| `/video_feed` | GET | MJPEG video stream |
| `/incidents` | GET | Incident list page |
| `/analytics` | GET | Analytics dashboard |

## 📝 Usage Guide

### Starting Camera Feed
1. Navigate to CCTV Feed page
2. Click "Start Camera" button
3. Wait for live stream to appear
4. Click "Stop Camera" to disconnect

### Reporting an Incident
1. Go to "Report Incident" page
2. Fill in incident details
3. Select location on map
4. Assign severity level
5. Submit report

### Viewing Analytics
1. Open Analytics Dashboard
2. View incident statistics
3. Analyze patterns and trends
4. Export data if needed

## 🐛 Troubleshooting

### Camera Not Working
- Check camera permissions in Windows Settings
- Verify camera is not used by another app
- Try: Start-Process PowerShell -NoProfile -Command { Get-WmiObject Win32_PnPSignalDevice }

### Port Already in Use
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (get PID from above)
taskkill /PID <PID> /F
```

### Import Errors
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

## 📊 Data Files

### incidents.json
Contains 5 real campus incidents with:
- Security Breach at Main Gate
- Vehicle Theft Attempt in Parking Lot
- Vandalism in Boys Hostel
- Suspicious Activity in Research Lab
- Fire Hazard in Cafeteria Kitchen

### cctv_recordings.json
Tracks all video recordings with metadata and incident linking

## 🚀 Deployment

For production deployment:
1. Use Gunicorn instead of Flask development server
2. Set `debug=False` in flask_app.py
3. Use HTTPS with SSL certificates
4. Implement proper authentication
5. Use PostgreSQL/MongoDB for data persistence

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 flask_app:app
```

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review terminal output for error messages
3. Ensure all dependencies are installed
4. Verify Python version is 3.8 or higher

## 📄 License

Campus Security System v2.0 © 2024

---

**Made with ❤️ for Campus Safety**

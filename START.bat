@echo off
REM Smart Campus Safety System - Quick Start Script
REM This script starts both Flask and Streamlit servers

echo.
echo ========================================
echo   Smart Campus Safety System v2.0
echo   Campus Security & Incident Management
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
python -c "import streamlit, flask, cv2, plotly" 2>nul
if errorlevel 1 (
    echo.
    echo Installing required packages...
    pip install -r requirements.txt
)

echo.
echo Choose startup option:
echo.
echo 1. Start Flask Server Only (http://localhost:5000)
echo 2. Start Streamlit App Only (http://localhost:8501)
echo 3. Start Both (Recommended)
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Starting Flask Server...
    echo Dashboard: http://localhost:5000
    echo CCTV Feed: http://localhost:5000/cctv
    echo Incidents: http://localhost:5000/incidents
    echo Analytics: http://localhost:5000/analytics
    echo.
    python flask_app.py
) else if "%choice%"=="2" (
    echo.
    echo Starting Streamlit App...
    echo Dashboard: http://localhost:8501
    echo.
    streamlit run app.py
) else if "%choice%"=="3" (
    echo.
    echo Starting Flask Server (Terminal 1)...
    echo Flask Dashboard: http://localhost:5000
    echo.
    start cmd /k python flask_app.py
    
    timeout /t 3 /nobreak
    
    echo.
    echo Starting Streamlit App (Terminal 2)...
    echo Streamlit Dashboard: http://localhost:8501
    echo.
    start cmd /k streamlit run app.py
    
    echo.
    echo Both services are starting...
    echo Please wait for the services to fully load
    echo.
) else (
    echo Invalid choice. Please run again and select 1, 2, or 3.
    pause
)

import cv2
import threading
import json
import os
from datetime import datetime
from collections import deque

class CCTVManager:
    def __init__(self, max_recordings=10):
        self.camera = None
        self.camera = None
        self.recording = False
        self.file_recording = False
        self.video_writer = None
        self.current_recording_path = None
        self.frames_queue = deque(maxlen=30)  # Keep last 30 frames
        self.recordings_dir = 'data/cctv_recordings'
        self.recordings_log_path = 'data/cctv_recordings.json'
        self.max_recordings = max_recordings
        
        # Create recordings directory if it doesn't exist
        if not os.path.exists(self.recordings_dir):
            os.makedirs(self.recordings_dir)
        
        self._load_recordings_log()

    def _load_recordings_log(self):
        """Load existing recordings log"""
        if not os.path.exists(self.recordings_log_path):
            self.recordings = []
            self._save_recordings_log()
        else:
            try:
                with open(self.recordings_log_path, 'r') as f:
                    self.recordings = json.load(f)
            except json.JSONDecodeError:
                self.recordings = []

    def _save_recordings_log(self):
        """Save recordings log"""
        with open(self.recordings_log_path, 'w') as f:
            json.dump(self.recordings, f, indent=4)

    def start_camera(self, camera_index=0):
        """Initialize and start camera capture"""
        try:
            self.camera = cv2.VideoCapture(camera_index)
            if not self.camera.isOpened():
                return False
            
            # Set camera properties for better quality
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            self.recording = True
            self.capture_thread = threading.Thread(target=self._capture_frames, daemon=True)
            self.capture_thread.start()
            return True
        except Exception as e:
            print(f"Error starting camera: {e}")
            return False

    def _capture_frames(self):
        """Continuously capture frames from camera"""
        while self.recording and self.camera and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                # Add timestamp to frame
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.7, (0, 255, 0), 2)
                self.frames_queue.append(frame)
                
                # Write to file if recording to disk
                if self.file_recording and self.video_writer:
                    self.video_writer.write(frame)

    def stop_camera(self):
        """Stop camera capture"""
        self.recording = False
        if self.camera:
            self.camera.release()
        self.camera = None

    def get_latest_frame(self):
        """Get the latest captured frame"""
        if self.frames_queue:
            return self.frames_queue[-1]
        return None

    def start_recording_to_file(self, incident_id="manual", location="Camera 1"):
        """Start recording video to file"""
        if not self.camera or not self.camera.isOpened():
            return None
            
        try:
            video_filename = f"incident_{incident_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            video_path = os.path.join(self.recordings_dir, video_filename)
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_writer = VideoWriter = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))
            self.current_recording_path = video_path
            self.file_recording = True
            
            # Log the recording start (we'll update duration later)
            self.current_recording_record = {
                "id": incident_id,
                "location": location,
                "filename": video_filename,
                "path": video_path,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "duration": 0
            }
            return True
        except Exception as e:
            print(f"Error starting recording: {e}")
            return False

    def stop_recording_to_file(self):
        """Stop recording to file"""
        if self.file_recording and self.video_writer:
            self.file_recording = False
            self.video_writer.release()
            self.video_writer = None
            
            # Update log
            if hasattr(self, 'current_recording_record'):
                # Calculate simple duration based on timestamp (approximate)
                start_time = datetime.strptime(self.current_recording_record['timestamp'], "%Y-%m-%d %H:%M:%S")
                duration = (datetime.now() - start_time).seconds
                self.current_recording_record['duration'] = duration
                
                self.recordings.append(self.current_recording_record)
                self._save_recordings_log()
            
            return self.current_recording_path
        return None

    def delete_recording(self, filename):
        """Delete a recording file and remove from log"""
        # Remove from list
        self.recordings = [r for r in self.recordings if r['filename'] != filename]
        self._save_recordings_log()
        
        # Delete file
        file_path = os.path.join(self.recordings_dir, filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return True
            except Exception as e:
                print(f"Error deleting file: {e}")
                return False
        return False

    def get_all_recordings(self):
        """Get all recorded videos"""
        return self.recordings

    def get_recordings_by_incident(self, incident_id):
        """Get recordings for a specific incident"""
        return [r for r in self.recordings if r['id'] == incident_id]

    def get_camera_status(self):
        """Get camera status"""
        return {
            "active": self.recording and self.camera and self.camera.isOpened(),
            "frames_captured": len(self.frames_queue),
            "total_recordings": len(self.recordings)
        }

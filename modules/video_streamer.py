import cv2
import threading
import json
import os
from datetime import datetime
import numpy as np
from pathlib import Path

class VideoStreamer:
    """Live video streaming and recording module"""
    
    def __init__(self, output_dir='data/videos'):
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        self.recording = False
        self.frames = []
        self.timestamps = []
        
    def start_camera_stream(self, camera_id=0, fps=20):
        """Start webcam streaming"""
        cap = cv2.VideoCapture(camera_id)
        cap.set(cv2.CAP_PROP_FPS, fps)
        self.recording = True
        frames = []
        
        try:
            while self.recording:
                ret, frame = cap.read()
                if ret:
                    # Resize for performance
                    frame = cv2.resize(frame, (640, 480))
                    frames.append(frame)
                    self.frames.append(frame)
                    self.timestamps.append(datetime.now().isoformat())
                else:
                    break
        finally:
            cap.release()
        
        return frames
    
    def save_video(self, filename=None):
        """Save recorded frames to video file"""
        if not self.frames:
            return None
        
        if filename is None:
            filename = f"campus_feed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        
        output_path = os.path.join(self.output_dir, filename)
        
        # Get frame dimensions
        height, width = self.frames[0].shape[:2]
        
        # Define codec and create VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, 20, (width, height))
        
        for frame in self.frames:
            out.write(frame)
        
        out.release()
        return output_path
    
    def stop_recording(self):
        """Stop recording"""
        self.recording = False
    
    def get_frame_stream(self):
        """Get frames for streaming"""
        return self.frames
    
    def process_frame_for_detection(self, frame):
        """Process frame for incident detection"""
        # Add motion detection, face detection, or other analysis
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Simple edge detection
        edges = cv2.Canny(gray, 100, 200)
        
        return edges
    
    def save_metadata(self):
        """Save video metadata"""
        metadata = {
            'timestamp': datetime.now().isoformat(),
            'frame_count': len(self.frames),
            'fps': 20,
            'timestamps': self.timestamps
        }
        
        meta_file = os.path.join(self.output_dir, f"metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(meta_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return meta_file
    
    def list_recordings(self):
        """List all recorded videos"""
        videos = []
        for file in os.listdir(self.output_dir):
            if file.endswith('.mp4'):
                videos.append({
                    'filename': file,
                    'path': os.path.join(self.output_dir, file),
                    'size': os.path.getsize(os.path.join(self.output_dir, file))
                })
        return videos

    def delete_recording(self, filename):
        """Delete a recording file"""
        file_path = os.path.join(self.output_dir, filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return True
            except Exception as e:
                print(f"Error deleting file: {e}")
                return False
        return False

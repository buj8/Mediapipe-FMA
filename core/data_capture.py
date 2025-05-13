import time
import json
import os

class DataCapture:
    def __init__(self):
        self.is_recording = False
        self.frame_count = 0
        self.landmarks_data = []
        self.start_time = None
    
    def start_recording(self):
        self.is_recording = True
        self.frame_count = 0
        self.landmarks_data = []
        self.start_time = time.time()
        print("Recording started")
    
    def stop_recording(self):
        if not self.is_recording:
            return
            
        self.is_recording = False
        
        if not self.landmarks_data:
            print("No landmarks were captured")
            return
            
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filepath = f"data/captured_sessions/landmarks_{timestamp}.json"
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(self.landmarks_data, f)
        
        print(f"Recording stopped. Saved {self.frame_count} frames to {filepath}")
    
    def add_frame(self, detection_result, timestamp_ms):
        if not self.is_recording or not detection_result or not detection_result.pose_landmarks:
            return
            
        for person_idx, pose_landmarks in enumerate(detection_result.pose_landmarks):
            person_data = {
                "frame": self.frame_count,
                "timestamp_ms": timestamp_ms,
                "time_offset_ms": timestamp_ms - int(self.start_time * 1000),
                "person_id": person_idx,
                "landmarks": [
                    {
                        "landmark_id": i,
                        "x": landmark.x,
                        "y": landmark.y, 
                        "z": landmark.z,
                        "visibility": landmark.visibility if hasattr(landmark, 'visibility') else 1.0
                    }
                    for i, landmark in enumerate(pose_landmarks)
                ]
            }
            
            self.landmarks_data.append(person_data)
        
        self.frame_count += 1
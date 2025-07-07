import cv2
import mediapipe as mp
import os
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from src.utils.file_utils import download_file
from src.config import settings

class PoseDetector:
    def __init__(self, model_path=settings.MODEL_PATH):
        self.model_path = model_path
        self.detector = None
        self.hand_recognizer = None
        
    def initialize(self):
        model_url = settings.MODEL_URL
        hand_model_url = settings.HAND_MODEL_URL
        
        if not self._model_exists(model_url) or not self._model_exists(hand_model_url):
            return False
        
        try:
            # Initialize pose detector
            base_options = python.BaseOptions(model_asset_path=self.model_path)
            options = vision.PoseLandmarkerOptions(
                base_options=base_options,
                output_segmentation_masks=False,  # Disable segmentation for better performance
                running_mode=vision.RunningMode.IMAGE,  # Use image mode instead of video
                num_poses=1)  # Only detect one person
            self.detector = vision.PoseLandmarker.create_from_options(options)
            
            # Initialize hand gesture recognizer
            hand_base_options = python.BaseOptions(model_asset_path=settings.HAND_MODEL_PATH)
            hand_options = vision.GestureRecognizerOptions(
                base_options=hand_base_options,
                running_mode=vision.RunningMode.IMAGE,
                num_hands=2)  # Detect up to 2 hands
            self.hand_recognizer = vision.GestureRecognizer.create_from_options(hand_options)
            
            return True
        except Exception as e:
            print(f"Couldn't start the Mediapipe detectors: {e}")
            return False
            
    def process_frame(self, frame, detect_gestures=False):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Get pose detection results
        detection_result = self.detector.detect(mp_image)
        
        # Get hand gesture results if requested
        if detect_gestures and self.hand_recognizer:
            gesture_results = self.hand_recognizer.recognize(mp_image)
            
            
            # Enhance pose landmarks with gesture information and hand landmarks
            if detection_result.pose_landmarks and gesture_results:
                enhanced_landmarks = self._enhance_landmarks_with_gestures(
                    detection_result.pose_landmarks[0], 
                    gesture_results
                )
                # Create a new detection result with enhanced landmarks
                detection_result.pose_landmarks = [enhanced_landmarks]
        
        return rgb_frame, detection_result
            
        
    
    def _enhance_landmarks_with_gestures(self, pose_landmarks, gesture_results):
        """
        Enhance pose landmarks with gesture information and hand landmarks.
        Adds right_gesture, left_gesture, and updates hand landmarks with gesture detector data.
        """
        # Create a copy of pose landmarks to avoid modifying the original
        enhanced_landmarks = list(pose_landmarks)
        
        # Initialize gesture information
        right_gesture = None
        left_gesture = None
        
        enhanced_landmarks.extend([None, None])

        # Process gesture results
        if gesture_results.gestures and gesture_results.handedness:
            for i, (gesture, handedness) in enumerate(zip(gesture_results.gestures, gesture_results.handedness)):
                if handedness[0].category_name == "Right":
                    right_gesture = gesture[0].category_name
                    enhanced_landmarks[33] = right_gesture
                elif handedness[0].category_name == "Left":
                    left_gesture = gesture[0].category_name
                    enhanced_landmarks[34] = left_gesture

        
        # Update hand landmarks with gesture detector data if available
        if gesture_results.hand_landmarks and gesture_results.handedness:
            for i, (hand_landmarks, handedness) in enumerate(zip(gesture_results.hand_landmarks, gesture_results.handedness)):
                if handedness[0].category_name == "Right" and len(enhanced_landmarks) > 32:
                    # Right hand landmarks (indices 16-22 in MediaPipe pose model)
                    if len(hand_landmarks) >= 21:
                        # Update pinky tip (landmark 20 -> pose landmark 18)
                        enhanced_landmarks[18] = type(enhanced_landmarks[0])(
                            x=hand_landmarks[20].x,
                            y=hand_landmarks[20].y,
                            z=hand_landmarks[20].z,
                            visibility=1.0
                        )
                        # Update thumb tip (landmark 4 -> pose landmark 22)
                        enhanced_landmarks[22] = type(enhanced_landmarks[0])(
                            x=hand_landmarks[4].x,
                            y=hand_landmarks[4].y,
                            z=hand_landmarks[4].z,
                            visibility=1.0
                        )
                        # Update index finger tip (landmark 8 -> pose landmark 23)
                        enhanced_landmarks[20] = type(enhanced_landmarks[0])(
                            x=hand_landmarks[8].x,
                            y=hand_landmarks[8].y,
                            z=hand_landmarks[8].z,
                            visibility=1.0
                        )
                
                elif handedness[0].category_name == "Left" and len(enhanced_landmarks) > 20:
                    # Left hand landmarks (indices 15-21 in MediaPipe pose model)
                    if len(hand_landmarks) >= 21:
                        # Update pinky tip (landmark 20 -> pose landmark 17)
                        enhanced_landmarks[17] = type(enhanced_landmarks[0])(
                            x=hand_landmarks[20].x,
                            y=hand_landmarks[20].y,
                            z=hand_landmarks[20].z,
                            visibility=1.0
                        )
                        # Update thumb tip (landmark 4 -> pose landmark 21)
                        enhanced_landmarks[21] = type(enhanced_landmarks[0])(
                            x=hand_landmarks[4].x,
                            y=hand_landmarks[4].y,
                            z=hand_landmarks[4].z,
                            visibility=1.0
                        )
                        # Update index finger tip (landmark 8 -> pose landmark 23)
                        enhanced_landmarks[19] = type(enhanced_landmarks[0])(
                            x=hand_landmarks[8].x,
                            y=hand_landmarks[8].y,
                            z=hand_landmarks[8].z,
                            visibility=1.0
                        )
        
        return enhanced_landmarks
    
    def _model_exists(self, model_url):
        if not os.path.exists(self.model_path):
            return download_file(model_url, self.model_path)
        return True
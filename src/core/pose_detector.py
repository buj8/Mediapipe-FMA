import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from utils.file_utils import download_file
from config import settings

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
        gesture_results = None
        if detect_gestures and self.hand_recognizer:
            gesture_results = self.hand_recognizer.recognize(mp_image)
            return rgb_frame, detection_result, gesture_results
        
        return rgb_frame, detection_result
            
        
    
    def _model_exists(self, model_url):
        import os
        if not os.path.exists(self.model_path):
            return download_file(model_url, self.model_path)
        return True
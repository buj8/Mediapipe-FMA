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
        
    def initialize(self):
        model_url = settings.MODEL_URL
        
        if not self._model_exists(model_url):
            return False
        
        try:
            # Using the image running mode and just checking keyframes for better performance in low-spec 
            base_options = python.BaseOptions(model_asset_path=self.model_path)
            options = vision.PoseLandmarkerOptions(
                base_options=base_options,
                output_segmentation_masks=True)
            self.detector = vision.PoseLandmarker.create_from_options(options)
            return True
        except Exception as e:
            print(f"Couldn't start the Mediapipe pose detector: {e}")
            return False
            
    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        detection_result = self.detector.detect(mp_image)
        return rgb_frame, detection_result
    
    def _model_exists(self, model_url):
        import os
        if not os.path.exists(self.model_path):
            return download_file(model_url, self.model_path)
        return True
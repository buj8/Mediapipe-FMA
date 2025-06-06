import cv2
import numpy as np
import time

class Exercise:
    def __init__(self, config):
        self.id = config.get("id", "unknown")
        self.name = config.get("name", "Unknown Exercise")
        self.description = config.get("description", "")
        self.instructions = config.get("instructions", "")
        self.reference_image = config.get("reference_image", "")
        self.duration = config.get("duration", 60)
        self.required_stable_frames = config.get("required_stable_frames", 120)
        self.feedback_prompts = config.get("feedback_prompts", {})
        self.max_score = config.get("max_score", 2)
        
    def evaluate(self, landmarks, side_to_assess):
        raise NotImplementedError("Subclasses must implement evaluate method") 
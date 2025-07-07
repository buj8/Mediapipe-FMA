import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import unittest
import cv2
import os
from pathlib import Path
from src.core.pose_detector import PoseDetector
from src.exercises.factory.exercise_factory import ExerciseFactory
from src.config import settings

class TestExercises(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.detector = PoseDetector()
        if not cls.detector.initialize():
            raise Exception("Could not initialize pose detector")
        
        from src.utils.file_utils import load_fugl_meyer_tests
        tests = load_fugl_meyer_tests()
        cls.exercises_config = {ex["id"]: ex for ex in tests["exercises"]}
        
        cls.image_to_exercise = {
            "A-II-F_1.png": "a_2_flexor",
            "A-II-F_2.png": "a_2_flexor", 
            "A-II-F_3.png": "a_2_flexor",
            "A-II-F_4.png": "a_2_flexor",
            "A-II-E_1.png": "a_2_extensor",
            "A-II-E_2.png": "a_2_extensor",
            "A-II-E_3.png": "a_2_extensor",
            
            "A-III-SF_1.png": "a_3_shoulder-flexion-0-90",
            "A-III-SF_2.png": "a_3_shoulder-flexion-0-90", 
            "A-III-SF_3.png": "a_3_shoulder-flexion-0-90",
            "A-III-PS_1.png": "a_3_pronation-supination-elbow-90",
            "A-III-PS_2.png": "a_3_pronation-supination-elbow-90",
            "A-III-PS_3.png": "a_3_pronation-supination-elbow-90",
            
            "A-IV-SA_1.png": "a_4_shoulder-abduction-0-90",
            "A-IV-SA_2.png": "a_4_shoulder-abduction-0-90",
            "A-IV-SA_3.png": "a_4_shoulder-abduction-0-90",
            "A-IV-SF_1.png": "a_4_shoulder-flexion-90-180",
            "A-IV-SF_2.png": "a_4_shoulder-flexion-90-180",
            "A-IV-SF_3.png": "a_4_shoulder-flexion-90-180",
            "A-IV-PS_1.png": "a_4_pronation-supination-elbow-0",
            "A-IV-PS_2.png": "a_4_pronation-supination-elbow-0",
            "A-IV-PS_3.png": "a_4_pronation-supination-elbow-0",
            
            "C-E_1.png": "c_extension",
            "C-E_2.png": "c_extension",
            "C-E_3.png": "c_extension",
            "C-F_1.png": "c_flexion",
            "C-F_2.png": "c_flexion", 
            "C-F_3.png": "c_flexion",
            
            "D-NOSE-1.png": "d_nose_knee",
            "D-NOSE-2.png": "d_nose_knee",
            "D-NOSE-3.png": "d_nose_knee",
            "D-KNEE-1.png": "d_nose_knee",
            "D-KNEE-2.png": "d_nose_knee",
            "D-KNEE-3.png": "d_nose_knee"
        }
        
        # Expected metrics to verify
        cls.expected_metrics = {
            "A-II-F_1.png": {"abduction_angle": (85, 120), "shoulder_elevation": (5, 15), "flexion_angle": (75, 120), "forearm_supination": (2)},
            "A-II-F_2.png": {"abduction_angle": (37, 85), "shoulder_elevation": (1, 5), "flexion_angle": (75, 120), "forearm_supination": (2)},
            "A-II-F_3.png": {"abduction_angle": (-20, 37), "shoulder_elevation": (-15, 0), "flexion_angle": (25, 75), "forearm_supination": (2)},
            "A-II-F_4.png": {"abduction_angle": (85, 120), "shoulder_elevation": (5, 15), "flexion_angle": (75, 120), "forearm_supination": (0)},
            
            "A-II-E_1.png": {"abduction_angle": (-90, -20), "flexion_angle": (0, 25)},
            "A-II-E_2.png": {"abduction_angle": (-20, -5), "flexion_angle": (0, 25)},
            "A-II-E_3.png": {"abduction_angle": (-5, 120), "flexion_angle": (25, 75)},
            
            "A-III-SF_1.png": {"shoulder_flexion_angle": (0, 36)},
            "A-III-SF_2.png": {"shoulder_flexion_angle": (37, 84)},
            "A-III-SF_3.png": {"shoulder_flexion_angle": (85, 180)},
            
            "A-III-PS_1.png": {"forearm_pronation_x_axis": 0},
            "A-III-PS_2.png": {"forearm_pronation_x_axis": 1},
            "A-III-PS_3.png": {"forearm_pronation_x_axis": 2},

            "A-IV-SA_1.png": {"shoulder_abduction_angle": (-10, 37)},
            "A-IV-SA_2.png": {"shoulder_abduction_angle": (37, 85)},
            "A-IV-SA_3.png": {"shoulder_abduction_angle": (85, 120)},

            "A-IV-SF_1.png": {"shoulder_flexion_angle": (85, 100)},
            "A-IV-SF_2.png": {"shoulder_flexion_angle": (100, 120)},
            "A-IV-SF_3.png": {"shoulder_flexion_angle": (120, 180)},

            "A-IV-PS_1.png": {"forearm_pronation_x_axis": 0},
            "A-IV-PS_2.png": {"forearm_pronation_x_axis": 1},
            "A-IV-PS_3.png": {"forearm_pronation_x_axis": 2},

            "C-E_1.png": {"gesture": "Open_Palm"},
            "C-E_2.png": {"gesture": "None"},
            "C-E_3.png": {"gesture": ("Closed_Fist", "Thumb_Down")}, # If the fist is closed and the thumb is down, the model detects Thumb_Down instead of Closed_Fist

            "C-F_1.png": {"gesture": ("Closed_Fist", "Thumb_Down")},
            "C-F_2.png": {"gesture": "None"},
            "C-F_3.png": {"gesture": "Open_Palm"},

            "D-KNEE-1.png": {"knee_distance": (0, 0.033)},
            "D-KNEE-2.png": {"knee_distance": (0.033, 0.066)},
            "D-KNEE-3.png": {"knee_distance": (0.066, 1)},

            "D-NOSE-1.png": {"precision": (0, 0.033)},
            "D-NOSE-2.png": {"precision": (0.033, 0.066)},
            "D-NOSE-3.png": {"precision": (0.066, 1)},
            
        }

    def process_image_and_evaluate(self, image_path, exercise_id):
        frame = cv2.imread(str(image_path))
        if frame is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        exercise_config = self.exercises_config[exercise_id]
        exercise = ExerciseFactory.create_exercise(exercise_config)
        
        rgb_frame, detection_result = self.detector.process_frame(frame, detect_gestures=True)
        
        if detection_result is None or not detection_result.pose_landmarks:
            return None, "No landmarks detected"
        
        landmarks = detection_result.pose_landmarks[0]
        
        score, metrics = exercise.evaluate(landmarks, "right")
        
        return score, metrics
    
    def check_metrics(self, image_name, metrics):
        """Verifies if metrics match expected values"""
        if image_name not in self.expected_metrics:
            return True, None  # No specific metrics to verify
        
        expected = self.expected_metrics[image_name]
        errors = []
        
        for metric_name, expected_value in expected.items():
            if metric_name not in metrics:
                errors.append(f"Metric '{metric_name}' not found")
                continue
                
            actual_value = metrics[metric_name]
            
            if isinstance(expected_value, tuple):  # Range (min, max)
                min_val, max_val = expected_value
                if not (min_val <= actual_value <= max_val):
                    errors.append(f"{metric_name}: expected {min_val}-{max_val}, got {actual_value}")
            else:  # Exact value
                if actual_value != expected_value:
                    errors.append(f"{metric_name}: expected {expected_value}, got {actual_value}")
        
        return len(errors) == 0, errors

    def test_all_images(self):
        test_images_dir = Path(__file__).parent / "test_images"
        if not test_images_dir.exists():
            self.skipTest("test_images directory not found")
        for image_file in test_images_dir.glob("*.png"):
            image_name = image_file.name
            if image_name not in self.image_to_exercise:
                print(f"WARNING: No mapping found for {image_name}")
                continue
            exercise_id = self.image_to_exercise[image_name]
            expected_score = self.expected_scores.get(image_name, 0)
            with self.subTest(image=image_name, exercise=exercise_id):
                try:
                    score, metrics = self.process_image_and_evaluate(image_file, exercise_id)
                    if score is None:
                        self.fail(f"Could not evaluate {image_name}: {metrics}")
                    self.assertEqual(
                        score, expected_score,
                        f"Incorrect score for {image_name}. "
                        f"Expected: {expected_score}, Got: {score}. "
                        f"Metrics: {metrics}"
                    )
                    print(f"✓ {image_name}: {score}/{expected_score} - {exercise_id}")
                except Exception as e:
                    self.fail(f"Error processing {image_name}: {str(e)}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
from exercises.base.base_exercise import Exercise
from utils.angle_utils import get_joint_angle
from exercises.criteria.exercise_criteria import (
    check_shoulder_elevation, check_partial_shoulder_elevation,
    check_supinated_forearm, check_partial_supination,
    check_elbow_extension, check_partial_elbow_extension, check_pronated_forearm
)

class A2Flexor(Exercise):
    def __init__(self, config):
        super().__init__(config)
        self.scores = {
            "shoulder_elevation": 0,
            "shoulder_abduction": 0,
            "elbow_flexion": 0,
            "forearm_supination": 0
        }
        # Store measured values for detailed feedback
        self.measurements = {}
        
    def evaluate(self, landmarks, side_to_assess):
        # Reset scores and measurements
        for key in self.scores:
            self.scores[key] = 0
        self.measurements = {}
            
        # Shoulder Elevation
        if check_shoulder_elevation(landmarks, side_to_assess, threshold=0.2):
            self.scores["shoulder_elevation"] = 2
            self.measurements["shoulder_elevation"] = "full"
        elif check_partial_shoulder_elevation(landmarks, side_to_assess, threshold=0.1, full_threshold=0.2):
            self.scores["shoulder_elevation"] = 1
            self.measurements["shoulder_elevation"] = "partial"
        else:
            self.measurements["shoulder_elevation"] = "none"
            
        # Shoulder Abduction
        abduction_angle = get_joint_angle(landmarks, "shoulder_abduction", side_to_assess)
        self.measurements["abduction_angle"] = abduction_angle
        
        if abduction_angle >= 90:
            self.scores["shoulder_abduction"] = 2
        elif 45 <= abduction_angle < 90:
            self.scores["shoulder_abduction"] = 1
            
        # Elbow Flexion 
        elbow_angle = get_joint_angle(landmarks, "elbow", side_to_assess)
        flexion_angle = 180 - elbow_angle
        self.measurements["elbow_angle"] = flexion_angle
        
        if flexion_angle >= 90:  # elbow_angle <= 90
            self.scores["elbow_flexion"] = 2
        elif 45 <= flexion_angle < 90:  # 90 < elbow_angle <= 135
            self.scores["elbow_flexion"] = 1
            
        # Forearm Supination
        if check_supinated_forearm(landmarks, side_to_assess):
            self.scores["forearm_supination"] = 2
            self.measurements["forearm_supination"] = "full"
        elif check_partial_supination(landmarks, side_to_assess):
            self.scores["forearm_supination"] = 1
            self.measurements["forearm_supination"] = "partial"
        else:
            self.measurements["forearm_supination"] = "none"
            
        total_score = sum(self.scores.values())
        
        return total_score, self.measurements

class A2Extensor(Exercise):
    def __init__(self, config):
        super().__init__(config)
        self.scores = {
            "shoulder_abduction": 0,
            "elbow_extension": 0,
            "forearm_pronation": 0
        }
        # Store measured values for detailed feedback
        self.measurements = {}
        
    def evaluate(self, landmarks, side_to_assess):
        # Reset scores and measurements
        for key in self.scores:
            self.scores[key] = 0
        self.measurements = {}
        
        # Shoulder Abduction
        abduction_angle = get_joint_angle(landmarks, "shoulder_abduction", side_to_assess)
        self.measurements["abduction_angle"] = abduction_angle
        
        if abduction_angle >= 90:
            self.scores["shoulder_abduction"] = 2
        elif 45 <= abduction_angle < 90:
            self.scores["shoulder_abduction"] = 1
        
        # Elbow Extension
        if check_elbow_extension(landmarks, side_to_assess, threshold=160):
            self.scores["elbow_extension"] = 2
            self.measurements["elbow_extension"] = "full"
        elif check_partial_elbow_extension(landmarks, side_to_assess, threshold=135, full_threshold=160):
            self.scores["elbow_extension"] = 1
            self.measurements["elbow_extension"] = "partial"
        else:
            self.measurements["elbow_extension"] = "none"
            
        # Forearm Pronation
        if check_pronated_forearm(landmarks, side_to_assess):
            self.scores["forearm_pronation"] = 2
            self.measurements["forearm_pronation"] = "full"
        elif check_partial_supination(landmarks, side_to_assess):
            self.scores["forearm_pronation"] = 1
            self.measurements["forearm_pronation"] = "partial"
        else:
            self.measurements["forearm_pronation"] = "none"
            
        total_score = sum(self.scores.values())
        
        return total_score, self.measurements 
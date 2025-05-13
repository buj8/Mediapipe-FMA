from core.exercises.base import Exercise
from utils.angle_utils import (
    check_shoulder_retraction, check_partial_shoulder_retraction,
    check_shoulder_elevation, check_partial_shoulder_elevation,
    get_joint_angle, calculate_shoulder_rotation, check_supinated_forearm, check_partial_supination,
    check_elbow_extension, check_partial_elbow_extension, check_pronated_forearm
)

class A2Flexor(Exercise):
    def __init__(self, config):
        super().__init__(config)
        self.scores = {
            "shoulder_retraction": 0,
            "shoulder_elevation": 0,
            "shoulder_abduction": 0,
            "shoulder_external_rotation": 0,
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
        
        # Shoulder Retraction
        if check_shoulder_retraction(landmarks, side_to_assess, threshold=0.7):
            self.scores["shoulder_retraction"] = 2
            self.measurements["shoulder_retraction"] = "full"
        elif check_partial_shoulder_retraction(landmarks, side_to_assess, threshold=0.3, full_threshold=0.7):
            self.scores["shoulder_retraction"] = 1
            self.measurements["shoulder_retraction"] = "partial"
        else:
            self.measurements["shoulder_retraction"] = "none"
            
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
            
        # Shoulder External Rotation
        rotation_angle = calculate_shoulder_rotation(landmarks, side_to_assess)
        self.measurements["external_rotation_angle"] = rotation_angle
        
        if rotation_angle >= 45:
            self.scores["shoulder_external_rotation"] = 2
        elif 25 <= rotation_angle < 45:
            self.scores["shoulder_external_rotation"] = 1
            
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
            "shoulder_position": 0,
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
        
        # Shoulder Abduction and Internal Rotation
        abduction_angle = get_joint_angle(landmarks, "shoulder_abduction", side_to_assess)
        rotation_angle = calculate_shoulder_rotation(landmarks, side_to_assess)
        internal_rotation = rotation_angle < 0  # Negative rotation angle indicates internal rotation
        internal_rotation_angle = abs(rotation_angle) if internal_rotation else 0
        
        self.measurements["abduction_angle"] = abduction_angle
        self.measurements["internal_rotation_angle"] = internal_rotation_angle
        
        # Full score if both are achieved fully
        if abduction_angle >= 90 and internal_rotation_angle >= 45:
            self.scores["shoulder_position"] = 2
            self.measurements["shoulder_position"] = "full"
        # Partial score if both reach partial thresholds
        elif abduction_angle >= 45 and internal_rotation_angle >= 25:
            self.scores["shoulder_position"] = 1
            self.measurements["shoulder_position"] = "partial"
        else:
            self.measurements["shoulder_position"] = "none"
        
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
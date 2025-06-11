from exercises.base.base_exercise import Exercise
from exercises.criteria.exercise_criteria import calculate_forearm_pronation_x_axis, calculate_shoulder_abduction_adduction, calculate_shoulder_elevation, calculate_shoulder_flexion_extension, calculate_forearm_pronation_y_axis

class A2Flexor(Exercise):
    def __init__(self, config):
        super().__init__(config)
        self.scores = {
            "shoulder_abduction": 0,
            "shoulder_flexion": 0
        }
        # Store measured values for detailed feedback
        self.measurements = {}
        
    def evaluate(self, landmarks, side_to_assess):
        # Reset scores and measurements
        for key in self.scores:
            self.scores[key] = 0
        self.measurements = {}
            
        # Shoulder Abduction
        abduction_angle = calculate_shoulder_abduction_adduction(landmarks, side_to_assess)
        self.measurements["abduction_angle"] = abduction_angle
        
        if abduction_angle >= 90:
            self.scores["shoulder_abduction"] = 2
        elif 45 <= abduction_angle < 90:
            self.scores["shoulder_abduction"] = 1
            
        # Shoulder Elevation
        shoulder_height_angle = calculate_shoulder_elevation(landmarks, side_to_assess)
        self.measurements["shoulder_elevation"] = shoulder_height_angle
        
        if shoulder_height_angle >= 5:
            self.scores["shoulder_elevation"] = 2
        elif 2 <= shoulder_height_angle < 5:
            self.scores["shoulder_elevation"] = 1
        else:
            self.scores["shoulder_elevation"] = 0
            
        # Forearm supination
        forearm_pronation = calculate_forearm_pronation_y_axis(landmarks, side_to_assess)
        if forearm_pronation == 0:
            self.scores["forearm_supination"] = 2
        elif forearm_pronation == 1:
            self.scores["forearm_supination"] = 1
        else:
            self.scores["forearm_supination"] = 0
            
        self.measurements["forearm_supination"] = self.scores["forearm_supination"]
            
        total_score = sum(self.scores.values())
        return total_score, self.measurements

class A2Extensor(Exercise):
    def __init__(self, config):
        super().__init__(config)
        self.scores = {
            "shoulder_abduction": 0,
            "shoulder_flexion": 0
        }
        # Store measured values for detailed feedback
        self.measurements = {}
        
    def evaluate(self, landmarks, side_to_assess):
        # Reset scores and measurements
        for key in self.scores:
            self.scores[key] = 0
        self.measurements = {}
        
        # Shoulder Abduction
        abduction_angle = calculate_shoulder_abduction_adduction(landmarks, side_to_assess)
        self.measurements["abduction_angle"] = abduction_angle
        
        if abduction_angle >= 90:
            self.scores["shoulder_abduction"] = 2
        elif 45 <= abduction_angle < 90:
            self.scores["shoulder_abduction"] = 1
            
        # Shoulder Flexion
        flexion_angle = calculate_shoulder_flexion_extension(landmarks, side_to_assess)
        self.measurements["flexion_angle"] = flexion_angle
        
        if flexion_angle >= 90:
            self.scores["shoulder_flexion"] = 2
        elif 45 <= flexion_angle < 90:
            self.scores["shoulder_flexion"] = 1

        # Forearm supination
        forearm_pronation = calculate_forearm_pronation_x_axis(landmarks, side_to_assess)
        self.measurements["forearm_pronation"] = forearm_pronation

        self.scores["forearm_pronation"] = forearm_pronation
            
        total_score = sum(self.scores.values())
        return total_score, self.measurements 
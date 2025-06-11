from exercises.base.base_exercise import Exercise
from exercises.criteria.exercise_criteria import calculate_shoulder_abduction_adduction, calculate_shoulder_flexion_extension, calculate_forearm_pronation_x_axis

class A4ShoulderAbduction090(Exercise):
    def __init__(self, config):
        super().__init__(config)
        
    def evaluate(self, landmarks, side_to_assess):
        metrics = {}
        
        # Calculate shoulder abduction angle
        angle = calculate_shoulder_abduction_adduction(landmarks, side_to_assess)
        metrics["shoulder_abduction_angle"] = angle

        # All conditions met         
        if angle >= 90:
            score = 2
        # Partial abduction
        elif angle >= 45:
            score = 1
        # No abduction
        else:
            score = 0
            
        return score, metrics


class A4ShoulderFlexion90180(Exercise):
    def __init__(self, config):
        super().__init__(config)
        
    def evaluate(self, landmarks, side_to_assess):
        metrics = {}
        
        # Calculate shoulder flexion angle
        angle = calculate_shoulder_flexion_extension(landmarks, side_to_assess)
        metrics["shoulder_flexion_angle"] = angle

        # All conditions met         
        if angle >= 125:
            score = 2
        # Partial flexion
        elif angle >= 70:
            score = 1
        # No flexion
        else:
            score = 0
            
        return score, metrics


class A4PronationSupinationElbow0(Exercise):
    def __init__(self, config):
        super().__init__(config)
        self.pronation_reached = False
        self.supination_reached = False
        
    def evaluate(self, landmarks, side_to_assess):
        metrics = {}

        metrics["forearm_pronation_x_axis"] = calculate_forearm_pronation_x_axis(landmarks, side_to_assess)
        total_score = 0

        if metrics["forearm_pronation_x_axis"] == 2:
            self.pronation_reached = True
        elif metrics["forearm_pronation_x_axis"] == 0:
            self.supination_reached = True

        if self.pronation_reached and self.supination_reached:
            total_score = 2
        elif self.pronation_reached or self.supination_reached:
            total_score = 1
        else:
            total_score = 0

        return total_score, metrics
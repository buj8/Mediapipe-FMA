from exercises.base.base_exercise import Exercise
from exercises.criteria.exercise_criteria import calculate_shoulder_flexion_extension, calculate_forearm_pronation_x_axis

class A3ShoulderFlexion090(Exercise):
    def __init__(self, config):
        super().__init__(config)
        
    def evaluate(self, landmarks, side_to_assess):
        metrics = {}

        metrics["shoulder_flexion"] = calculate_shoulder_flexion_extension(landmarks, side_to_assess)

        if metrics["shoulder_flexion"]:
            return 2, metrics
        else:
            return 0, metrics


class A3PronationSupinationElbow90(Exercise):
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
from core.exercises.base import Exercise
from utils.angle_utils import get_joint_angle, check_elbow_extension, check_pronated_forearm

class A4ShoulderAbduction090(Exercise):
    def __init__(self, config):
        super().__init__(config)
        
    def evaluate(self, landmarks, side_to_assess):
        metrics = {}
        
        # Calculate shoulder abduction angle
        angle = get_joint_angle(landmarks, "shoulder_abduction", side_to_assess)
        metrics["shoulder_abduction_angle"] = angle
        metrics["extended_elbow"] = check_elbow_extension(landmarks, side_to_assess)
        metrics["pronated_forearm"] = check_pronated_forearm(landmarks, side_to_assess)

        # All conditions met         
        if angle >= 90 and metrics["extended_elbow"] and metrics["pronated_forearm"]:
            score = 2
        # Supination or elbow flexion during movement (can achieve either forearm pronation or elbow extension)
        elif metrics["extended_elbow"] or metrics["pronated_forearm"]:
            score = 1
        # Immediate supination or elbow flexion
        else:
            score = 0
            
        return score, metrics


class A4ShoulderFlexion90180(Exercise):
    def __init__(self, config):
        super().__init__(config)
        
    def evaluate(self, landmarks, side_to_assess):
        # TODO: Implement A4ShoulderFlexion90180 evaluation
        return 0, {}


class A4PronationSupinationElbow0(Exercise):
    def __init__(self, config):
        super().__init__(config)
        
    def evaluate(self, landmarks, side_to_assess):
        # TODO: Implement A4PronationSupinationElbow0 evaluation
        return 0, {}
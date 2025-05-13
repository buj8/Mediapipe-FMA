from core.exercises.base import Exercise
from utils.angle_utils import check_elbow_extension, check_shoulder_flexion

class A3HandToLumbarSpine(Exercise):
    def __init__(self, config):
        super().__init__(config)
        
    def evaluate(self, landmarks, side_to_assess):
        # TODO: Implement A3HandToLumbarSpine evaluation
        return 2, {}


class A3ShoulderFlexion090(Exercise):
    def __init__(self, config):
        super().__init__(config)
        
    def evaluate(self, landmarks, side_to_assess):
        metrics = {}

        metrics["shoulder_flexion"] = check_shoulder_flexion(landmarks, side_to_assess)
        metrics["extended_elbow"] = check_elbow_extension(landmarks, side_to_assess)

        if metrics["shoulder_flexion"] and metrics["extended_elbow"]:
            return 2, metrics
        elif metrics["shoulder_flexion"] or metrics["extended_elbow"]:
            return 1, metrics
        else:
            return 0, metrics


class A3PronationSupinationElbow90(Exercise):
    def __init__(self, config):
        super().__init__(config)
        
    def evaluate(self, landmarks, side_to_assess):
        #TODO: Implement A3PronationSupinationElbow90 evaluation
        return 2, {}
from config.landmarks import *
from core.exercises.factory import ExerciseFactory

class PoseEvaluator:
    def __init__(self, non_affected_side):
        if non_affected_side not in ["left", "right"]:
            raise ValueError("non_affected_side must be 'left' or 'right'")
            
        self.non_affected_side = non_affected_side
        self.affected_side = "right" if non_affected_side == "left" else "left"
        self.current_assessment_side = "unaffected"
        self.current_exercise = None
        self._last_evaluation = None
        
    def set_assessment_side(self, side):
        if side not in ["affected", "unaffected"]:
            raise ValueError("side must be 'affected' or 'unaffected'")
        self.current_assessment_side = side
        
    def set_current_exercise(self, exercise_config):
        if self.current_exercise is None or self.current_exercise.id != exercise_config.get("id"):
            self.current_exercise = ExerciseFactory.create_exercise(exercise_config)
        
    def evaluate_exercise(self, exercise_config, detection_result):
        if detection_result is None or not detection_result.pose_landmarks:
            return None
            
        landmarks = detection_result.pose_landmarks[0]
        self.set_current_exercise(exercise_config)
            
        side_to_assess = self.get_actual_side()
        self._last_evaluation = self.current_exercise.evaluate(landmarks, side_to_assess)
        
        return self._last_evaluation[0] if self._last_evaluation else None

    def get_actual_side(self):
        return self.non_affected_side if self.current_assessment_side == "unaffected" else self.affected_side

    def get_exercise_score(self):
        return self._last_evaluation[0] if self._last_evaluation else 0
        
    def get_last_metrics(self):
        return self._last_evaluation[1] if self._last_evaluation else {}
        
    def get_current_side(self):
        return self.current_assessment_side
        
    def is_affected_side(self):
        return self.current_assessment_side == "affected"
        

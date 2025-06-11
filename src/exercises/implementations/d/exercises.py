from exercises.base.base_exercise import Exercise
from exercises.criteria.exercise_criteria import calculate_index_nose_distance, calculate_index_knee_distance
import time


class DNose(Exercise):
    def __init__(self, config):
        super().__init__(config)
        self.start_time = None
        
    def evaluate(self, landmarks, side_to_assess):
        metrics = {}
        
        # Initialize start time if not set
        if self.start_time is None:
            self.start_time = time.time()
        
        # Calculate distance between index finger and nose
        distance = calculate_index_nose_distance(landmarks, side_to_assess)
        metrics["precision"] = distance
        
        # Calculate elapsed time
        elapsed_time = time.time() - self.start_time
        metrics["time"] = elapsed_time
        
        # Score based on distance thresholds
        if distance <= 0.1:  # Very close to nose
            precision_score = 2
        elif distance <= 0.2:  # Moderately close to nose
            precision_score = 1
        else:  # Too far from nose
            precision_score = 0
            
        # Score based on time thresholds
        if elapsed_time >= 6:  # Too slow
            time_score = 0
        elif elapsed_time >= 2:  # Moderate time
            time_score = 1
        else:  # Fast
            time_score = 2
            
        
        total_score = precision_score + time_score
            
        return total_score, metrics


class DKnee(Exercise):
    def __init__(self, config):
        super().__init__(config)
        self.start_time = None
        
    def evaluate(self, landmarks, side_to_assess):
        metrics = {}
        
        # Initialize start time if not set
        if self.start_time is None:
            self.start_time = time.time()
        
        # Calculate distance between index finger and knee
        distance = calculate_index_knee_distance(landmarks, side_to_assess)
        metrics["precision"] = distance
        
        # Calculate elapsed time
        elapsed_time = time.time() - self.start_time
        metrics["time"] = elapsed_time
        
        # Score based on distance thresholds
        if distance <= 0.1:  # Very close to knee
            precision_score = 2
        elif distance <= 0.2:  # Moderately close to knee
            precision_score = 1
        else:  # Too far from knee
            precision_score = 0
            
        # Score based on time thresholds
        if elapsed_time >= 6:  # Too slow
            time_score = 0
        elif elapsed_time >= 2:  # Moderate time
            time_score = 1
        else:  # Fast
            time_score = 2
            
        total_score = precision_score + time_score
            
        return total_score, metrics
from exercises.base.base_exercise import Exercise
from exercises.criteria.exercise_criteria import calculate_index_nose_distance, calculate_index_knee_distance
import time

class DNoseKnee(Exercise):
    def __init__(self, config):
        super().__init__(config)
        self.start_time = None
        self.current_state = "start"
        self.times_completed = 0
        self.precision_scores = []
        self.time_scores = []
        self.repetition_start_time = None
        
    def evaluate(self, landmarks, side_to_assess):
        metrics = {}

        # Initialize time if not set or reset if 20 seconds have passed
        current_time = time.time()
        if self.start_time is None or current_time - self.start_time > 20:
            self.start_time = current_time
            self.repetition_start_time = current_time
            self.current_state = "start"
            self.times_completed = 0
            self.precision_scores = []
            self.time_scores = []

        nose_distance = calculate_index_nose_distance(landmarks, side_to_assess)
        knee_distance = calculate_index_knee_distance(landmarks, side_to_assess)

        # State machine for tracking nose-to-knee movement
        if self.current_state == "start":
            if nose_distance < 0.15:
                self.current_state = "nose"
                self.repetition_start_time = current_time
                self.precision_scores.append(1)
            else:
                self.precision_scores.append(0)
        elif self.current_state == "nose":
            if nose_distance < 0.15:
                self.precision_scores[-1] = 2
            elif nose_distance > 0.2:  # Moved away from nose
                self.current_state = "moving_to_knee"
        elif self.current_state == "moving_to_knee":
            if knee_distance < 0.15:
                self.current_state = "knee"
                self.precision_scores.append(1)
            else:
                self.precision_scores.append(0)
        elif self.current_state == "knee":
            if knee_distance < 0.1:
                self.precision_scores[-1] = 2
            elif knee_distance > 0.2:  # Moved away from knee
                self.current_state = "moving_to_nose"
                # Calculate time score for this repetition
                elapsed_time = current_time - self.repetition_start_time
                if elapsed_time >= 6:  # Too slow
                    self.time_scores.append(0)
                elif elapsed_time >= 2:  # Moderate time
                    self.time_scores.append(1)
                else:  # Fast
                    self.time_scores.append(2)
                self.times_completed += 1
                self.repetition_start_time = current_time
        elif self.current_state == "moving_to_nose":
            if nose_distance < 0.2:
                self.current_state = "nose"
                self.precision_scores.append(1)
            else:
                self.precision_scores.append(0)

        # Calculate average scores
        if self.times_completed > 0:
            avg_precision = sum(self.precision_scores) / len(self.precision_scores)
            avg_time = sum(self.time_scores) / len(self.time_scores)
            total_score = round((avg_precision + avg_time) / 2 * 2) 
        else:
            total_score = 0

        metrics["precision"] = nose_distance
        metrics["knee_distance"] = knee_distance
        metrics["current_state"] = self.current_state
        metrics["times_completed"] = self.times_completed
        metrics["avg_precision"] = round(avg_precision) if self.times_completed > 0 else 0
        metrics["avg_time"] = round(avg_time) if self.times_completed > 0 else 0

        return total_score, metrics


class DNose(Exercise):
    def __init__(self, config):
        super().__init__(config)
        self.start_time = None
        
    def evaluate(self, landmarks, side_to_assess):
        metrics = {}
        
        # Initialize start time if not set
        if self.start_time is None or self.start_time - time.time() > 20:
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
        if self.start_time is None or self.start_time - time.time() > 20:
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
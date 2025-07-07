from src.exercises.base.base_exercise import Exercise

class CFlexion(Exercise):
    def __init__(self, config):
        super().__init__(config)
        self.scores = {
            "is_flexed": 0
        }

    def evaluate(self, landmarks, side_to_assess):
        metrics = {}
        if len(landmarks) <= 33:
            metrics["gesture"] = None
            return self.scores["is_flexed"], metrics
        metrics["gesture"] = landmarks[33] if side_to_assess == "right" else landmarks[34]
        if metrics["gesture"] == "Closed_Fist" or metrics["gesture"] == "Thumb_Down":
            self.scores["is_flexed"] = 2
        elif metrics["gesture"] == "Open_Palm":
            self.scores["is_flexed"] = 0
        else:
            self.scores["is_flexed"] = 1


        return self.scores["is_flexed"], metrics   

class CExtension(Exercise):
    def __init__(self, config):
        super().__init__(config)
        self.scores = {
            "is_extended": 0
        }
        
    def evaluate(self, landmarks, side_to_assess):
        metrics = {}
        if len(landmarks) <= 33:
            metrics["gesture"] = None
            return self.scores["is_extended"], metrics
        else:
            metrics["gesture"] = landmarks[33] if side_to_assess == "right" else landmarks[34]
            
        if metrics["gesture"] == "Closed_Fist" or metrics["gesture"] == "Thumb_Down":
            self.scores["is_extended"] = 0
        elif metrics["gesture"] == "Open_Palm":
            self.scores["is_extended"] = 2
        else:
            self.scores["is_extended"] = 1

        return self.scores["is_extended"], metrics
        
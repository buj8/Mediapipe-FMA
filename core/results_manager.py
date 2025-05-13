import time
import os 
import json

class ResultsManager:
   def __init__(self):
       self.exercise_scores = {}
       self.total_score = 0
       self.max_possible_score = 0
       self.affected_scores = {}
       self.unaffected_scores = {}
       
   def add_exercise_score(self, exercise_id, score, max_score=2, side="affected"):
       # Store scores by side
       if side == "affected":
           self.affected_scores[exercise_id] = score
           # Add to total score if it's the affected side
           self.total_score += score
           self.max_possible_score += max_score
       else:  # unaffected
           self.unaffected_scores[exercise_id] = score
       
   def generate_report(self):
       # Calculate totals
       affected_total = sum(self.affected_scores.values())
       unaffected_total = sum(self.unaffected_scores.values())
       
       # Calculate asymmetry index
       asymmetry_index = 0
       if affected_total > 0:
           asymmetry_index = (affected_total - unaffected_total) / affected_total * 100
       
       report = {
           "total_score": self.total_score,  # This is now only affected side
           "max_score": self.max_possible_score,
           "percentage": (self.total_score / self.max_possible_score * 100) if self.max_possible_score > 0 else 0,
           "affected_side_scores": self.affected_scores,
           "unaffected_side_scores": self.unaffected_scores,
           "asymmetry_index": asymmetry_index,
           "timestamp": time.strftime("%Y%m%d-%H%M%S")
       }
       
       return report
       
   def save_report(self, filepath=None):
       if filepath is None:
           timestamp = time.strftime("%Y%m%d-%H%M%S")
           filepath = f"data/assessment_reports/report_{timestamp}.json"
           
       os.makedirs(os.path.dirname(filepath), exist_ok=True)
       
       with open(filepath, 'w') as f:
           json.dump(self.generate_report(), f, indent=2)
           
       return filepath
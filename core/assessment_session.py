from core.pose_detector import PoseDetector
from core.data_capture import DataCapture
from utils.file_utils import load_fugl_meyer_tests

class FuglMeyerAssessment:
    def __init__(self):
        self.detector = PoseDetector()
        self.data_capture = DataCapture()
        self.exercises = []
        self.assessment_phase = "unaffected"
        self.current_exercise_index = 0
        self.results = {
            "affected": {},
            "unaffected": {}
        }
        
    def initialize(self):
        print("\nInitializing pose detector...")
        if not self.detector.initialize():
            return False
        
        # Load exercises from configuration
        tests = load_fugl_meyer_tests()
        if not tests or "exercises" not in tests:
            print("No exercises loaded from configuration")
            return False
        
        self.exercises = tests["exercises"]
        print(f"Loaded {len(self.exercises)} exercise(s)")
        return True
            
    def run_assessment(self, run_exercise_func):
        if not self.exercises:
            print("No exercises to run")
            return False
            
        print("\nReady to begin assessment")
        
        # Run each exercise for both sides before moving to the next exercise
        for i, exercise in enumerate(self.exercises):
            self.current_exercise_index = i
            print(f"\nExercise {i+1}/{len(self.exercises)}: {exercise['name']}")
            
            # First do unaffected side
            self.assessment_phase = "unaffected"
            print(f"\nStarting {self.assessment_phase} side...")
            
            exercise_complete = run_exercise_func(exercise, self.assessment_phase)
            if exercise_complete:
                self.results[self.assessment_phase][exercise['id']] = {
                    'name': exercise['name'],
                    'description': exercise['description'],
                    'completed': True
                }
            else:
                print(f"\nExercise skipped by user")
                
            # Then do affected side
            self.assessment_phase = "affected"
            print(f"\nStarting {self.assessment_phase} side...")
            
            exercise_complete = run_exercise_func(exercise, self.assessment_phase)
            if exercise_complete:
                self.results[self.assessment_phase][exercise['id']] = {
                    'name': exercise['name'],
                    'description': exercise['description'],
                    'completed': True
                }
            else:
                print(f"\nExercise skipped by user")
                
            print(f"\nCompleted exercise {i+1} for both sides")
            
        return self.results
        
    def get_current_exercise(self):
        if not self.exercises or self.current_exercise_index >= len(self.exercises):
            return None
        return self.exercises[self.current_exercise_index]
        
    def get_next_exercise(self):
        if not self.exercises or self.current_exercise_index >= len(self.exercises) - 1:
            return None
        return self.exercises[self.current_exercise_index + 1]
        
    def get_side_results(self, side):
        return self.results.get(side, {})
        
    def get_total_score(self, side):
        return sum(result.get('score', 0) for result in self.results.get(side, {}).values())
        
    def get_asymmetry_index(self):
        affected_score = self.get_total_score('affected')
        unaffected_score = self.get_total_score('unaffected')
        if affected_score == 0:
            return 0
        return (affected_score - unaffected_score) / affected_score * 100
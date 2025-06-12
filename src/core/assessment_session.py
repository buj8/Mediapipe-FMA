from src.core.pose_detector import PoseDetector
from src.utils.file_utils import load_fugl_meyer_tests
import cv2
import time
from src.utils.pose_visualization import draw_landmarks

class FuglMeyerAssessment:
    def __init__(self):
        self.detector = PoseDetector()
        self.exercises = []
        self.assessment_phase = "unaffected"
        self.current_exercise_index = 0
        self.results = {
            "affected": {},
            "unaffected": {}
        }
        self.interface = None
        self.evaluator = None
        self.results_manager = None
        
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
        print(f"Loaded {len(self.exercises)} exercises")
        return True
        
    def set_components(self, interface, evaluator, results_manager):
        """Set the components needed for running exercises"""
        self.interface = interface
        self.evaluator = evaluator
        self.results_manager = results_manager
            
    def run_assessment(self, cap):
        """Run the complete assessment"""
        if not self.exercises:
            print("No exercises to run")
            return False
            
        if not all([self.interface, self.evaluator, self.results_manager]):
            print("Missing required components. Call set_components first.")
            return False
            
        print("\nReady to begin assessment")
        
        # Run each exercise for both sides before moving to the next exercise
        for i, exercise in enumerate(self.exercises):
            self.current_exercise_index = i
            print(f"\nExercise {i+1}/{len(self.exercises)}: {exercise['name']}")
            
            # First do unaffected side
            self.assessment_phase = "unaffected"
            print(f"\nStarting {self.assessment_phase} side...")
            
            exercise_complete = self.run_exercise(cap, exercise, self.assessment_phase)
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

            self.evaluator.reset_current_exercise()
            
            exercise_complete = self.run_exercise(cap, exercise, self.assessment_phase)
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

    def run_exercise(self, cap, exercise, assessment_phase="affected"):
        """Run a single exercise and handle its results"""
        start_time = time.time()
        best_score = 0
        stabilization_frames = 0
        
        # Set the current side in the evaluator and load the exercise
        self.evaluator.set_assessment_side(assessment_phase)
        self.evaluator.set_current_exercise(exercise)
        
        # Read exercise configuration
        exercise_duration = exercise.get("duration", 30)
        required_stable_frames = exercise.get("required_stable_frames", 30) 
        
        while time.time() - start_time < exercise_duration and best_score < exercise.get("max_score", 2):
            # Calculate remaining time
            remaining_time = int(exercise_duration - (time.time() - start_time))
            
            # Read frame
            ret, frame = cap.read()
            if not ret:
                break
                
            # Process the frame with pose detection
            rgb_frame, detection_result = self.detector.process_frame(frame)
            annotated_frame = draw_landmarks(rgb_frame, detection_result)
            
            # Convert back to BGR 
            annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)

            # Evaluate the pose
            score = self.evaluator.evaluate_exercise(exercise, detection_result)
            metrics = self.evaluator.get_last_metrics()
            
            # Track best score and if they achieve it, we can stop the exercise
            if score is not None:
                if score >= best_score:
                    stabilization_frames += 1
                    if stabilization_frames >= required_stable_frames:
                        best_score = score
                else:
                    stabilization_frames = 0
            
            # Create split screen view
            split_screen = self.interface.create_split_screen(
                annotated_frame, 
                exercise, 
                self.evaluator, 
                metrics,
                time_remaining=remaining_time
            )
            self.interface.display(split_screen)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC key
                return False
        
        # If exercise completed successfully, save the score
        if best_score > 0:
            max_score = exercise.get("max_score", 2)
            self.results_manager.add_exercise_score(exercise['id'], best_score, max_score, assessment_phase)
            print(f"Exercise {exercise['id']} ({assessment_phase} side) completed with score: {best_score}")
            
        return True
        
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
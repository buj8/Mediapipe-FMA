import cv2
import time
from utils.pose_visualization import draw_landmarks

def run_exercise(cap, detector, interface, evaluator, exercise, assessment_phase="affected"):
    start_time = time.time()
    best_score = 0
    stabilization_frames = 0
    
    # Set the current side in the evaluator and load the exercise
    evaluator.set_assessment_side(assessment_phase)
    evaluator.set_current_exercise(exercise)
    
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
        rgb_frame, detection_result = detector.process_frame(frame)
        annotated_frame = draw_landmarks(rgb_frame, detection_result)
        
        # Convert back to BGR 
        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)

        # Evaluate the pose
        score = evaluator.evaluate_exercise(exercise, detection_result)
        metrics = evaluator.get_last_metrics()
        
        # Track best score and if they achieve it, we can stop the exercise
        if score is not None:
            if score >= best_score:
                stabilization_frames += 1
                if stabilization_frames >= required_stable_frames:
                    best_score = score
            else:
                stabilization_frames = 0
        
        # Create split screen view
        split_screen = interface.create_split_screen(
            annotated_frame, 
            exercise, 
            evaluator, 
            metrics,
            time_remaining=remaining_time
        )
        interface.display(split_screen)
        
        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            return False
    
    return True
import cv2

from core.exercise_interface import ExerciseInterface
from core.pose_evaluator import PoseEvaluator
from core.results_manager import ResultsManager
from core.assessment_session import FuglMeyerAssessment
from core.run_exercise import run_exercise
from utils.file_utils import ensure_directories_exist
from config.settings import *

def get_non_affected_side():
    print("\nPlease select your non-affected side:")
    print("1. Left (stroke affected your right side)")
    print("2. Right (stroke affected your left side)")
    
    while True:
        choice = input("Enter your choice (1 or 2): ")
        if choice == '1':
            return "left"
        elif choice == '2':
            return "right"
        else:
            print("Invalid choice. Please enter 1 or 2.")

def main():
    """
    Main application entry point for Fugl Meyer Upper Extremity Assessment
    """
    # Ensure required directories exist
    ensure_directories_exist([
        MODELS_DIRECTORY, 
        CAPTURED_SESSIONS_DIRECTORY, 
        ASSESSMENT_REPORTS_DIRECTORY,
        REFERENCE_POSES_DIRECTORY
    ])
    
    # Get non-affected side
    non_affected_side = get_non_affected_side()
    print(f"Non-affected side set to: {non_affected_side}")
    print(f"Affected side set to: {'right' if non_affected_side == 'left' else 'left'}")
    
    # Initialize assessment session
    assessment = FuglMeyerAssessment()
    if not assessment.initialize():
        print("Failed to initialize assessment. Exiting.")
        return
    
    # Initialize components
    interface = ExerciseInterface("Fugl Meyer Assessment")
    evaluator = PoseEvaluator(non_affected_side)
    results = ResultsManager()
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
        
    print("Webcam opened successfully")
    
    # Define a wrapper function for run_exercise that includes our components
    def run_exercise_wrapper(exercise, assessment_phase):
        success = run_exercise(cap, assessment.detector, interface, evaluator, exercise, assessment_phase)
        if success:
            score = evaluator.get_exercise_score()
            max_score = 2  # Default max score
            results.add_exercise_score(exercise['id'], score, max_score, assessment_phase)
            print(f"Exercise {exercise['id']} ({assessment_phase} side) completed with score: {score}")
        return success
    
    # Run the assessment
    assessment.run_assessment(run_exercise_wrapper)
    
    # Generate and save report
    report_path = results.save_report()
    print(f"\nAssessment complete. Report saved to {report_path}")
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    
    # Show final results
    total_score = results.total_score
    max_possible = results.max_possible_score
    percentage = (total_score / max_possible * 100) if max_possible > 0 else 0
    
    print("\n" + "="*50)
    print("Fugl Meyer Assessment Results")
    print("="*50)
    print(f"Total Score (Affected Side): {total_score}/{max_possible} ({percentage:.1f}%)")
    print(f"Asymmetry Index: {results.generate_report()['asymmetry_index']:.1f}%")
    print("="*50)
    
    print("\nAffected Side Scores:")
    for exercise_id, score in results.affected_scores.items():
        print(f"{exercise_id}: {score}")
        
    print("\nUnaffected Side Scores (for asymmetry):")
    for exercise_id, score in results.unaffected_scores.items():
        print(f"{exercise_id}: {score}")
    
    print("\nThank you for completing the assessment!")

if __name__ == "__main__":
    main()
import cv2
import sys

from src.gui.exercise_interface import ExerciseInterface
from src.core.pose_evaluator import PoseEvaluator
from src.core.results_manager import ResultsManager
from src.core.assessment_session import FuglMeyerAssessment
from src.utils.file_utils import ensure_directories_exist, get_non_affected_side
from src.config.settings import *
from src.gui.results_interface import ResultsInterface

def main():
    """
    Main application entry point for Fugl Meyer Upper Extremity Assessment
    """
    # Ensure required directories exist
    ensure_directories_exist([
        MODELS_DIRECTORY, 
        ASSESSMENT_REPORTS_DIRECTORY,
        REFERENCE_POSES_DIRECTORY
    ])
    
    # Get non-affected side
    non_affected_side = get_non_affected_side()
    
    # Initialize assessment session
    assessment = FuglMeyerAssessment()
    if not assessment.initialize():
        print("Failed to initialize assessment. Exiting.")
        return
    
    # Initialize components
    interface = ExerciseInterface("Fugl Meyer Assessment")
    evaluator = PoseEvaluator(non_affected_side)
    results = ResultsManager()
    
    # Set components in assessment
    assessment.set_components(interface, evaluator, results)
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, 30)  # Set to 30 FPS
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffer size
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
        
    print("Webcam opened successfully")
    
    # Run the assessment
    assessment.run_assessment(cap)
    
    # Generate and save report
    report_path = results.save_report()
    print(f"\nAssessment complete. Report saved to {report_path}")
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    
    # Show results
    results = ResultsManager()
    results.affected_scores = assessment.get_side_results("affected")
    results.unaffected_scores = assessment.get_side_results("unaffected")
    results.total_score = assessment.get_total_score("affected")
    results.max_possible_score = sum(exercise['max_score'] for exercise in assessment.exercises)
    
    interface = ResultsInterface(results, evaluator.affected_side)
    return interface.show()

if __name__ == "__main__":
    main()
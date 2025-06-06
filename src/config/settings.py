import os
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Camera settings
CAMERA_ID = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# MediaPipe model settings
MODEL_PATH = str(PROJECT_ROOT / "data/models/pose_landmarker.task")
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/1/pose_landmarker_heavy.task"

# File paths
OUTPUT_DIRECTORY = str(PROJECT_ROOT / "data/assessment_reports")
MODELS_DIRECTORY = str(PROJECT_ROOT / "data/models")
ASSESSMENT_REPORTS_DIRECTORY = str(PROJECT_ROOT / "data/assessment_reports")
REFERENCE_POSES_DIRECTORY = str(PROJECT_ROOT / "data/reference_poses")
CONFIG_DIRECTORY = str(PROJECT_ROOT / "src/config")

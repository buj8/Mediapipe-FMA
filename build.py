import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build_directories():
    """Clean up previous build artifacts"""
    dirs_to_clean = ['build', 'main.dist', 'main.build']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)

def copy_required_files():
    """Copy necessary files to the build directory"""
    # Create directories if they don't exist
    os.makedirs('main.dist/data', exist_ok=True)
    os.makedirs('main.dist/test_images', exist_ok=True)
    
    # Copy data directory
    if os.path.exists('data'):
        shutil.copytree('data', 'main.dist/data', dirs_exist_ok=True)
    
    # Copy test images
    if os.path.exists('test_images'):
        shutil.copytree('test_images', 'main.dist/test_images', dirs_exist_ok=True)

def build_executable():
    """Build the executable using Nuitka"""
    # Clean previous builds
    clean_build_directories()
    
    # Nuitka command
    nuitka_cmd = [
        sys.executable, '-m', 'nuitka',
        '--standalone',
        '--enable-plugin=pyqt6',
        '--enable-plugin=numpy',
        '--include-package=mediapipe',
        '--include-package=mediapipe.python',
        '--include-package=mediapipe.framework',
        '--include-package=mediapipe.modules',
        '--include-package=mediapipe.tasks',
        '--include-package=cv2',
        '--include-package=numpy',
        '--include-package=PyQt6',
        '--include-data-dir=src=src',
        '--include-data-dir=data=data',
        '--include-data-dir=test_images=test_images',
        '--output-dir=build',
        '--output-filename=FuglMeyerAssessment',
        '--jobs=0',  # Use all available CPU cores
        '--remove-output',  # Remove build directory before building
        '--show-progress',
        '--show-memory',
        '--verbose',
        '--follow-imports',
        'main.py'
    ]
    
    # Run Nuitka
    subprocess.run(nuitka_cmd, check=True)
    
    # Copy additional required files
    copy_required_files()
    
    print("\nBuild completed successfully!")
    print("The executable can be found in the 'build' directory.")

if __name__ == "__main__":
    build_executable() 
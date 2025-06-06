import os
import urllib.request
from src.config.settings import CONFIG_DIRECTORY

def ensure_directories_exist(directory_list):
    for directory in directory_list:
        os.makedirs(directory, exist_ok=True)
        print(f"Ensured directory exists: {directory}")

def download_file(url, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    print(f"Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"Downloaded {filename} successfully!")
        return True
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
        return False

def get_session_filename(prefix="session", extension="json"):
    import time
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"

def load_json_file(filepath):
    import json
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file {filepath}: {e}")
        return None

def load_fugl_meyer_tests():
    config_path = os.path.join(CONFIG_DIRECTORY, "fugl_meyer_tests.json")
    return load_json_file(config_path)

def get_non_affected_side():
    print("\nPlease select your non-affected side:")
    print("1. Left (stroke affected your right side)")
    print("2. Right (stroke affected your left side)")
    
    while True:
        choice = input("Enter your choice (1 or 2): ")
        if choice == '1':
            non_affected = "left"
            break
        elif choice == '2':
            non_affected = "right"
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
    
    print(f"Non-affected side set to: {non_affected}")
    print(f"Affected side set to: {'right' if non_affected == 'left' else 'left'}")
    return non_affected
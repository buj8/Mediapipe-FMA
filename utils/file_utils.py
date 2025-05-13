import os
import urllib.request

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
    config_path = "config/fugl_meyer_tests.json"
    return load_json_file(config_path)
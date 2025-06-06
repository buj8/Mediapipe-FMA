import numpy as np
import math
from config.landmarks import *

# ---------- HELPER FUNCTIONS ----------

def calculate_angle(a, b, c):
    vector_ba = np.array([a[0] - b[0], a[1] - b[1], a[2] - b[2]])
    vector_bc = np.array([c[0] - b[0], c[1] - b[1], c[2] - b[2]])
    
    vector_ba = vector_ba / np.linalg.norm(vector_ba)
    vector_bc = vector_bc / np.linalg.norm(vector_bc)
    
    dot_product = np.dot(vector_ba, vector_bc)
    angle = math.acos(np.clip(dot_product, -1.0, 1.0))
    
    angle = math.degrees(angle)
    
    return angle

def calculate_2d_vertical_angle(landmark_a, landmark_b):
    vertical = np.array([0, -1, 0])
    
    vector = np.array([landmark_b.x - landmark_a.x, landmark_b.y - landmark_a.y, 0])
    
    if np.all(vector == 0):
        return 0
        
    vector = vector / np.linalg.norm(vector)
    
    dot_product = np.dot(vertical, vector)
    angle = math.acos(np.clip(dot_product, -1.0, 1.0))
    
    angle = math.degrees(angle)
    
    return angle

def calculate_2d_sagittal_angle(landmark_a, landmark_b):
    """Calculate angle in the sagittal plane (for measuring shoulder flexion).
    Returns the angle between a vertical line and the line formed by landmarks a and b.
    """
    # Sagittal direction vector (forward is positive X in mediapipe)
    sagittal = np.array([1, 0, 0])
    
    # Create vector from landmark_a to landmark_b (primarily in the X-Y plane)
    vector = np.array([landmark_b.x - landmark_a.x, landmark_b.y - landmark_a.y, 0])
    
    if np.all(vector == 0):
        return 0
        
    vector = vector / np.linalg.norm(vector)
    
    dot_product = np.dot(sagittal, vector)
    angle = math.acos(np.clip(dot_product, -1.0, 1.0))
    
    angle = math.degrees(angle)
    
    # Adjust the angle based on whether the arm is raised or lowered
    if landmark_b.y > landmark_a.y:  # If the arm is below horizontal
        angle = 180 - angle
        
    return angle

def get_joint_angle(landmarks, joint_type, side="left"):
    """Calculate the angle for a specific joint."""
    side_dict = LEFT_LANDMARKS if side == "left" else RIGHT_LANDMARKS
    
    if joint_type == "shoulder_abduction":
        # For shoulder abduction, we need shoulder, elbow, and a reference point
        shoulder = landmarks[side_dict["SHOULDER"]]
        elbow = landmarks[side_dict["ELBOW"]]
        # Reference point is the opposite shoulder
        opposite_dict = RIGHT_LANDMARKS if side == "left" else LEFT_LANDMARKS
        reference = landmarks[opposite_dict["SHOULDER"]]
        
        # Calculate vectors
        v1 = np.array([shoulder.x - reference.x, shoulder.y - reference.y])
        v2 = np.array([elbow.x - shoulder.x, elbow.y - shoulder.y])
        
    elif joint_type == "shoulder_flexion":
        # For shoulder flexion, we need shoulder, elbow, and hip
        shoulder = landmarks[side_dict["SHOULDER"]]
        elbow = landmarks[side_dict["ELBOW"]]
        hip = landmarks[side_dict["HIP"]]
        
        # Calculate vectors
        v1 = np.array([shoulder.x - hip.x, shoulder.y - hip.y])
        v2 = np.array([elbow.x - shoulder.x, elbow.y - shoulder.y])
        
    elif joint_type == "elbow":
        # For elbow, we need shoulder, elbow, and wrist
        shoulder = landmarks[side_dict["SHOULDER"]]
        elbow = landmarks[side_dict["ELBOW"]]
        wrist = landmarks[side_dict["WRIST"]]
        
        # Calculate vectors
        v1 = np.array([shoulder.x - elbow.x, shoulder.y - elbow.y])
        v2 = np.array([wrist.x - elbow.x, wrist.y - elbow.y])
        
    elif joint_type == "forearm_supination":
        # For forearm supination, we need elbow, wrist, and a reference point
        elbow = landmarks[side_dict["ELBOW"]]
        wrist = landmarks[side_dict["WRIST"]]
        shoulder = landmarks[side_dict["SHOULDER"]]
        
        # Calculate vectors
        v1 = np.array([shoulder.x - elbow.x, shoulder.y - elbow.y])
        v2 = np.array([wrist.x - elbow.x, wrist.y - elbow.y])
        
    elif joint_type == "forearm_pronation":
        # For forearm pronation, we need elbow, wrist, and a reference point
        elbow = landmarks[side_dict["ELBOW"]]
        wrist = landmarks[side_dict["WRIST"]]
        shoulder = landmarks[side_dict["SHOULDER"]]
        
        # Calculate vectors
        v1 = np.array([shoulder.x - elbow.x, shoulder.y - elbow.y])
        v2 = np.array([wrist.x - elbow.x, wrist.y - elbow.y])
        
    else:
        raise ValueError(f"Unknown joint type: {joint_type}")
    
    # Calculate angle
    v1_norm = v1 / np.linalg.norm(v1) if np.linalg.norm(v1) > 0 else v1
    v2_norm = v2 / np.linalg.norm(v2) if np.linalg.norm(v2) > 0 else v2
    
    dot = np.dot(v1_norm, v2_norm)
    angle = math.degrees(math.acos(np.clip(dot, -1.0, 1.0)))
    
    # Determine sign of angle based on cross product
    cross = np.cross(v1_norm, v2_norm)
    sign = 1 if cross > 0 else -1
    
    return angle * sign

def calculate_shoulder_width(landmarks):
    """Calculate the width between shoulders."""
    left_shoulder = landmarks[LEFT_LANDMARKS["SHOULDER"]]
    right_shoulder = landmarks[RIGHT_LANDMARKS["SHOULDER"]]
    return abs(left_shoulder.x - right_shoulder.x)

def calculate_horizontal_distance(landmark_a, landmark_b):
    """Calculate horizontal distance between landmarks (x and z plane)."""
    return np.sqrt((landmark_a.x - landmark_b.x)**2 + (landmark_a.z - landmark_b.z)**2)

def calculate_vertical_distance(landmark_a, landmark_b):
    """Calculate vertical distance between landmarks (y axis)."""
    return abs(landmark_a.y - landmark_b.y)

def calculate_shoulder_rotation(landmarks, side="left"):
    """Calculate external/internal rotation of the shoulder."""
    side_dict = LEFT_LANDMARKS if side == "left" else RIGHT_LANDMARKS
    
    shoulder = landmarks[side_dict["SHOULDER"]]
    elbow = landmarks[side_dict["ELBOW"]]
    wrist = landmarks[side_dict["WRIST"]]
    
    # Project onto the frontal plane (y-z plane)
    elbow_projected = np.array([0, elbow.y, elbow.z])
    wrist_projected = np.array([0, wrist.y, wrist.z])
    shoulder_projected = np.array([0, shoulder.y, shoulder.z])
    
    # Vector from elbow to shoulder
    se_vector = shoulder_projected - elbow_projected
    
    # Vector from elbow to wrist
    we_vector = wrist_projected - elbow_projected
    
    # Calculate the angle between these vectors in the frontal plane
    se_vector_norm = se_vector / np.linalg.norm(se_vector) if np.linalg.norm(se_vector) > 0 else se_vector
    we_vector_norm = we_vector / np.linalg.norm(we_vector) if np.linalg.norm(we_vector) > 0 else we_vector
    
    dot = np.dot(se_vector_norm, we_vector_norm)
    angle = math.degrees(math.acos(np.clip(dot, -1.0, 1.0)))
    
    # Determine if internal or external rotation
    cross = np.cross(se_vector_norm, we_vector_norm)
    sign = 1 if (cross[0] > 0 and side == "left") or (cross[0] < 0 and side == "right") else -1
    
    return angle * sign

# ---------- SHOULDER FUNCTIONS ----------

# Shoulder Elevation
def check_shoulder_elevation(landmarks, side="left", threshold=0.2):
    """Check if shoulder is elevated (shrugged up)."""
    side_dict = LEFT_LANDMARKS if side == "left" else RIGHT_LANDMARKS
    
    shoulder = landmarks[side_dict["SHOULDER"]]
    hip = landmarks[side_dict["HIP"]]
    
    # Compare relative height of shoulders to reference height
    body_height = abs(hip.y - shoulder.y)
    opposite = "right" if side == "left" else "left"
    opposite_dict = RIGHT_LANDMARKS if side == "left" else LEFT_LANDMARKS
    opposite_shoulder = landmarks[opposite_dict["SHOULDER"]]
    
    # Elevation is measured by how much higher the shoulder is than expected
    elevation_ratio = (shoulder.y - opposite_shoulder.y) / body_height
    
    return elevation_ratio <= -threshold if side == "left" else elevation_ratio >= threshold

def check_partial_shoulder_elevation(landmarks, side="left", threshold=0.1, full_threshold=0.2):
    """Check if shoulder is partially elevated."""
    elevation = check_shoulder_elevation(landmarks, side, full_threshold)
    if elevation:
        return False  # It's a full elevation, not partial
    
    # Same calculation but with a lower threshold for partial
    side_dict = LEFT_LANDMARKS if side == "left" else RIGHT_LANDMARKS
    shoulder = landmarks[side_dict["SHOULDER"]]
    hip = landmarks[side_dict["HIP"]]
    
    body_height = abs(hip.y - shoulder.y)
    opposite = "right" if side == "left" else "left"
    opposite_dict = RIGHT_LANDMARKS if side == "left" else LEFT_LANDMARKS
    opposite_shoulder = landmarks[opposite_dict["SHOULDER"]]
    
    elevation_ratio = (shoulder.y - opposite_shoulder.y) / body_height
    
    return elevation_ratio <= -threshold if side == "left" else elevation_ratio >= threshold

# Shoulder Abduction/Adduction
def check_shoulder_abduction(landmarks, side="left", angle_threshold=90):
    """Check if shoulder is abducted (raised to the side) at specified angle."""
    abduction_angle = get_joint_angle(landmarks, "shoulder_abduction", side)
    return abs(abduction_angle) >= angle_threshold

def check_shoulder_abduction_50(landmarks, side="left"):
    """Check if shoulder is abducted at approximately 50 degrees."""
    return check_shoulder_abduction(landmarks, side, 50)

def check_shoulder_abduction_90(landmarks, side="left"):
    """Check if shoulder is abducted at approximately 90 degrees."""
    return check_shoulder_abduction(landmarks, side, 90)

def check_shoulder_adduction(landmarks, side="left", threshold=20):
    """Check if shoulder is adducted (arm close to body)."""
    abduction_angle = get_joint_angle(landmarks, "shoulder_abduction", side)
    return abs(abduction_angle) <= threshold

def check_partial_shoulder_adduction(landmarks, side="left", threshold=30, full_threshold=20):
    """Check if shoulder is partially adducted."""
    adduction = check_shoulder_adduction(landmarks, side, full_threshold)
    if adduction:
        return False  # It's a full adduction, not partial
    
    abduction_angle = get_joint_angle(landmarks, "shoulder_abduction", side)
    return abs(abduction_angle) <= threshold

# Shoulder Rotation
def check_shoulder_ext_rotation(landmarks, side="left", threshold=45):
    """Check if shoulder is externally rotated."""
    rotation = calculate_shoulder_rotation(landmarks, side)
    return rotation >= threshold

def check_partial_shoulder_ext_rotation(landmarks, side="left", threshold=25, full_threshold=45):
    """Check if shoulder is partially externally rotated."""
    rotation = calculate_shoulder_rotation(landmarks, side)
    return threshold <= rotation < full_threshold

# Shoulder Flexion
def check_shoulder_flexion(landmarks, side="left", threshold=90):
    """Check if shoulder is flexed (arm raised forward) beyond the threshold angle."""
    flexion_angle = get_joint_angle(landmarks, "shoulder_flexion", side)
    return flexion_angle >= threshold

def check_partial_shoulder_flexion(landmarks, side="left", threshold=45, full_threshold=90):
    """Check if shoulder is partially flexed forward."""
    flexion = check_shoulder_flexion(landmarks, side, full_threshold)
    if flexion:
        return False  # It's a full flexion, not partial
    
    flexion_angle = get_joint_angle(landmarks, "shoulder_flexion", side)
    return threshold <= flexion_angle < full_threshold

# ---------- ELBOW FUNCTIONS ----------

def check_elbow_flexion(landmarks, side="left", threshold=90):
    """Check if elbow is flexed (bent)."""
    elbow_angle = get_joint_angle(landmarks, "elbow", side)
    return elbow_angle <= 180 - threshold  # 180 degrees is straight arm

def check_partial_elbow_flexion(landmarks, side="left", threshold=45, full_threshold=90):
    """Check if elbow is partially flexed."""
    elbow_angle = get_joint_angle(landmarks, "elbow", side)
    return (180 - full_threshold) < elbow_angle <= (180 - threshold)

def check_elbow_extension(landmarks, side="left", threshold=160):
    """Check if elbow is extended (straight)."""
    elbow_angle = get_joint_angle(landmarks, "elbow", side)
    return elbow_angle >= threshold

def check_partial_elbow_extension(landmarks, side="left", threshold=135, full_threshold=160):
    """Check if elbow is partially extended."""
    elbow_angle = get_joint_angle(landmarks, "elbow", side)
    return threshold <= elbow_angle < full_threshold


# ---------- FOREARM FUNCTIONS ----------

# Basic implementation, ideally we'll use the hand model to check for supination/pronation

def check_pronated_forearm(landmarks, side="left"):
    side_dict = LEFT_LANDMARKS if side == "left" else RIGHT_LANDMARKS

    index = landmarks[side_dict["INDEX"]]
    pinky = landmarks[side_dict["PINKY"]]
    
    return index.y > pinky.y

def check_supinated_forearm(landmarks, side="left"):
    side_dict = LEFT_LANDMARKS if side == "left" else RIGHT_LANDMARKS
    
    index = landmarks[side_dict["INDEX"]]
    pinky = landmarks[side_dict["PINKY"]]

    return pinky.y < index.y

def check_partial_supination(landmarks, side="left"):
    side_dict = LEFT_LANDMARKS if side == "left" else RIGHT_LANDMARKS
    
    wrist = landmarks[side_dict["WRIST"]]
    index = landmarks[side_dict["INDEX"]]
    pinky = landmarks[side_dict["PINKY"]]
    
    # For partial supination, index and pinky more or less at same height
    height_diff = abs(pinky.y - index.y)
    
    # Normalize by wrist-to-finger distance (using index finger instead of middle)
    wrist_to_finger_distance = np.sqrt((wrist.x - index.x)**2 + (wrist.y - index.y)**2 + (wrist.z - index.z)**2)
    
    # When height difference is small relative to hand size, consider it partial supination
    return height_diff < 0.05 * wrist_to_finger_distance

def calculate_forearm_rotation(landmarks, side="left"):
    side_dict = LEFT_LANDMARKS if side == "left" else RIGHT_LANDMARKS
    
    index = landmarks[side_dict["INDEX"]]
    pinky = landmarks[side_dict["PINKY"]]
    
    # Calculate vector from pinky to index finger (across palm)
    hand_vector = np.array([index.x - pinky.x, index.y - pinky.y, index.z - pinky.z])
    
    # Calculate vertical vector (representing gravity)
    vertical_vector = np.array([0, 1, 0])
    
    # Calculate the angle between these vectors
    hand_vector_norm = hand_vector / np.linalg.norm(hand_vector) if np.linalg.norm(hand_vector) > 0 else hand_vector
    
    dot = np.dot(hand_vector_norm, vertical_vector)
    angle = math.degrees(math.acos(np.clip(dot, -1.0, 1.0)))
    
    # Determine if pronation or supination based on relative positions
    if side == "left":
        # For left arm, pronation means index is below pinky
        sign = 1 if index.y > pinky.y else -1
    else:
        # For right arm, pronation means pinky is below index
        sign = 1 if pinky.y > index.y else -1
    
    # Return signed angle: positive for pronation, negative for supination
    return angle * sign
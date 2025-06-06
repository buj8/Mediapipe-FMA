from utils.angle_utils import (
    get_joint_angle, calculate_shoulder_width,
    LEFT_LANDMARKS, RIGHT_LANDMARKS
)

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
    
    side_dict = LEFT_LANDMARKS if side == "left" else RIGHT_LANDMARKS
    shoulder = landmarks[side_dict["SHOULDER"]]
    hip = landmarks[side_dict["HIP"]]
    
    body_height = abs(hip.y - shoulder.y)
    opposite = "right" if side == "left" else "left"
    opposite_dict = RIGHT_LANDMARKS if side == "left" else LEFT_LANDMARKS
    opposite_shoulder = landmarks[opposite_dict["SHOULDER"]]
    
    elevation_ratio = (shoulder.y - opposite_shoulder.y) / body_height
    
    return elevation_ratio <= -threshold if side == "left" else elevation_ratio >= threshold

def check_shoulder_abduction(landmarks, side="left", angle_threshold=90):
    """Check if shoulder is abducted (raised to the side) at specified angle."""
    abduction_angle = get_joint_angle(landmarks, "shoulder_abduction", side)
    return abs(abduction_angle) >= angle_threshold

def check_shoulder_flexion(landmarks, side="left", threshold=90):
    """Check if shoulder is flexed (arm raised forward) beyond the threshold angle."""
    flexion_angle = get_joint_angle(landmarks, "shoulder_flexion", side)
    return flexion_angle >= threshold

def check_elbow_extension(landmarks, side="left", threshold=160):
    """Check if elbow is extended beyond the threshold angle."""
    elbow_angle = get_joint_angle(landmarks, "elbow", side)
    return elbow_angle >= threshold

def check_partial_elbow_extension(landmarks, side="left", threshold=135, full_threshold=160):
    """Check if elbow is partially extended."""
    extension = check_elbow_extension(landmarks, side, full_threshold)
    if extension:
        return False  # It's a full extension, not partial
    
    elbow_angle = get_joint_angle(landmarks, "elbow", side)
    return threshold <= elbow_angle < full_threshold

def check_supinated_forearm(landmarks, side="left", threshold=45):
    """Check if forearm is supinated (palm up) beyond the threshold angle."""
    supination_angle = get_joint_angle(landmarks, "forearm_supination", side)
    return abs(supination_angle) >= threshold

def check_partial_supination(landmarks, side="left", threshold=25, full_threshold=45):
    """Check if forearm is partially supinated."""
    supination = check_supinated_forearm(landmarks, side, full_threshold)
    if supination:
        return False  # It's a full supination, not partial
    
    supination_angle = get_joint_angle(landmarks, "forearm_supination", side)
    return threshold <= abs(supination_angle) < full_threshold

def check_pronated_forearm(landmarks, side="left", threshold=45):
    """Check if forearm is pronated (palm down) beyond the threshold angle."""
    pronation_angle = get_joint_angle(landmarks, "forearm_pronation", side)
    return abs(pronation_angle) >= threshold 
import math
import numpy as np
from src.config.landmarks import LEFT_LANDMARKS, RIGHT_LANDMARKS


def calculate_shoulder_abduction_adduction(landmarks, side="left"):
    """Calculate shoulder abduction/adduction angle in the frontal plane (x-y).
    Positive values indicate abduction (arm raised), negative values indicate adduction (arm lowered).
    0 degrees means arm is parallel to ground, 90 degrees means arm is vertical.
    
    Uses two 2D vectors:
    1. Vector from shoulder to ground (gravity-aligned) in (x,y) plane
    2. Vector from shoulder to elbow in (x,y) plane
    """
    side_dict = LEFT_LANDMARKS if side == "left" else RIGHT_LANDMARKS
    
    # Get relevant landmarks
    shoulder = landmarks[side_dict["SHOULDER"]]
    elbow = landmarks[side_dict["ELBOW"]]
    
    # Vector 1: From shoulder to ground (gravity-aligned) in x-y plane
    v1 = np.array([0, 1])  # Points downward
    
    # Vector 2: From shoulder to elbow in x-y plane
    v2 = np.array([elbow.x - shoulder.x, elbow.y - shoulder.y])
    
    if np.all(v2 == 0):
        return 0
        
    # Normalize vectors
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    
    # Calculate angle magnitude (always positive, between 0 and 180)
    dot = np.dot(v1, v2)
    angle = math.degrees(math.acos(dot))

    # Determine sign using cross product
    if side == "left":
        sign = -1 if np.cross(v1, v2) > 0 else 1
    else:
        sign = 1 if np.cross(v1, v2) > 0 else -1
    
    return angle * sign

def calculate_shoulder_flexion_extension(landmarks, side="left"):
    """Calculate shoulder flexion/extension angle in the sagittal plane (y-z).
    Positive values indicate flexion (arm raised forward), negative values indicate extension (arm behind).
    0 degrees means arm is parallel to ground, 90 degrees means arm is vertical.
    
    Uses two 2D vectors:
    1. Vector from shoulder to ground (gravity-aligned) in (y,z) plane
    2. Vector from shoulder to elbow in (y,z) plane
    """
    side_dict = LEFT_LANDMARKS if side == "left" else RIGHT_LANDMARKS
    
    # Get relevant landmarks
    shoulder = landmarks[side_dict["SHOULDER"]]
    elbow = landmarks[side_dict["ELBOW"]]
    
    # Vector 1: From shoulder to ground (gravity-aligned) in y-z plane
    v1 = np.array([0, 1])  # Points downward
    
    # Vector 2: From shoulder to elbow in y-z plane
    v2 = np.array([elbow.z - shoulder.z + 0.07, elbow.y - shoulder.y])
    
    if np.all(v2 == 0):
        return 0
        
    # Normalize vectors
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    
    # Calculate angle magnitude (always positive, between 0 and 180)
    dot = np.dot(v1, v2)
    angle = math.degrees(math.acos(dot))
    
    
    return angle

def calculate_shoulder_elevation(landmarks, side="left"):
    """
    Calculate the shoulder elevation in the gravity axis (y) relative to the opposite shoulder.
    Positive values indicate elevation (shoulder is raised above the opposite shoulder)
    Negative values indicate depression (shoulder is lowered below the opposite shoulder)
    """
    # Angle from opposite shoulder to shoulder with the floor as axis
    side_dict = LEFT_LANDMARKS if side == "left" else RIGHT_LANDMARKS
    opposite_side_dict = RIGHT_LANDMARKS if side == "left" else LEFT_LANDMARKS

    # Get relevant landmarks
    shoulder = landmarks[side_dict["SHOULDER"]]
    opposite_shoulder = landmarks[opposite_side_dict["SHOULDER"]]

    # Vector 1: From opposite shoulder to shoulder
    v1 = np.array([opposite_shoulder.x - shoulder.x, opposite_shoulder.y - shoulder.y])

    # Vector 2: From opposite shoulder parallel to the floor
    v2 = np.array([-1 if side == "left" else 1, 0])

    # Normalize vectors
    sign = 1 if opposite_shoulder.y > shoulder.y else -1

    v1 = v1 / np.linalg.norm(v1)

    

    # Calculate the angle between the two vectors
    angle = math.degrees(math.acos(np.dot(v1, v2)))

    return angle * sign

def calculate_elbow_flexion_extension(landmarks, side="left", plane="frontal"):
    """Calculate elbow flexion/extension angle.
    Positive values indicate flexion (bending the elbow), negative values indicate extension (straightening).
    0 degrees means arm is straight, 90 degrees means elbow is bent at right angle.
    
    Uses two 2D vectors:
    1. Vector from elbow to shoulder
    2. Vector from elbow to wrist
    
    Args:
        landmarks: Dictionary of landmark positions
        side: "left" or "right" side of the body
        plane: "frontal" for x-y plane or "sagittal" for y-z plane
    """
    side_dict = LEFT_LANDMARKS if side == "left" else RIGHT_LANDMARKS
    
    # Get relevant landmarks
    shoulder = landmarks[side_dict["SHOULDER"]]
    elbow = landmarks[side_dict["ELBOW"]]
    wrist = landmarks[side_dict["WRIST"]]
    
    # Vector 1: From elbow to shoulder
    if plane == "frontal":
        v1 = np.array([shoulder.x - elbow.x, shoulder.y - elbow.y])
        v2 = np.array([wrist.x - elbow.x, wrist.y - elbow.y])
    else:  # sagittal plane
        v1 = np.array([shoulder.z - elbow.z, shoulder.y - elbow.y])
        v2 = np.array([wrist.z - elbow.z, wrist.y - elbow.y])
    
    # Normalize vectors
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    
    # Calculate angle magnitude (always positive, between 0 and 180)
    dot = np.dot(v1, v2)
    angle = math.degrees(math.acos(dot))
    
    return angle

def calculate_index_knee_distance(landmarks, side="left"):
    """Calculate the distance between the index finger and the knee in the frontal plane (x-y).
    
    Args:
        landmarks: Dictionary of landmark positions
        side: "left" or "right" side of the body
    """
    side_dict = LEFT_LANDMARKS if side == "left" else RIGHT_LANDMARKS
    
    # Get relevant landmarks
    index = landmarks[side_dict["INDEX"]]
    knee = landmarks[side_dict["KNEE"]]
    
    # Calculate distance in x-y plane
    dx = index.x - knee.x
    dy = index.y - knee.y
    
    return math.sqrt(dx*dx + dy*dy)

def calculate_index_nose_distance(landmarks, side="left"):
    """Calculate the distance between the index finger and the nose in the frontal plane (x-y).
    
    Args:
        landmarks: Dictionary of landmark positions
        side: "left" or "right" side of the body
    """
    side_dict = LEFT_LANDMARKS if side == "left" else RIGHT_LANDMARKS

    nose_index = 0
    
    # Get relevant landmarks
    index = landmarks[side_dict["INDEX"]]
    nose = landmarks[nose_index]
    
    # Calculate distance in x-y plane
    dx = index.x - nose.x
    dy = index.y - nose.y
    
    return math.sqrt(dx*dx + dy*dy)


def calculate_forearm_pronation_x_axis(landmarks, side="left"):
    """
    Calculate the forearm pronation angle.
    Compares the position of the thumb, index and pinky fingers in the X axis.
    For the right side:
        If the pinky finger is right of the thumb and the index, the pronation is 2.
        If the index finger is right on top of the thumb, the pronation is 1.
        If the pinky finger is left of the thumb and the index, the pronation is 0
    Opposite for the left side.
    """
    side_dict = LEFT_LANDMARKS if side == "left" else RIGHT_LANDMARKS

    # Get relevant landmarks
    thumb = landmarks[side_dict["THUMB"]]
    index = landmarks[side_dict["INDEX"]]
    pinky = landmarks[side_dict["PINKY"]]

    # Get x coordinates
    thumb_x = thumb.x
    index_x = index.x
    pinky_x = pinky.x

    if side == "right":
        # For right side
        if abs(index_x - thumb_x) < 0.001:  # Index and thumb aligned
            return 1  # Neutral position
        elif pinky_x > index_x:
            return 2  # Pronation
        else:
            return 0  # Supination
    else:
        # For left side (opposite logic)
        if abs(index_x - thumb_x) < 0.001:  # Index and thumb aligned
            return 1  # Neutral position
        elif pinky_x < index_x:
            return 2  # Pronation
        else:
            return 0  # Supination

def calculate_forearm_pronation_y_axis(landmarks, side="left"):
    """
    Calculate the forearm pronation angle based on Y-axis positions.
    Compares the position of the thumb and pinky fingers in the Y axis.
    For both sides:
        If the thumb is below the pinky, the pronation is 0 (supination)
        If the thumb is at the same height as the pinky, the pronation is 1 (neutral)
        If the thumb is above the pinky, the pronation is 2 (pronation)
    """
    side_dict = LEFT_LANDMARKS if side == "left" else RIGHT_LANDMARKS

    # Get relevant landmarks
    thumb = landmarks[side_dict["THUMB"]]
    pinky = landmarks[side_dict["PINKY"]]

    # Get y coordinates
    thumb_y = thumb.y
    pinky_y = pinky.y

    if abs(thumb_y - pinky_y) < 0.005:  # Thumb and pinky at same height
        return 1  # Neutral position
    elif thumb_y > pinky_y:  # Thumb is below pinky
        return 0  # Pronation
    else:
        return 2  # Supination







import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

def draw_landmarks(rgb_image, detection_result):
    annotated_image = rgb_image.copy()
    
    if detection_result is None:
        return annotated_image
    
    if detection_result.pose_landmarks:
        for pose_landmarks in detection_result.pose_landmarks:
            pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            # Always take exactly 33 landmarks (0-32), ignore any gesture strings after that
            pose_landmarks_to_draw = pose_landmarks[:33]
            
            pose_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(
                    x=landmark.x, 
                    y=landmark.y, 
                    z=landmark.z,
                    visibility=landmark.visibility if hasattr(landmark, 'visibility') else 1.0
                ) 
                for landmark in pose_landmarks_to_draw
            ])
            solutions.drawing_utils.draw_landmarks(
                annotated_image,
                pose_landmarks_proto,
                solutions.pose.POSE_CONNECTIONS,
                solutions.drawing_styles.get_default_pose_landmarks_style())
    
    return annotated_image 
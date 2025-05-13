import cv2
import numpy as np
import os

class ExerciseInterface:
    def __init__(self, window_name="Fugl Meyer Assessment"):
        self.window_name = window_name

        cv2.namedWindow(self.window_name, cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow(self.window_name, 1280, 480)
        
    def create_split_screen(self, frame, exercise, evaluator, metrics=None, time_remaining=None):
        height, width = frame.shape[:2]
        canvas = np.zeros((height, width * 2, 3), dtype=np.uint8)
        
        # Copy the frame to the right side
        canvas[:, width:] = frame
        
        current_side = evaluator.current_assessment_side
        actual_side = evaluator.get_actual_side()
        
        # Draw instructions on the left panel without current side and timer
        self._draw_instructions(canvas[:, :width], exercise, metrics, current_side, actual_side)
        
        # Add current side and timer to the camera view (right panel)
        self._draw_camera_overlay(canvas[:, width:], current_side, actual_side, time_remaining)
        
        return canvas
    
    def _draw_camera_overlay(self, camera_view, current_side, actual_side, time_remaining=None):
        height, width = camera_view.shape[:2]
        
        overlay = camera_view.copy()
        cv2.rectangle(overlay, (0, 0), (width, 45), (0, 0, 0), -1)
        alpha = 0.2
        cv2.addWeighted(overlay, alpha, camera_view, 1 - alpha, 0, camera_view)
        
        # Draw side information
        side_color = (0, 255, 255) if current_side == "unaffected" else (0, 200, 255)
        cv2.putText(camera_view, f"Current side: {actual_side} ({current_side})", (20, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, side_color, 2)
        
        # Display time remaining if provided
        if time_remaining is not None:
            time_color = (0, 255, 0) if time_remaining > 10 else (0, 0, 255)
            cv2.putText(camera_view, f"Time remaining: {time_remaining}s", (width - 250, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, time_color, 2)
        
    def _draw_instructions(self, canvas, exercise, metrics=None, current_side="affected", actual_side="right"):
        height, width = canvas.shape[:2]
    
        canvas[:, :] = (50, 50, 50)
        
        cv2.putText(canvas, "Exercise Instructions", (20, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        cv2.line(canvas, (10, 60), (width-10, 60), (200, 200, 200), 1)
        
        exercise_name = exercise.get("name", "Unknown Exercise")
        cv2.putText(canvas, exercise_name, (20, 90), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        
        description = exercise.get("description", "")
        cv2.putText(canvas, description, (20, 120), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        instruction_text = exercise.get("instructions", "")
        if current_side == "unaffected":
            instruction_text = instruction_text.replace("affected arm", "unaffected arm")
            
        y_position = 150
        
        words = instruction_text.split()
        line = ""
        for word in words:
            test_line = line + word + " "
            text_size = cv2.getTextSize(test_line, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0]
            
            if text_size[0] > width - 40:
                cv2.putText(canvas, line, (20, y_position), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                y_position += 30
                line = word + " "
            else:
                line = test_line
        
        if line:
            cv2.putText(canvas, line, (20, y_position), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            y_position += 40
        
        if metrics:
            cv2.putText(canvas, "Current Measurements:", (20, y_position), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 1)
            y_position += 30
            
            for key, value in metrics.items():
                if isinstance(value, float):
                    metric_text = f"{key}: {value:.1f} degrees"
                elif isinstance(value, bool):
                    metric_text = f"{key}: {'Yes' if value else 'No'}"
                else:
                    metric_text = f"{key}: {value}"
                
                cv2.putText(canvas, metric_text, (30, y_position), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 255), 1)
                y_position += 25
            
            y_position += 15
        
        reference_image_path = None
        reference_images = exercise.get("reference_image", {})
        reference_image_path = reference_images.get(actual_side)

        if reference_image_path and os.path.exists(reference_image_path):
            try:
                ref_img = cv2.imread(reference_image_path)
                if ref_img is not None:
                    img_height, img_width = ref_img.shape[:2]
                    aspect_ratio = img_width / img_height
                    new_width = width - 40
                    new_height = int(new_width / aspect_ratio)
                    
                    resized_img = cv2.resize(ref_img, (new_width, new_height))
                    
                    y_start = y_position
                    if y_start + new_height < height - 100:
                        canvas[y_start:y_start+new_height, 20:20+new_width] = resized_img
            except Exception as e:
                print(f"Error loading reference image: {e}")


        
    def display(self, canvas):
        cv2.imshow(self.window_name, canvas)
        
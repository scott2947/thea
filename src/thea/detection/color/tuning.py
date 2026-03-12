import cv2, os
import numpy as np
from datetime import datetime
from thea.morse import play_morse_pattern


is_tuning = False
def tune(frame: np.ndarray) -> None:
    global is_tuning
    if is_tuning: return
    is_tuning = True
    
    play_morse_pattern("-")

    h_steps, s_steps, v_min = [26, 29, 32], [80, 100, 120], 50
    upper_bound = np.array([60, 255, 255])

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    
    results_list = []
    for h_low in h_steps:
        for s_low in s_steps:
            lower_bound = np.array([h_low, s_low, v_min])
            
            mask = cv2.inRange(hsv, lower_bound, upper_bound)
            mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=3)
            mask_3ch = cv2.cvtColor(mask_cleaned, cv2.COLOR_GRAY2BGR)

            annotated = frame.copy()
            label = f"L:[{h_low},{s_low},{v_min}] U:[60,255,255]"
            cv2.putText(annotated, label, (10, frame.shape[0] - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            results_list.append(np.hstack((annotated, mask_3ch)))

    if results_list:
        final_stack = np.vstack(results_list)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = "storage/tuning_results"
        
        filepath = os.path.join(output_dir, f"hsv_sweep_{timestamp}.jpg")
        cv2.imwrite(filepath, final_stack)
        print(f"Saved tuning image: {filepath}")

    play_morse_pattern(".")


if __name__ == "__main__":
    pass

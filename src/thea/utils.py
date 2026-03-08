import numpy as np
def calculate_average(frame: np.ndarray) -> None:
    b, r, g = np.mean(frame, axis=(0, 1))
    print(f"B: {b:.1f} G: {g:.1f} R: {r:.1f} ", end="\r")


import cv2
def identify_coordinates_hsv(frame: np.ndarray) -> None:
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_bound, upper_bound = np.array([29, 120, 50]), np.array([60, 255, 255])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=3)

    num_labels, _, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)
    for i in range(1, num_labels):
        if stats[i, cv2.CC_STAT_AREA] > 200:
            cx, cy = centroids[i]
            print(f"Ball {i}: Centre = ({int(cx)}, {int(cy)}, Area={stats[i, cv2.CC_STAT_AREA]})")

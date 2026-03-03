import numpy as np
import cv2


def calculate_average(frame: np.ndarray) -> None:
    b, r, g = np.mean(frame, axis=(0, 1))
    print(f"B: {b:.1f} G: {g:.1f} R: {r:.1f} ", end="\r")


def identify_coordinates(frame: np.ndarray) -> None:
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # lower_bound = np.array([80, 110, 55])
    # upper_bound = np.array([95, 255, 255])

    lower_bound = np.array([30, 100, 100])
    upper_bound = np.array([70, 255, 255])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.erode(mask, kernel, iterations=3)
    mask = cv2.dilate(mask, kernel, iterations=3)

    num_labels, _, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)

    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]

        cx, cy = centroids[i]

        if area > 200:
            print(f"Ball {i}: Centre = ({int(cx)}, {int(cy)}, Area={area})")

import cv2
import numpy as np
from thea.detection.base import BaseDetector


class ColorDetector(BaseDetector):
    def detect_targets(self, frame: np.ndarray) -> np.ndarray:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_bound, upper_bound = np.array([29, 120, 50]), np.array([60, 255, 255])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=3)

        num_labels, _, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)
        targets = []
        for i in range(1, num_labels):
            if stats[i, cv2.CC_STAT_AREA] > 100:
                cx, cy = centroids[i]
                targets.append([int(cx), int(cy)])

        return np.array(targets)

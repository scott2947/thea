import numpy as np


def calculate_average(frame: np.ndarray) -> tuple[float, float, float]:
    avg_color = np.mean(frame, axis=(0, 1))
    return float(avg_color[0]), float(avg_color[1]), float(avg_color[2])

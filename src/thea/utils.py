import numpy as np
def calculate_average(frame: np.ndarray) -> tuple[float, float, float]:
    b, g, r = np.mean(frame, axis=(0, 1))
    return b, g, r


if __name__ == "__main__":
    pass

import numpy as np
def calculate_average(frame: np.ndarray) -> None:
    b, r, g = np.mean(frame, axis=(0, 1))
    print(f"B: {b:.1f} G: {g:.1f} R: {r:.1f} ", end="\r")


if __name__ == "__main__":
    pass

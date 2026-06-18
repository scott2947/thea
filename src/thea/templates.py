from dataclasses import dataclass
import numpy as np


@dataclass
class VisionFrame:
    frame: np.ndarray
    timestamp: float
    received_at: float

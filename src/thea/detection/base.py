import numpy as np
from abc import ABC, abstractmethod


class BaseDetector(ABC):
    @abstractmethod
    def detect_targets(self, frame: np.ndarray) -> np.ndarray:
        pass


if __name__ == "__main__":
    pass

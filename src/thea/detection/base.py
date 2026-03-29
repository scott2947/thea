import numpy as np
from abc import ABC, abstractmethod


class BaseDetector(ABC):
    @abstractmethod
    def detect(self, frame: np.ndarray) -> list:
        pass


if __name__ == "__main__":
    pass

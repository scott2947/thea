import numpy as np
from abc import ABC, abstractmethod


class BasePlanner(ABC):
    @abstractmethod
    def plan_commands(self, coords: np.ndarray) -> np.ndarray:
        return np.array(["forward", "backward", "left", "right"])


if __name__ == "__main__":
    pass

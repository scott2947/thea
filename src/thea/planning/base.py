import numpy as np
from abc import ABC, abstractmethod


class BasePlanner(ABC):
    @abstractmethod
    def plan(self, coords: list) -> dict:
        pass


if __name__ == "__main__":
    pass

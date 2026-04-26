from abc import ABC, abstractmethod


class BasePlanner(ABC):
    @abstractmethod
    def plan(self, coords: list, timestamp: float) -> tuple:
        pass


if __name__ == "__main__":
    pass

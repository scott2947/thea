import numpy as np
from thea.pipeline import Pipeline
from thea.detection.color.detector import ColorDetector
from thea.planning.base import BasePlanner


class DefaultPlanner(BasePlanner):
    def plan_commands(self, coords: np.ndarray) -> np.ndarray:
        return super().plan_commands(coords)


if __name__ == "__main__":
    pl = Pipeline("colour-tracking", ColorDetector(), DefaultPlanner())
    pl.start()
    pl.run()

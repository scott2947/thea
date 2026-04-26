import math
from thea.planning.base import BasePlanner
from thea.planning.head.pid import PIDController
from thea.config import GRID_WIDTH, GRID_HEIGHT

DEAD_ZONE = 0.04  # 4% of frame dimension


class HeadPlanner(BasePlanner):
    def __init__(self):
        self.mid_x = GRID_WIDTH / 2
        self.mid_y = GRID_HEIGHT / 2
        self.pan_pid = PIDController(kp=25, ki=0.1, kd=0.72) # 19.2, 0.72
        self.tilt_pid = PIDController(kp=12, ki=0.1, kd=0.45) # 12, 0.45

    def plan(self, coords: list, timestamp: float) -> tuple:
        target = min(coords, key=lambda c: math.hypot(c[0] - self.mid_x, c[1] - self.mid_y), default=None)
        if target is None:
            return (0.0, 0.0)

        error_x = (target[0] - self.mid_x) / GRID_WIDTH
        error_y = (target[1] - self.mid_y) / GRID_HEIGHT

        dpan  = -self.pan_pid.update(error_x, timestamp) if abs(error_x) > DEAD_ZONE else 0.0 # image flipped on RPI
        dtilt = -self.tilt_pid.update(error_y, timestamp) if abs(error_y) > DEAD_ZONE else 0.0

        return (dpan, dtilt)


if __name__ == "__main__":
    pass

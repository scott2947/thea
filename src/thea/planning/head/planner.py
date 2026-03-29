import math
from thea.planning.base import BasePlanner
from thea.config import GRID_WIDTH, GRID_HEIGHT, H_FOV, V_FOV


class HeadPlanner(BasePlanner):
    def __init__(self):
        self.mid_x, self.mid_y = GRID_WIDTH / 2, GRID_HEIGHT / 2
        self.f_x = self.mid_x / math.tan(math.radians(H_FOV / 2))
        self.f_y = self.mid_y / math.tan(math.radians(V_FOV / 2))

    def plan(self, coords: list) -> dict:
        target = min(coords, key=lambda c: math.hypot(c[0] - self.mid_x, c[1] - self.mid_y), default=None)
        if target is None:
            return {}
        
        x, y = target[0], target[1]
        
        offset_x = x - self.mid_x
        offset_y = y - self.mid_y

        angle_x = math.degrees(math.atan(offset_x / self.f_x))
        angle_y = math.degrees(math.atan(offset_y / self.f_y))

        return {"x": angle_x, "y": angle_y}


if __name__ == "__main__":
    pass

import numpy as np
from thea.planning.base import BasePlanner
from thea.config import GRID_WIDTH, GRID_HEIGHT


class HeadPlanner(BasePlanner):
    def plan_commands(self, coords: np.ndarray) -> np.ndarray:
        coords = coords.tolist()
        commands = []

        if len(coords) == 1:
            x, y = coords[0]
            
            if x < GRID_WIDTH / 2:
                commands.append("right")
            elif x > GRID_WIDTH / 2:
                commands.append("left")
            
            if y < GRID_HEIGHT / 2:
                commands.append("up")
            elif y > GRID_HEIGHT / 2:
                commands.append("down")
        
        return np.array(commands)


if __name__ == "__main__":
    hp = HeadPlanner()
    cmds = hp.plan_commands(np.array([[6, 6]]))
    print(cmds)

import queue
from thea.planning.base import BasePlanner


class PlanningProcessor:
    def __init__(self, coord_queue: queue.Queue[tuple], command_queue: queue.Queue[tuple], planner: BasePlanner):
        self.coord_queue = coord_queue
        self.command_queue = command_queue
        self.planner = planner
        self.running = False

    def start(self) -> None:
        self.running = True

    def run(self) -> None:
        while self.running:
            try:
                coords, timestamp = self.coord_queue.get()
                command = self.planner.plan(coords, timestamp)
                self.command_queue.put(command)
                self.coord_queue.task_done()
            except queue.Empty:
                pass
            except queue.Full:
                pass

    def stop(self) -> None:
        self.running = False


if __name__ == "__main__":
    pass

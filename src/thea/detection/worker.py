import queue
import numpy as np
from thea.detection.base import BaseDetector


class DetectionProcessor:
    def __init__(self, frame_queue: queue.Queue[np.ndarray], coord_queue: queue.Queue[np.ndarray], detector: BaseDetector):
        self.frame_queue = frame_queue
        self.coord_queue = coord_queue
        self.detector = detector
        self.running = False
    

    def start(self) -> None:
        self.running = True
    

    def run(self) -> None:
        while self.running:
            try:
                frame = self.frame_queue.get()
                coords = self.detector.detect_targets(frame)
                self.coord_queue.put(coords)
                self.frame_queue.task_done()
            except queue.Empty:
                pass
            except queue.Full:
                pass
    

    def stop(self) -> None:
        self.running = False


if __name__ == "__main__":
    pass

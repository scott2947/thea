import queue
from thea.templates import VisionFrame
from thea.detection.base import BaseDetector


class DetectionProcessor:
    def __init__(self, frame_queue: queue.Queue[VisionFrame], coord_queue: queue.Queue[tuple], detector: BaseDetector):
        self.frame_queue = frame_queue
        self.coord_queue = coord_queue
        self.detector = detector
        self.running = False

    def start(self) -> None:
        self.running = True

    def run(self) -> None:
        while self.running:
            try:
                vision_frame = self.frame_queue.get()
                coords = self.detector.detect(vision_frame.frame)
                self.coord_queue.put((coords, vision_frame.timestamp))
                self.frame_queue.task_done()
            except queue.Empty:
                pass
            except queue.Full:
                pass

    def stop(self) -> None:
        self.running = False


if __name__ == "__main__":
    pass

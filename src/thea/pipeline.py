import queue, threading
from thea.detection.base import BaseDetector
from thea.planning.base import BasePlanner
from thea.network.frame_worker import FrameProducer
from thea.detection.worker import DetectionProcessor
from thea.planning.worker import PlanningProcessor
from thea.network.command_worker import CommandConsumer
from thea.network.server import TCPServer


class Pipeline:
    def __init__(self, name: str, detector: BaseDetector, planner: BasePlanner):
        self.name = name
        self.detector = detector
        self.planner = planner

    def build(self) -> None:
        self.server = TCPServer()

        frame_queue = queue.Queue(maxsize=10)
        self.frame_producer = FrameProducer(frame_queue, self.server)
        coord_queue = queue.Queue(maxsize=30)
        self.detection_processor = DetectionProcessor(frame_queue, coord_queue, self.detector)
        command_queue = queue.Queue(maxsize=30)
        self.planning_processor = PlanningProcessor(coord_queue, command_queue, self.planner)
        self.command_consumer = CommandConsumer(command_queue, self.server)

        self.frame_producer_thread = threading.Thread(target=self.frame_producer.run, daemon=True)
        self.detection_processor_thread = threading.Thread(target=self.detection_processor.run, daemon=True)
        self.planning_processor_thread = threading.Thread(target=self.planning_processor.run, daemon=True)
        self.command_consumer_thread = threading.Thread(target=self.command_consumer.run, daemon=True)

    def start(self) -> None:
        self.server.start_server()
        self.server.receive()

        self.frame_producer.start()
        self.detection_processor.start()
        self.planning_processor.start()
        self.command_consumer.start()

        self.frame_producer_thread.start()
        self.detection_processor_thread.start()
        self.planning_processor_thread.start()
        self.command_consumer_thread.start()

        try:
            self.frame_producer_thread.join()
            self.detection_processor_thread.join()
            self.planning_processor_thread.join()
            self.command_consumer_thread.join()
        except KeyboardInterrupt:
            self.stop()

    def stop(self) -> None:
        self.frame_producer.stop()
        self.detection_processor.stop()
        self.planning_processor.stop()
        self.command_consumer.stop()
        self.server.close_server()


if __name__ == "__main__":
    pass

import cv2
import numpy as np
import queue
import threading
from thea.network.server import UDPServer
from thea.network.processing import calculate_average


class VideoProducer:
    def __init__(self, server: UDPServer, frame_queue: queue.Queue[np.ndarray]):
        self.server = server
        self.frame_queue = frame_queue
        self.running = True


    def run(self) -> None:
        while self.running:
            try:
                data = self.server.receive()
                if data:
                    nparr = np.frombuffer(data, np.uint8)
                    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    if frame is not None:
                        try:
                            self.frame_queue.put_nowait(frame)
                        except queue.Full:
                            pass
            except Exception:
                pass


class VideoConsumer:
    def __init__(self, frame_queue: queue.Queue[np.ndarray], operation):
        self.frame_queue = frame_queue
        self.operation = operation
        self.running = True


    def run(self) -> None:
        while self.running:
            try:
                frame = self.frame_queue.get()
                self.operation(frame)
                self.frame_queue.task_done()
            except Exception:
                pass


class VideoController:
    def __init__(self, operation) -> None:
        self.server = UDPServer()
        self.shared_queue = queue.Queue(maxsize=30)

        self.producer = VideoProducer(self.server, self.shared_queue)
        self.consumer = VideoConsumer(self.shared_queue, operation)

        self.producer_thread = threading.Thread(target=self.producer.run, daemon=True)
        self.consumer_thread = threading.Thread(target=self.consumer.run, daemon=True)
    
    
    def start(self) -> None:
        self.server.start_server()

        self.producer_thread.start()
        self.consumer_thread.start()

        try:
            self.producer_thread.join()
            self.consumer_thread.join()
        except KeyboardInterrupt:
            self.producer.running = False
            self.consumer.running = False
            self.server.close_server()


if __name__ == "__main__":
    vc = VideoController(calculate_average)
    vc.start()

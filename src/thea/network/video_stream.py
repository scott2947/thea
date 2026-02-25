import cv2
import numpy as np
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
                    frame: np.ndarray | None = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    if frame is not None:
                        try:
                            self.frame_queue.put_nowait(frame)
                        except queue.Full:
                            pass
            except Exception:
                pass

class VideoConsumer:
    def __init__(self, frame_queue: queue.Queue[np.ndarray]):
        self.frame_queue = frame_queue
        self.running = True

    def run(self) -> None:
        while self.running:
            try:
                frame = self.frame_queue.get()
                b, g, r = calculate_average(frame)
                print(f"B: {b:.1f} G: {g:.1f} R: {r:.1f} | Queue: {self.frame_queue.qsize()}  ", end="\r")
                self.frame_queue.task_done()
            except Exception:
                pass

if __name__ == "__main__":
    import queue
    import threading
    
    server = UDPServer()
    server.start_server()
    
    shared_queue: queue.Queue[np.ndarray] = queue.Queue(maxsize=10)
    
    producer = VideoProducer(server, shared_queue)
    consumer = VideoConsumer(shared_queue)

    producer_thread = threading.Thread(target=producer.run, daemon=True)
    consumer_thread = threading.Thread(target=consumer.run, daemon=True)

    producer_thread.start()
    consumer_thread.start()

    try:
        producer_thread.join()
        consumer_thread.join()
    except KeyboardInterrupt:
        producer.running = False
        consumer.running = False
        server.close_server()


## Look at using multiprocessing.Process, synchronisation (with Events not Booleans), Poison Pills

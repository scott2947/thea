import queue, cv2
import numpy as np
from thea.network.server import UDPServer


class FrameWorker:
    def __init__(self, frame_queue: queue.Queue[np.ndarray]):
        self.frame_queue = frame_queue
        self.server = UDPServer()
        self.running = False

    
    def start(self) -> None:
        self.server.start_server()
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
    

    def stop(self) -> None:
        self.running = False
        self.server.close_server()


if __name__ == "__main__":
    pass

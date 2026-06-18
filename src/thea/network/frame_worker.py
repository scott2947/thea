import queue, cv2, struct, time
import numpy as np
from thea.network.server import TCPServer
from thea.templates import VisionFrame

HEADER_SIZE = 8


class FrameProducer:
    def __init__(self, frame_queue: queue.Queue[VisionFrame], server: TCPServer):
        self.frame_queue = frame_queue
        self.server = server
        self.running = False

    def start(self) -> None:
        self.running = True

    def run(self) -> None:
        while self.running:
            try:
                data = self.server.receive()
                if data:
                    timestamp, = struct.unpack('>d', data[:HEADER_SIZE])
                    frame = cv2.imdecode(np.frombuffer(data[HEADER_SIZE:], dtype=np.uint8), cv2.IMREAD_COLOR)
                    if frame is not None:
                        vision_frame = VisionFrame(frame=frame, timestamp=timestamp, received_at=time.monotonic())
                        try:
                            self.frame_queue.put_nowait(vision_frame)
                        except queue.Full:
                            pass
            except Exception:
                pass

    def stop(self) -> None:
        self.running = False


if __name__ == "__main__":
    pass

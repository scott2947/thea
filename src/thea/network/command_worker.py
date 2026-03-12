import queue
import numpy as np
from thea.network.server import TCPServer


class CommandConsumer:
    def __init__(self, command_queue: queue.Queue[np.ndarray]):
        self.command_queue = command_queue
        self.server = TCPServer()
        self.running = False
    

    def start(self) -> None:
        self.server.start_server()
        self.server.receive() # Client hello
        self.running = True

    
    def run(self) -> None:
        while self.running:
            try:
                command = self.command_queue.get()
                self.server.send(command.tobytes())
                self.command_queue.task_done()
            except queue.Empty:
                pass

    
    def stop(self) -> None:
        self.running = False
        self.server.close_server()


if __name__ == "__main__":
    pass

import queue, struct
from thea.network.server import TCPServer


class CommandConsumer:
    def __init__(self, command_queue: queue.Queue[tuple], server: TCPServer):
        self.command_queue = command_queue
        self.server = server
        self.running = False

    def start(self) -> None:
        self.running = True

    def run(self) -> None:
        while self.running:
            try:
                command = self.command_queue.get()
                self.server.send(struct.pack('>2f', command[0], command[1]))
                self.command_queue.task_done()
            except queue.Empty:
                pass

    def stop(self) -> None:
        self.running = False


if __name__ == "__main__":
    pass

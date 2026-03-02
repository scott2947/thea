import random
import time
from thea.network.server import TCPServer

class CommandSender:

    def __init__(self):
        self.commands = ["forward", "backward", "left", "right", "do a barrel roll"]
        self.server = TCPServer()
    

    def stream(self) -> None:

        self.server.start_server()
        self.server.receive() ## client hello

        print("Streaming started. Press Ctrl+C to stop")

        try:
            while True:
                command = random.choice(self.commands)
                self.server.send_string(command)
                time.sleep(0.5)
        
        except KeyboardInterrupt:
            print("Streaming stopped by user")
        except Exception as e:
            print(f"Error during streaming: {e}")
        finally:
            self.server.close_server()



if __name__ == "__main__":
    cs = CommandSender()
    cs.stream()

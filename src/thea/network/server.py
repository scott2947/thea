from abc import ABC, abstractmethod
import socket, struct
from thea.config import HOST, PORT

class BaseServer(ABC):

    def __init__(self):
        self.socket : socket.socket

    
    @abstractmethod
    def start_server(self):
        pass


    def close_server(self) -> None:
        self.socket.close()


    @abstractmethod
    def receive(self) -> bytes:
        pass


class TCPServer(BaseServer):

    def __init__(self):
        super().__init__()
        self.conn : socket.socket


    def start_server(self) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen()

        self.socket = s
        print(f"TCP Server started on {HOST}:{PORT}")
    

    def close_server(self) -> None:
        super().close_server()
        print("TCP Server closed")


    def accept_connection(self) -> None:
        self.conn, addr = self.socket.accept()
        print(f"Connected by {addr}")

    
    def close_connection(self) -> None:
        self.conn.close()
        print("Connection closed")
    
    
    def receive(self) -> bytes:
        header = self.conn.recv(4)
        message_length = struct.unpack(">I", header)[0]
        message = b""

        while len(message) < message_length:
            data = self.conn.recv(4096)
            if not data:
                break
            message += data
        
        print("Data received")
        return message
    

class UDPServer(BaseServer):

    def start_server(self) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((HOST, PORT))

        self.socket = s
        print(f"UDP Server started on {HOST}:{PORT}")
    

    def close_server(self) -> None:
        super().close_server()
        print("UDP Server closed")
    

    def receive(self) -> bytes:
        data, addr = self.socket.recvfrom(4096)
        print(f"Data received from {addr}")
        return data


if __name__ == "__main__":
    pass

## Look up the Liskov substitution principle - this code needs refactoring

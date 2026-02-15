from abc import ABC, abstractmethod
import socket, struct
from thea.config import HOST, PORT

class BaseServer(ABC):

    def __init__(self):
        self.socket = None


    @abstractmethod
    def start_server(self):
        pass


    @abstractmethod
    def receive(self) -> bytes:
        pass


    def receive_string(self) -> str:
        data = self.receive()
        if not data:
            return ""
        
        return data.decode("utf-16")


    def close_server(self) -> None:
        if self.socket:
            self.socket.close()
            self.socket = None


class TCPServer(BaseServer):

    def __init__(self):
        super().__init__()
        self.conn = None


    def start_server(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((HOST, PORT))
        self.socket.listen(1)
        print(f"TCP Server started on {HOST}:{PORT}")


    def _recv_exactly(self, n: int) -> bytes:
        assert self.conn is not None, "Connection was lost or not established"

        data = b''
        while len(data) < n:
            packet = self.conn.recv(n - len(data))
            if not packet:
                return b''
            data += packet
        return data


    def receive(self) -> bytes:

        if not self.socket:
            raise RuntimeError("Server not started. Call start_server() first.")

        if self.conn is None:
            print("TCP Server waiting for a connection")
            self.conn, addr = self.socket.accept()
            print(f"TCP Server connected by {addr}")

        try:
            header = self._recv_exactly(4)
            if not header:
                self.close_connection()
                return b""
            
            message_length = struct.unpack(">I", header)[0]
            message = self._recv_exactly(message_length)
            return message
        
        except Exception as e:
            print(f"TCP Server receive error: {e}")
            self.close_connection()
            return b""
        

    def close_connection(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None
            print("TCP connection closed")


    def close_server(self) -> None:
        self.close_connection()
        super().close_server()
        print("TCP Server closed")


class UDPServer(BaseServer):

    def start_server(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((HOST, PORT))
        print(f"UDP Server started on {HOST}:{PORT}")


    def receive(self) -> bytes:
        if not self.socket:
            raise RuntimeError("Server not started.")
        
        data, _ = self.socket.recvfrom(65535)
        return data


    def close_server(self) -> None:
        super().close_server()
        print("UDP Server closed")


if __name__ == "__main__":
    server = TCPServer()
    server.start_server()
    message = server.receive_string()
    print(message)
    server.close_server()

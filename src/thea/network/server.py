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


    @abstractmethod
    def send(self, data: bytes) -> None:
        pass

    
    def send_string(self, message: str) -> None:
        data = message.encode("utf-16")
        self.send(data)


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
        
        if not self.conn:
            raise RuntimeError("Connection lost or closed by client")

        data = b''
        while len(data) < n:
            packet = self.conn.recv(n - len(data))
            if not packet:
                return b''
            data += packet
        return data
    

    def _connect(self) -> None:

        if not self.socket:
            raise RuntimeError("Server not started. Call start_server() first")
        
        if self.conn is None:
            print("TCP Server waiting for a connection")
            self.conn, addr = self.socket.accept()
            print(f"TCP Server connected by {addr}")


    def receive(self) -> bytes:

        self._connect()

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
        

    def send(self, data: bytes) -> None:
        
        self._connect()

        if not self.conn:
            raise RuntimeError("Connection lost or closed by client")

        try:
            header = struct.pack(">I", len(data))
            self.conn.sendall(header + data)
        
        except Exception as e:
            print(f"TCP Server send error: {e}")
            self.close_connection()
        

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

    def __init__(self):
        super().__init__()
        self.addr = None

    def start_server(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((HOST, PORT))
        print(f"UDP Server started on {HOST}:{PORT}")


    def receive(self) -> bytes:
        if not self.socket:
            raise RuntimeError("Server not started. Call start_server() first")
        
        data, self.addr = self.socket.recvfrom(65535)
        return data


    def send(self, data: bytes) -> None:
        
        if not self.socket:
            raise RuntimeError("Server not started. Call start_server() first")
        
        if not self.addr:
            raise RuntimeError("Client not helloed")
        
        self.socket.sendto(data, self.addr)


    def close_server(self) -> None:
        super().close_server()
        print("UDP Server closed")


if __name__ == "__main__":
    pass

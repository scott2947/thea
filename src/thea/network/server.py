import socket, struct
from thea.config import HOST, PORT


def start_server() -> socket.socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()

    print(f"SERVER STARTED ON {HOST}:{PORT}")

    return s


def close_server(s : socket.socket) -> None:
    print("SERVER CLOSED")
    s.close()


def accept_connection(s : socket.socket) -> socket.socket:
    conn, addr = s.accept()
    print(f"CONNECTED BY {addr}")
    return conn


def close_connection(conn : socket.socket):
    print("CONNECTION CLOSED")
    conn.close()


def receive_data(conn : socket.socket) -> bytes:
    header = conn.recv(4)
    message_length = struct.unpack(">I", header)[0]
    message = b""

    while len(message) < message_length:
        data = conn.recv(4096)
        if not data:
            break
        message += data
    
    print("DATA RECEIVED")
    return message


def receive_text(s : socket.socket) -> str:
    data = receive_data(s)
    return data.decode()


if __name__ == "__main__":
    s = start_server()
    conn = accept_connection(s)
    message = receive_text(conn)
    close_connection(conn)
    close_server(s)
    print(message)

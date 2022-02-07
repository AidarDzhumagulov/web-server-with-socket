import socket

from handler import Handler


class App:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

        self.sock: socket.socket = None

    def __enter__(self) -> "App":
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()

    def run(self):
        while True:
            connection, address = self.sock.accept()
            try:
                data = self._get_request_data(connection)
                req_data = data.decode("utf-8").strip().split("\r\n")

                method = req_data[0].split()[0]
                result = Handler(method, req_data).handle()

                connection.send(result.encode('utf-8'))
            except Exception as e:
                print(e)
                connection.close()
            connection.close()

    @staticmethod
    def _get_request_data(conn: socket) -> bytes:
        full_data = b''
        while True:
            data = conn.recv(1024)
            full_data += data
            if data.endswith(b"\r\n\r\n"):
                break
        return full_data






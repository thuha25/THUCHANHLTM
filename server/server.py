import socket
from threading import Thread
import logger

HOST = ""
PORT = 8000


class Server:
    def __init__(self, host=HOST, port=PORT, max_clients=8, handler=None):
        self.host = host
        self.port = port
        self.max_clients = max_clients
        self.handler = handler
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen(max_clients)
        self.client_threads = []
        logger.log(f"Server started at {host}:{port}")

    def start(self):
        try:
            while True:
                client, addr = self.server.accept()
                logger.log(f"Connection from: {addr}")
                if self.handler:
                    t = Thread(target=self.handler, args=(self, client, addr))
                    t.start()
                    self.client_threads.append(t)
        except KeyboardInterrupt:
            print("Stopped by Ctrl+C")
        finally:
            if self.server:
                self.server.close()
            for t in self.client_threads:
                t.join()


if __name__ == "__main__":
    server = Server()
    server.start()

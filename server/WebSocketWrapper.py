class CustomWebSocket:
    def __init__(self, raw_socket, server):
        self.raw_socket = raw_socket
        self.server = server

    def send(self, message: str):
        self.server.send_message(self.raw_socket, message)

    def receive(self):
        return self.server.receive_message(self.raw_socket)
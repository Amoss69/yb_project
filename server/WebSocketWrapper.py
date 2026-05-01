from logger import log

class CustomWebSocket:
    def __init__(self, raw_socket, server):
        self.raw_socket = raw_socket
        self.server = server

    def send(self, message: str):

        client = str(self.raw_socket.getpeername())
        log("OUT", client, message)

        self.server.send_message(self.raw_socket, message)

    def receive(self):

        message = self.server.receive_message(self.raw_socket)
        if message:
            client = str(self.raw_socket.getpeername())
            log("IN", client, message)
        return message
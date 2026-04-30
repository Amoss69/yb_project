import socket
import ssl
import base64
import hashlib
import threading

from sympy import false

from WebSocketWrapper import CustomWebSocket

CLOSE_OPCODE = 8
PING_OPCODE = 9
PONG_OPCODE = 10
TEXT_OPCODE = 1


class CustomWebSocketServer:
    def __init__(self, host, port, handler):
        self.host = host
        self.port = port
        self.handle_client = handler
        self.clients = []
        self.lock = threading.Lock()

    def start_websocket(self):
        #context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        #context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

        server = socket.socket()
        server.bind((self.host, self.port))
        server.listen()
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            raw_client, addr = server.accept()
            print(f"New connection from {addr}")


            #client = context.wrap_socket(raw_client, server_side=True)

            handshake = self.receive_and_send_handshake(raw_client)
            if not handshake:
                continue #if handshake didn't work skip the client

            websocket = CustomWebSocket(raw_client, self)

            with self.lock:
                self.clients.append(websocket)


            t = threading.Thread(target=self.handle_client, args=(websocket,), daemon=True)
            t.start()



    def receive_and_send_handshake(self, client):
        request = b""

        while b'\r\n\r\n' not in request:
            data = client.recv(1024)
            if not data:
                break
            request += data
        try:
            request = request.decode()
            key = None
            for line in request.split("\r\n"):
                if "Sec-WebSocket-Key" in line:
                    key = line.split(": ")[1].strip()

            if key is None:
                raise Exception("No WebSocket key found in handshake")

            magic_string = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
            accept_key = base64.b64encode(
                hashlib.sha1((key + magic_string).encode()).digest()
            ).decode()

            response = (
                "HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Accept: {accept_key}\r\n\r\n"
            )
            client.send(response.encode())
            return True
        except Exception as e:
            print("Handshake error:", e)
            client.close()
            return False


    def receive_message(self, client : socket.socket):
        full_message = bytearray()

        while True:

            header = self.recv_exact(client, 2)  #get the header (2 bytes)

            if not header:
                return None

            first_byte = header[0]
            second_byte = header[1]

            fin = (first_byte >> 7) & 1 # shift right 7 times then and 1
            opcode = first_byte & 0x0F # get the opcode (second half byte)

            if opcode == CLOSE_OPCODE:
                try:
                    client.send(bytes([0b10001000, 0]))  # FIN + close opcode
                except OSError:
                    pass
                client.close()
                return None


            elif opcode == PING_OPCODE:

                ping_len = second_byte & 0b01111111
                ping_data = self.recv_exact(client, 4 + ping_len)  # 4 mask bytes + payload
                mask = ping_data[:4]
                payload = ping_data[4:]
                decoded = bytearray()
                for i in range(len(payload)):
                    decoded.append(payload[i] ^ mask[i % 4])
                self.send_pong(client, decoded)
                continue

            elif opcode == TEXT_OPCODE or opcode ==0: # if text opcode dont do anything
                pass

            else:  # if other opcode that doesn't get handle skip to the next loop
                continue




            payload_length = second_byte & 0b01111111  #7 last bits are payload length

            if payload_length == 126: # length more then one byte so real length in the 2 bytes after
                real_length = self.recv_exact(client , 2)
                real_length = int.from_bytes(real_length, "big")  # convert from bytes to int

            elif payload_length == 127:
                real_length = self.recv_exact(client, 8)
                real_length = int.from_bytes(real_length, "big")  # convert from bytes to int

            else:
                real_length = payload_length

            mask = self.recv_exact(client, 4)
            payload = self.recv_exact(client , real_length)


            # decode this frame
            decoded = bytearray()
            for i in range(len(payload)):
                decoded.append(payload[i] ^ mask[i % 4])

            # add to full message
            full_message.extend(decoded)

            # if this is the last data (first bit == 1) stop
            if fin == 1:
                break

        return full_message.decode()

    def send_message(self, client, message: str):  #frame a text message and send to the client
        data = message.encode()
        length = len(data)
        frame = bytearray([0b10000001])  # FIN + text opcode

        if length <= 125:
            frame.append(length)
        elif length < 65536:
            frame.append(126)
            frame.extend(length.to_bytes(2, "big"))
        else:
            frame.append(127)
            frame.extend(length.to_bytes(8, "big"))

        frame.extend(data)
        client.send(bytes(frame))

    def send_pong(self, client, payload: bytes):
        frame = bytearray([0b10001010, len(payload)]) + bytearray(payload)
        client.send(bytes(frame))

    def recv_exact(self, client, n):
        buf = bytearray()
        while len(buf) < n:
            chunk = client.recv(n - len(buf))
            if not chunk:
                return None
            buf.extend(chunk)
        return buf













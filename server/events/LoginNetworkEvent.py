from .base import NetworkEvent
from UsersDatabase import get_user, hash_password

class LoginNetworkEvent(NetworkEvent):
    @staticmethod
    def detect(message):
        return message.startswith("login|")

    @staticmethod
    def handle(client, message, clients):
        parts = message.split("|")
        username = parts[1]
        password = parts[2]
        room_id = int(parts[3])

        user = get_user(username)
        if not user:
            client.send("login|error|no_user")
            return

        salt = user[3]
        _, hashed = hash_password(password, salt)

        if hashed != user[2]:
            client.send("login|error|wrong_password")
        elif room_id < 1 or room_id > 10:
            client.send("login|error|room_error")
        else:
            client.send("login|success|" + str(user[0]))
            for websocket, cid, rid in list(clients):
                if websocket == client:
                    clients.remove((websocket, cid, rid))
                    clients.add((websocket, user[0], room_id))


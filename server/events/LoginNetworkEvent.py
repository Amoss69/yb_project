from .base import NetworkEvent
from UsersDatabase import get_user, add_user

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
        elif user[2] != password:
             client.send("login|error|wrong_password")
        elif room_id < 1 or room_id > 10:
             client.send("login|error|room_error")
        else:
             client.send("login|success|" + str(user[0]))  # user[0] = user_id
             for websocket, cid, rid in list(clients): # Update the client tuple
                if websocket == client:
                    clients.remove((websocket, cid, rid))
                    clients.add((websocket, user[0], room_id))


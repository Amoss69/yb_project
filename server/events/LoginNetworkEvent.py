from .base import NetworkEvent
from UsersDatabase import get_user, add_user

class LoginNetworkEvent(NetworkEvent):
    @staticmethod
    def detect(message):
        return message.startswith("login|")

    @staticmethod
    async def handle(client, message, clients):
        parts = message.split("|")
        username = parts[1]
        password = parts[2]
        room_id = int(parts[3])

        user = get_user(username)
        if not user:
            await client.send("login|error|no_user")
        elif user[2] != password:
            await client.send("login|error|wrong_password")
        elif room_id < 1 or room_id > 10:
            await client.send("login|error|room_error")
        else:
            await client.send("login|success|" + str(user[0]))  # user[0] = user_id

            # Update the client tuple
            for websocket, cid, rid in list(clients):
                if websocket == client:
                    clients.remove((websocket, cid, rid))
                    clients.add((websocket, user[0], room_id))


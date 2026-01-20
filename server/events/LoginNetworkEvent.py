from .base import NetworkEvent
from database import get_user, add_user

class LoginNetworkEvent(NetworkEvent):
    @staticmethod
    def detect(message):
        return message.startswith("login|")

    @staticmethod
    async def handle(client, message):
        parts = message.split("|")
        username = parts[1]
        password = parts[2]


        user = get_user(username)
        if not user:
            await client.send("login|error|no_user")
        elif user[2] != password:
            await client.send("login|error|wrong_password")
        else:
            await client.send("login|success")

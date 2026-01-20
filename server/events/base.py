import abc


class NetworkEvent(abc.ABC):
    @staticmethod
    def detect(message: str):
        """Return True if this event should handle the message."""
        pass

    @staticmethod
    async def handle(client, message: str):
        """Handle the message."""
        pass

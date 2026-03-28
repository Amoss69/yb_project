import asyncio

from .base import NetworkEvent
from MarksDataBase import add_marker, remove_marker


class MapMarksEvent(NetworkEvent):

    @staticmethod
    def detect(message):
        return message.split('|')[0] == "marker"

    @staticmethod
    async def handle(client, message: str, clients: set):
        # find this client's room_id
        room_id = None
        for ws, cid, rid in clients:
            if ws == client:
                room_id = rid
                break

        command = message.split('|')[1]

        if command == "place":
            marker, command, marker_type, lat, lng = message.split('|')
            marker_id = add_marker(marker_type, float(lat), float(lng), room_id)
            await MapMarksEvent.broadcast(clients, room_id, f"place_marker|{marker_id}|{marker_type}|{lat}|{lng}")

        elif command == "remove":
            marker_id = message.split('|')[2]
            remove_marker(int(marker_id))
            await MapMarksEvent.broadcast(clients, room_id, f"remove_marker|{marker_id}")

        elif command == "get_markers":
            await MapMarksEvent.sync_markers(client, room_id)

    @staticmethod
    async def broadcast(clients: set, room_id: int, message: str):
        """Send a message to all clients in the same room."""
        room_clients = [ws for ws, cid, rid in clients if rid == room_id]
        if room_clients:
            await asyncio.gather(*[ws.send(message) for ws in room_clients])

    @staticmethod
    async def sync_markers(websocket, room_id: int):
        """Send all existing markers in the room to a newly connected client."""
        from MarksDataBase import get_markers
        for marker in get_markers(room_id):
            marker_id, marker_type, lat, lng = marker
            await websocket.send(f"place_marker|{marker_id}|{marker_type}|{lat}|{lng}")
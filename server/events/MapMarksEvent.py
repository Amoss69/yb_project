import asyncio


from .base import NetworkEvent
from MarksDataBase import add_marker, remove_marker


class MapMarksEvent(NetworkEvent):



    @staticmethod
    def detect(message):
        return message.split('|')[0] == "marker"

    @staticmethod
    async def handle(client, message : str, clients : set):
        command = message.split('|')[1]
        if command == "place": # if command place, get info of marker and insert to sql
            marker, command, marker_type, lat, lng = message.split('|')
            marker_id = add_marker(marker_type, float(lat), float(lng))  # get ID from sql db
            await MapMarksEvent.broadcast(clients, f"place_marker|{marker_id}|{marker_type}|{lat}|{lng}")

        elif command == "remove":  # if command remove, get marker id of marker and use it to remove
            marker_id = message.split('|')[2]
            remove_marker(int(marker_id))
            await MapMarksEvent.broadcast(clients, f"remove_marker|{marker_id}")

        elif command == "get_markers":
            await MapMarksEvent.sync_markers(client)




    @staticmethod
    async def broadcast(clients: set, message: str):
        """Send a message to all connected clients."""
        if clients:
            await asyncio.gather(*[client[0].send(message) for client in clients]) #client[0] = websocket

    @staticmethod
    async def sync_markers(websocket):
        """Send all existing markers to a newly connected client."""
        from MarksDataBase import get_markers
        for marker in get_markers():
            marker_id, marker_type, lat, lng = marker
            await websocket.send(f"place_marker|{marker_id}|{marker_type}|{lat}|{lng}")
import asyncio
import websockets
from UsersDatabase import create_users_tables
from MarksDataBase import create_marks_tables, reset_markers

# Import all event classes from the events package
from events.LoginNetworkEvent import LoginNetworkEvent
from events.MapMarksEvent import MapMarksEvent


connected_clients = set() #Will be set of tuples - (websocket, client_id)

# List of all event handlers
network_events = [
    LoginNetworkEvent,
    MapMarksEvent,
]


async def handle_message(client, message: str):
    print(f"Received from client: {message}")

    # Find which event should handle this message
    for event in network_events:
        if event.detect(message):
            await event.handle(client, message, connected_clients)
            return

    # If no event matched
    await client.send("Unknown command")


async def handle_client(websocket):
    connected_clients.add((websocket,None))  # currently clients have no id, add later in login
    print("Client connected")

    try:
        async for message in websocket:
            await handle_message(websocket, message)

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

    finally:
        for ws, cid in list(connected_clients):
            if ws == websocket:
                connected_clients.remove((ws, cid))


async def main():
    create_users_tables()
    reset_markers()
    create_marks_tables()
    server = await websockets.serve(handle_client, "0.0.0.0", 3000)
    print("Server running on ws://0.0.0.0:3000")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())

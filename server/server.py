import asyncio
import websockets
from database import create_tables

# Import all event classes from the events package
from events import LoginNetworkEvent

connected_clients = set()

# List of all event handlers
network_events = [
    LoginNetworkEvent,
]


async def handle_message(client, message: str):
    print(f"Received from client: {message}")

    # Find which event should handle this message
    for event in network_events:
        if event.detect(message):
            await event.handle(client, message)
            return

    # If no event matched
    await client.send("Unknown command")


async def handle_client(websocket):
    connected_clients.add(websocket)
    print("Client connected")

    try:
        async for message in websocket:
            await handle_message(websocket, message)

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

    finally:
        connected_clients.remove(websocket)


async def main():
    create_tables()
    server = await websockets.serve(handle_client, "0.0.0.0", 3000)
    print("Server running on ws://0.0.0.0:3000")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())

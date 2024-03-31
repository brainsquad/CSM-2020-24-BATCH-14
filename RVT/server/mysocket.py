import asyncio
import websockets
import json

connected = set()


async def chat(websocket, path):
    connected.add(websocket)
    try:
        print("Listening for messages")
        async for message in websocket:
            if message == "start_searching" or message == "start_searching_with_number":
                print("Received start message")
                for conn in connected:
                    if conn != websocket:
                        await conn.send(message)
            
            else:
                for conn in connected:
                    if conn != websocket:
                        await conn.send(json.dumps({"action": "update", "message": message}))

            
    finally:
        connected.remove(websocket)


async def main():
    async with websockets.serve(chat, "localhost", 5001):
        print("Server started on ws://localhost:5001")
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())

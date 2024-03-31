import asyncio
import websockets
from vehicle_tracking.feature_extraction import compare_images_from_path
from vehicle_tracking.vehicle_detection import get_similarity_of_frame
import os
from PIL import Image

connected = set()

async def chat(websocket, path):
    connected.add(websocket)
    try:
        print("Listening for messages")
        async for message in websocket:

            if message == "start":
                print("Received start message")
                # similarity = compare_images_from_path(os.path.join(os.path.dirname(__file__) , 'query_images\query.png'), os.path.join(os.path.dirname(__file__) ,'query_images\query.png'))
                # await websocket.send(f"Similarity: {similarity}")
                frame = Image.open(os.path.join(os.path.dirname(__file__) ,'images\\frame.png')).convert('RGB')
                similarities = get_similarity_of_frame(frame)

                await websocket.send(f"Similarities: {similarities}")

            else:
                print("Received message", message)



            for conn in connected:
                if conn != websocket:
                    await conn.send(message)
    finally:
        connected.remove(websocket)

async def main():
    async with websockets.serve(chat, "localhost", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
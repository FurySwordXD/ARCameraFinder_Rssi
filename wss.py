import asyncio
import websockets

async def handler(websocket):
    while True:
        message = await websocket.recv()
        rssi = int(message)
        print(message)


async def main():
    async with websockets.serve(handler, "0.0.0.0", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
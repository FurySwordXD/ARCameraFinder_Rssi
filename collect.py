from arena import *
import json
import atexit
import random

import asyncio
import websockets

from threading import Thread

scene = Scene(host='mqtt.arenaxr.org', scene='Test')

path_trace = []
id_seq = 0
user_name = 'Fury'

class DataCollector:

    def __init__(self, name):
        self.position = { 'x': 0, 'y': 0, 'z': 0 }
        self.rssi = 0
        self.id = 0
        self.user_name = name

        self.path_trace = []        

        t1 = Thread(target=scene.run_tasks)
        t1.start()

        t2 = Thread(target=self.start_wss)
        t2.start()


    def start_wss(self):
        asyncio.run(self.serve_wss())
    
    async def serve_wss(self):
        async with websockets.serve(self.handler, "", 8001):
            await asyncio.Future()  # run forever

    async def handler(self, websocket):
        while True:
            message = await websocket.recv()
            print(message)


    def push_data_point(self):
        self.id += 1
        self.path_trace.append({ 'position': self.position, 'rssi': self.rssi, 'id': self.id })

    @scene.run_forever(interval_ms=200)
    def update_position(self):
        user = None

        for k, v in scene.users.items():
            if v.displayName == self.user_name:
                user = v

        # user = scene.users[list(scene.users.keys())[0]]
        if user:
            self.position = { 'x': float(user.data.position.x), 'y': float(user.data.position.y), 'z': float(user.data.position.z) }

    def update_rssi(self, rssi):




# def periodic(): 
#     global path_trace
#     global id_seq

#     if len(scene.users.keys()) == 0:
#         print('')
#         return
    

#     user = None
#     for k, v in scene.users.items():
#         if v.displayName == user_name:
#             user = v
#     # user = scene.users[list(scene.users.keys())[0]]
#     if user:
#         position = { 'x': float(user.data.position.x), 'y': float(user.data.position.y), 'z': float(user.data.position.z) }
#         rssi = int(random.random() * 100)
#         id_seq += 1
#         path_trace.append({ 'position': position, 'rssi': rssi, 'id': id_seq })
#         print(user.displayName, position, rssi);



d = DataCollector(name='Fury')

def on_end():
    global d

    with open('data.json', 'w') as f:
        f.write(json.dumps(d.path_trace))

atexit.register(on_end)
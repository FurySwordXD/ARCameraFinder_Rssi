from random import randint
from arena import *
import json

scene = Scene(host='mqtt.arenaxr.org', scene='Test')

data = []
with open('data.json', 'r') as f:
    data = json.loads(f.read())

def find_max_rssi_location(data):    
    # data is of structure:
    # [
    # {
    #     "position": {
    #         "x": -0.034,
    #         "y": 0.388,
    #         "z": 0.06
    #     },
    #     "rssi": -15,
    #     "timestamp": ...
    # },
    # {
    #     "position": {
    #         "x": -0.04,
    #         "y": 0.399,
    #         "z": 0.063
    #     },
    #     "rssi": -85,
    #     "timestamp": ...
    # }, ... ]
    # Find the max rssi in the array of data points and return its corresponding position    
    max_rssi = -1000
    position_at_max = { 'x': 0, 'y': 0, 'z': 0}
    timestamp_at_max = 0
    
    # YOUR CODE HERE
    for data_point in data:
        if data_point['rssi'] > max_rssi:
            max_rssi = data_point['rssi']
            position_at_max = data_point['position']
            timestamp_at_max = data_point['timestamp']

    return max_rssi, position_at_max, timestamp_at_max


@scene.run_once
def start():
    global data    

    objects_to_update = []    
    for i in range(len(data)-2):
        coord1 = Position(data[i]['position']['x'], data[i]['position']['y'], data[i]['position']['z'])
        coord2 = Position(data[i+1]['position']['x'], data[i+1]['position']['y'], data[i+1]['position']['z'])
        rssi = data[i]['rssi']        
        
        line = ThickLine(
            object_id=f'line_{i}',
            color=Color(255,0,0),
            path=(coord1, coord2),
            lineWidth=5,            
            ttl=60 # live for 1 minute
        )
        objects_to_update.append(line)
        

    max_rssi, max_position, max_timestamp = find_max_rssi_location(data)
    print(f"RSSI max of {max_rssi} was at ({max_position['x']}, {max_position['y']}, {max_position['z']})")    
        
    camera_position = (max_position['x'], max_position['y'] - 0.1, max_position['z'])
    end_position = tuple(map(lambda i, j: i + j, camera_position, (0,0.2,0)))    
    camera_marker = Object(
        object_id='cam_object',        
        object_type='gltf-model',
        position=camera_position,
        scale=Scale(10, 10, 10),
        url='store/models/BoomBox.glb',        
        persist=True
    )
    camera_marker.dispatch_animation([
        Animation(property="rotation",start=(0,0,0),end=(0,360,0),dur=5000, easing='linear', dir='forward', loop=True),
        Animation(property="position",start=camera_position,end=end_position,dur=2500, dir='alternate', loop=True)
    ])
    objects_to_update.append(camera_marker)

    
    scene.update_objects(objects_to_update)        



scene.run_tasks()
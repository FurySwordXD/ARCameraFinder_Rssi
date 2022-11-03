import math
from arena import *

scene = Scene(host='mqtt.arenaxr.org', scene='Test')

data = []
with open('data.json', 'r') as f:
    data = json.loads(f.read())

def find_max_rssi_location():
    global data 
    # data is of structure:
    # [
    # {
    #     "position": {
    #         "x": -0.034,
    #         "y": 0.388,
    #         "z": 0.06
    #     },
    #     "rssi": -15,
    #     "id": 1
    # },
    # {
    #     "position": {
    #         "x": -0.04,
    #         "y": 0.399,
    #         "z": 0.063
    #     },
    #     "rssi": -85,
    #     "id": 2
    # }, ... ]
    # Find the max rssi in the array of data points and return its corresponding position
    max_position = Position(0,0,0)
    max_rssi = -1000
    
    for data_point in data:
        if data_point['rssi'] > max_rssi:
            max_rssi = data_point['rssi']
            max_position = data_point['position']

    return max_rssi, max_position


@scene.run_once
def main():
    max_rssi, max_position = find_max_rssi_location()

    print('max ' + str(max_rssi))
    print(Position(max_position['x'], max_position['y'], max_position['z']))
    # camera_marker = Box(
    #     object_id="cam_box",
    #     position=Position(max_position['x'], max_position['y'], max_position['z']),
    #     scale=Scale(.1, .1, .1),
    #     ttl=
    #     # persist=True
    # )            
    # scene.add_object(camera_marker)

    # globe = Object(
    #     object_id='earth_model',
    #     persist=True,
    #     object_type='gltf-model',
    #     position=Position(0, 0.1, 0),
    #     scale=Scale(1,1,1),
    #     url='/store/models/Earth.glb',
    # )
    # scene.add_object(globe)

def convert_range(OldMax, OldMin, NewMax, NewMin, OldValue):
    OldRange = (OldMax - OldMin)  
    NewRange = (NewMax - NewMin)  
    NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin

    return max(NewMin, min(NewValue, NewMax))

ping_pong = True

@scene.run_forever(interval_ms=5000)
def periodic():
    global data
    global ping_pong

    for i in range(0, 6, 2):
        coord1 = Position(data[i]['position']['x'], data[i]['position']['y'], data[i]['position']['z'])
        coord2 = Position(data[i+1]['position']['x'], data[i+1]['position']['y'], data[i+1]['position']['z'])        
        rssi = data[i]['rssi']
        weight = convert_range(-20, -70, 1, 0, rssi)
        print(rssi, weight)
        if i < 4:
            color="#ff0000"            
        else:
            color="#ffffff"
        # color = Color(int(255 * weight), 0, int(255 * (1 - weight))) # R, G, B

        print(color)
        line = ThickLine(
            object_id=f'line_{i}',
            color=Color(255,255,255) if i == 2 else Color(255,0,0),
            path=(coord1, coord2),
            lineWidth=5,
            ttl=5 # live for 5 seconds
        )
        scene.add_object(line)

    max_rssi, max_position = find_max_rssi_location()
    print(max_rssi)
    if (len(list(scene.users.keys())) > 0):
        user = scene.users[list(scene.users.keys())[0]]
        
    camera_position = (max_position['x'], max_position['y'] - 0.1, max_position['z'])
    end_position = tuple(map(lambda i, j: i + j, camera_position, (0,0.2,0)))
    # ping_pong = not ping_pong
    camera_marker = Object(
        object_id='cam_object',
        persist=True,
        object_type='gltf-model',
        position=camera_position,
        scale=Scale(10, 10, 10),
        url='store/models/BoomBox.glb',
        ttl=5
    )
    camera_marker.dispatch_animation([
        Animation(property="rotation",start=(0,0,0),end=(0,360,0),dur=5000, easing='linear', dir='forward', loop=True),
        Animation(property="position",start=camera_position,end=end_position,dur=2500, dir='alternate', loop=True)
    ])
    scene.add_object(camera_marker)    
    # print('Line Trace added')


scene.run_tasks()
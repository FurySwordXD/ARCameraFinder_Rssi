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
    #     "rssi": 15,
    #     "id": 1
    # },
    # {
    #     "position": {
    #         "x": -0.04,
    #         "y": 0.399,
    #         "z": 0.063
    #     },
    #     "rssi": 85,
    #     "id": 2
    # }, ... ]
    # Find the max rssi in the array of data points and return its corresponding position
    max_position = Position(0,0,0)
    max_rssi = 0
    
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
    camera_marker = Box(
        object_id="cam_box",
        position=Position(max_position['x'], max_position['y'], max_position['z']),
        scale=Scale(.1, .1, .1),
        persist=True        
    )            
    scene.add_object(camera_marker)

    globe = Object(
        object_id='earth_model',
        persist=True,
        object_type='gltf-model',
        position=Position(0, 0.1, 0),
        scale=Scale(1,1,1),
        url='/store/models/Earth.glb',
    )
    scene.add_object(globe)


@scene.run_forever(interval_ms=3000)
def periodic():
    global data

    for i in range(len(data)-1):
        coord1 = Position(data[i]['position']['x'], data[i]['position']['y'], data[i]['position']['z'])
        coord2 = Position(data[i+1]['position']['x'], data[i+1]['position']['y'], data[i+1]['position']['z'])        

        line = ThickLine(
            color="#ff0000",            
            path=(coord1, coord2),
            lineWidth=10,
            ttl=3 # live for 30 seconds
        )
        scene.add_object(line)

    print('Line Trace added')


scene.run_tasks()
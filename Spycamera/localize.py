from arena import *
import json

scene = Scene(host='arenaxr.org', scene='spy_camera_finder')

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
    # to get the rssi value at an index use data[index]['rssi']
    position = { 'x': 0, 'y': 0, 'z': 0}
    timestamp = 0
    
    # YOUR CODE HERE

    return max_rssi, position, timestamp

@scene.run_once
def start():
    ar_marker = Object(
        object_id='ar-marker', position=(0,0,0), rotation=(-90,0,0), scale=(.15,.15,.15),
        object_type='gltf-model', url='/store/public/armarker.glb',
        armarker={'markerid': '0', 'markertype': 'apriltag_36h11', 'size': 150, 'dynamic': False, 'buildable': False},
        persist=True
    )
    camera = Object(
        object_id='real-camera',        
        object_type='gltf-model',
        position=(11.0, 0, -6),
        scale=Scale(.2, .2, .2),
        url='store/models/AntiqueCamera.glb',
        persist=True
    )
    scene.add_object(camera)
    scene.add_object(ar_marker)
    
def rescale_value(old_min, old_max, new_min, new_max, value):
    return ((value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min

@scene.run_forever(interval_ms=5000)
def update():
    global data    

    max_rssi, position, timestamp = find_max_rssi_location(data)
    print(f"RSSI max of {max_rssi} was at ({position['x']}, {position['y']}, {position['z']})")    
        
    camera_position = (position['x'], position['y'], position['z'])
    end_position = tuple(map(lambda i, j: i + j, camera_position, (0,0.2,0)))    
    camera_marker = Object(
        object_id='cam_object',        
        object_type='gltf-model',
        position=camera_position,
        scale=Scale(15, 15, 15),
        url='store/models/BoomBox.glb',
        persist=True
    )
    camera_marker.dispatch_animation([
        Animation(property="rotation",start=(0,0,0),end=(0,360,0),dur=5000, easing='linear', dir='forward', loop=True),
        Animation(property="position",start=camera_position,end=end_position,dur=2500, dir='alternate', loop=True)
    ])
    scene.update_object(camera_marker)
    # objects_to_update.append(camera_marker)
    
    # draws multiple line segements to visualize the path we took to collect data  
    for i in range(len(data)-2):
        coord1 = Position(data[i]['position']['x'], data[i]['position']['y'], data[i]['position']['z'])
        coord2 = Position(data[i+1]['position']['x'], data[i+1]['position']['y'], data[i+1]['position']['z'])
        rssi = data[i]['rssi']
        
        line = ThickLine(
            object_id=f'line_{i}',
            color=Color(128,128,128),
            path=(coord1, coord2),
            lineWidth=5,            
            ttl=30 # live for 1 minute
        )
        scene.update_object(line)

        factor = rescale_value(
            min(map(lambda x: x['rssi'], data)),
            max(map(lambda x: x['rssi'], data)), 
            0, 1, rssi
        )
        color = int(255*(1-factor)) # color the sphere based on rssi intensity; RED - High RSSI, WHITE - LOW RSSI
        scale = .2*factor # scale the sphere based on rssi intensity; Big - High RSSI, Small - LOW RSSI
        sphere = Sphere(
            object_id=f'sphere_{i}', 
            position=coord1,
            color=Color(255,color,color),
            scale=Scale(scale,scale,scale),
            ttl=30
        )
        scene.update_object(sphere)        


scene.run_tasks()
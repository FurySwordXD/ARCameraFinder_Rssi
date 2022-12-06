import json, time, atexit
from arena import *
from arena_localizer import ArenaLocalizer
# from rssi_scanner import RSSIScanner

name = "Sainath Ganesh" # Enter the name you used as display name in arena
DEV_MAC = "dc:a6:32:33:ae:15" #camera's mac address
CHANNEL_NUM = 5 #Channel to listen on
IFACE = "wlan1" #Interface for sniffer

# rssi_scanner = RSSIScanner(mac_address=DEV_MAC, channel=CHANNEL_NUM, iface=IFACE)

scene = Scene(host='arenaxr.org', scene='spy_camera_finder')
path_trace = []

arena_localizer = ArenaLocalizer(name=name)

data = []

@scene.run_once
def start():    
    ar_marker = Object(
        object_id='ar-marker', position=(0,0,0), rotation=(-90,0,0), scale=(.15,.15,.15),
        object_type='gltf-model', url='/store/public/armarker.glb',
        armarker={'markerid': '0', 'markertype': 'apriltag_36h11', 'size': 150, 'dynamic': False, 'buildable': False},
        persist=True
    )
    scene.add_object(ar_marker)
    
@scene.run_forever(interval_ms=1000)
def update():
    global data

    # rssi = rssi_scanner.get_rssi()
    rssi = -20
    position = arena_localizer.update_position(scene)
    timestamp = int(time.time())

    # if rssi != None and position != None:
    if position != None:
        data_point = {}
        data_point['position'] = position
        data_point['rssi'] = rssi
        data_point['timestamp'] = timestamp
        data.append(data_point)


def on_end():
    global data
    with open('data.json', 'w') as f:
        f.write(json.dumps(data))

atexit.register(on_end)
scene.run_tasks()
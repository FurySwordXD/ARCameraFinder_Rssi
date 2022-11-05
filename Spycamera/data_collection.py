import json, time, atexit
from arena import *
from arena_localizer import ArenaLocalizer
from rssi_scanner import RSSIScanner

name = "<Display Name>" # Enter the name you used as display name in arena
DEV_MAC = "dc:a6:32:33:ae:15" #camera's mac address
CHANNEL_NUM = 5 #Channel to listen on
IFACE = "wlan1" #Interface for sniffer

rssi_scanner = RSSIScanner(mac_address=DEV_MAC, channel=CHANNEL_NUM, iface=IFACE)

scene = Scene(host='arenaxr.org', scene='spy_camera_finder')
path_trace = []

arena_localizer = ArenaLocalizer(name=name)

data = []

@scene.run_forever(interval_ms=200)
def update():
    global data

    rssi = rssi_scanner.get_rssi()
    position = arena_localizer.update_position(scene)
    timestamp = int(time.time())

    if rssi != None and position != None:
        # data_point = {}
        # data_point['position'] = position
        data_point = position
        data_point['rssi'] = rssi
        data_point['timestamp'] = timestamp
        data.append(data_point)


def on_end():
    global data
    with open('data.json', 'w') as f:
        f.write(json.dumps(data))

atexit.register(on_end)
scene.run_tasks()
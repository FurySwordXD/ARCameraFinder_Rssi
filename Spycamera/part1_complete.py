from random import randint
from arena import *

# Connect to ARENA server
scene = Scene(host="arenaxr.org", scene="lab_part_1")

box = None

@scene.run_once # runs once at startup
def main():
    ar_marker = Object(
        object_id='ar-marker', position=(0,0,0), rotation=(0,0,0), scale=(.15,.15,.15),
        object_type='gltf-model', url='/store/public/armarker.glb',
        armarker={'markerid': '0', 'markertype': 'apriltag_36h11', 'size': 150, 'dynamic': False, 'buildable': False},
        persist=True
    )
    scene.add_object(ar_marker)

    
    global scene, box #we want to reference the box we create and add an animation to it later

    # create a box
    box = Box(
        object_id="myBox",     
        position=(0,0,0), scale=(1,1,1), 
        color=(255,0,0), 
        persist=True
    )    
    # Add the box to ARENA
    scene.add_object(box)
    

@scene.run_forever(interval_ms=5000) # runs every 5 seconds
def interval():
    global scene, box
    
    y = randint(2, 5)
    box.dispatch_animation([
        Animation(property="position",start=(0,0,0),end=(0,y+3,0),dur=2500, dir='alternate', loop=True),
        Animation(property="rotation",start=(0,0,0),end=(0,360*y,0),dur=5000, easing='linear', dir='forward', loop=True),
    ])
    scene.update_object(box)

# start tasks
scene.run_tasks()
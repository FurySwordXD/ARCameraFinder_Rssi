from random import randint
from arena import *

# Connect to ARENA server
scene = Scene(host="arenaxr.org", scene="lab_part_1")

box = None

@scene.run_once # runs once at startup
def main():
    global scene, box #we want to reference the box we create and add an animation to it later

    # create a box
    box = Object(object_id="myBox", object_type='gltf-model', url='store/models/BoomBox.glb', position=(0,0,0), rotation=(0,0,-90), scale=(10,10,10), color=(255,0,0), persist=True)    
    # Add the box to ARENA
    scene.add_object(box)    

@scene.run_forever(interval_ms=5000) # runs every 5 seconds
def interval():
    global scene, box
    
    # y = randint(0, 5)
    box.dispatch_animation([
        Animation(property="position",start=(0,0,0),end=(0,2,0),dur=2500, dir='alternate', loop=True),
        Animation(property="rotation",start=(0,0,-90),end=(360,0,-90),dur=5000, easing='linear', dir='forward', loop=True),
    ])
    scene.update_object(box)

# start tasks
scene.run_tasks()
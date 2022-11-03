from random import randint
from arena import *

# Connect to ARENA server
scene = Scene(host="mqtt.arenaxr.org", scene="lab_part_1")

box = None

@scene.run_once # runs once at startup
def main():
    global scene, box #we want to reference the box we create and add an animation to it later

    # create a box
    box = Box(object_id="myBox", position=(0,0,0), scale=(1,1,1), ttl=30)
    box.dispatch_animation([        
        Animation(property="position",start=(0,0,0),end=(0,5,0),dur=2500, dir='alternate', loop=True)
    ])
    # Add the box to ARENA
    scene.add_object(box)    

@scene.run_forever(interval_ms=5000) # runs every 5 seconds
def interval():
    global scene, box
    
    y = randint(0, 5)
    box.dispatch_animation([
        Animation(property="rotation",start=(0,0,0),end=(0,360,0),dur=5000, delay=2000, easing='linear', dir='forward', loop=True),
        Animation(property="position",start=(0,y,0),end=(0,5,0),dur=2500, dir='alternate', loop=True)
    ])
    scene.update_object(box)

# start tasks
scene.run_tasks()
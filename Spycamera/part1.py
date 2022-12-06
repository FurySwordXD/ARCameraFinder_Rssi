from random import randint
from arena import *

# Connect to ARENA server
scene = Scene(host="arenaxr.org", scene="lab_part_1")

box = None

@scene.run_once # runs once at startup
def main():
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

# start tasks
scene.run_tasks()
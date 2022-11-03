from arena import *

class ArenaLocalizer:

    def __init__(self, name):
        self.position = { 'x': 0, 'y': 0, 'z': 0 }
        self.username = name
    
    def update_position(self, scene): 
        user = None
        for k, v in scene.users.items():            
            if self.username == v.displayName:
                user = v                
                break

        if user != None:
            self.position = { 'x': float(user.data.position.x), 'y': float(user.data.position.y), 'z': float(user.data.position.z) }
            print(f'{user.displayName} - {str(self.position)}')
            return self.position

        return None

if __name__ == "__main__":
    scene = Scene(host='mqtt.arenaxr.org', scene='Test')
    arena_localizer = ArenaLocalizer(name="Sainath Ganesh")

    @scene.run_forever(interval_ms=200) # runs ever 0.2 seconds
    def on_scene_update():
        global arena_localizer
        arena_localizer.update_position(scene)
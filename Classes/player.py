from Classes.areas import *

trans = {
    (-1,0): "left",
    (1,0): "right",
    (0,-1): "up",
    (0,1): "down"
}
rights = {
    "left": (-1,0),
    "right": (1,0),
    "up": (0,-1),
    "down": (0,1)
}

class Player:
    def __init__(self):
        self.location = "plains"
        self.pos = plains.default_spawn
        self.facing = "down"
        self.inventory = {
            "pokeballs": [],
            "healing": [],
            "tms": [],
            "key_items": []
        }
    def get_pointing(self):
        return (self.pos[0] + rights[self.facing][0], self.pos[1] + rights[self.facing][1])

player = Player()
current_player_data = Player()
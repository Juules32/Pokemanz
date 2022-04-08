from Classes.areas import *

class Player:
    def __init__(self):
        self.location = "plains"
        self.pos = plains.default_spawn
        self.facing = (0,0)
        self.inventory = {
            "pokeballs": [],
            "healing": [],
            "tms": [],
            "key_items": []
        }
        self.run_queue = []
    def get_pointing(self):
        return (self.pos[0] + self.facing[0], self.pos[1] + self.facing[1])

    def run_1_tile(self, dir):
        x = 0
        while x < TILE_SIZE:
            self.run_queue.append(dir)
            x += 1
        self.pos[0] += dir[0]
        self.pos[1] += dir[1]


player = Player()
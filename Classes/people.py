import pygame
from constants import *

class Person:
    def __init__(self, location, pos, facing):
        self.location = location
        self.pos = pos
        self.facing = facing

class Player(Person):
    def __init__(self, location, pos, facing):
        super().__init__(location, pos, facing)
        self.inventory = {
            "pokeballs": [],
            "healing": [],
            "tms": [],
            "key_items": []
        }
        self.run_queue = []
        self.latest_dir = None
        self.current_dirs = []
        self.sprites = {
            "[-1, 0]_0": pygame.image.load("Assets/left_0.png"),
            "[-1, 0]_1": pygame.image.load("Assets/left_1.png"),
            "[-1, 0]_2": pygame.image.load("Assets/left_2.png"),
            "[1, 0]_0": pygame.image.load("Assets/right_0.png"),
            "[1, 0]_1": pygame.image.load("Assets/right_1.png"),
            "[1, 0]_2": pygame.image.load("Assets/right_2.png"),
            "[0, -1]_0": pygame.image.load("Assets/up_0.png"),
            "[0, -1]_1": pygame.image.load("Assets/up_1.png"),
            "[0, -1]_2": pygame.image.load("Assets/up_2.png"),
            "[0, 1]_0": pygame.image.load("Assets/down_0.png"),
            "[0, 1]_1": pygame.image.load("Assets/down_1.png"),
            "[0, 1]_2": pygame.image.load("Assets/down_2.png")
        }

        #animation variables
        self.count = 0
        self.stance = 0
        self.wants_to_interact = False
        self.interacting = False
    
    def get_pointing(self):
        return (self.pos[0] + self.facing[0], self.pos[1] + self.facing[1])

    def run_1_tile(self, dir):
        for i in range(0,16):
            self.run_queue.append(dir)

        self.pos[0] += dir[0]
        self.pos[1] += dir[1]

class Npc(Person):
    def __init__(self, location, pos, facing, id, text):
        super().__init__(location, pos, facing)
        self.id = id
        self.text = text
        self.sprite = pygame.image.load("Assets/" + self.id.split("_")[0] + ".png")
    
    def interact(self):
        for line in self.text:
            print(line)

class Trainer(Npc):
    def __init__(self, location, pos, facing, id):
        super().__init__(location, pos, facing, id)


class ImportantNpc(Npc):
    pass

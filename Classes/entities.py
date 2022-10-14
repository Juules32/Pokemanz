import pygame
from constants import *

class Entity:
    def __init__(self, id, location, pos):
        self.id = id
        self.location = location
        self.pos = pos
        self.sprite = pygame.image.load("Assets/" + self.id.split("_")[0] + ".png")

class Player(Entity):
    def __init__(self, id, location, pos):
        super().__init__(id, location, pos)
        self.inventory = {
            "pokeballs": [],
            "healing": [],
            "tms": [],
            "key_items": []
        }
        self.facing = (0,0)
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


class Interactable(Entity):
    def __init__(self, id, location, pos, text):
        super().__init__(id, location, pos)
        self.text = text
    
    def interact(self):
        print(self.text)  

class Npc(Interactable):
    def __init__(self, id, location, pos, facing, text):
        super().__init__(id, location, pos, text)
        self.facing = facing

class Trainer(Npc):
    def __init__(self, id, location, pos, facing, text):
        super().__init__(id, location, pos, facing, text)

    def detect_vision(self):
        pass

class ImportantNpc(Npc):
    pass

class Item(Interactable):
    def __init__(self, id, location, pos, text, visible = True):
        super().__init__(id, location, pos, text)
        if not visible:
            self.sprite

    def pickup(self):
        pass



items = {
    "pokeballs": ["pokeball", "great ball", "ultra ball"]
}

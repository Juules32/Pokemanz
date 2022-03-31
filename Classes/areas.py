
import pygame, json
from Classes.npc import *

class Map:

    def __init__(self, name, previous_location = None):
        self.name = name
        try:
            self.collision_map = self.get_collision_map()
        except:
            self.collision_map = [[]]
        self.w = len(self.collision_map[0])
        self.h = len(self.collision_map)

        self.default_spawn = self.get_default_spawn()
        self.previous_location = previous_location
        self.background_sprite = pygame.image.load(f"Areas/{name}/background.png")
        self.foreground_sprite = pygame.image.load(f"Areas/{name}/foreground.png")
        self.npc_map = self.get_npc_map()
        self.npcs = self.get_npcs()

    def get_collision_map (self):
        file = open(f"Areas/{self.name}/collision.txt", "r")
        data = file.read().split("\n")
        file.close()
        collision_map = []
        for row in data:
            collision_map.append([int(x) for x in list(row)])
        return collision_map
    
    def get_default_spawn(self):
        y = 0
        for row in self.collision_map:
            try:
                if row.index(3):
                    return [row.index(3), y]
            except:
                y += 1

    def get_npc_map(self):
        with open(f"Areas/{self.name}/npcs.txt", "r") as file:
            data = json.load(file)
        return data
    
    def get_npcs(self):
        data = self.get_npc_map()
        found_npcs = []
        x = 0
        for row in data:
            y = 0
            for tile in row:
                if tile != None:
                    found_npcs.append([tile, x, y])
                y += 1
            x += 1
        return found_npcs
    
    
plains = Map("plains")


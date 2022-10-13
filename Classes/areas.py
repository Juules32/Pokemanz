import pygame, json, copy
from all_npcs import all_npcs

class Map:

    def __init__(self, name, previous_location = None):
        self.name = name
        

        self.previous_location = previous_location
        self.background_sprite = pygame.image.load(f"Areas/{name}/background.png")
        self.foreground_sprite = pygame.image.load(f"Areas/{name}/foreground.png")
        self.npcs = self.get_npcs()
        self.items = self.get_items()
        try:
            self.collision_map = self.get_collision_map()
        except:
            self.collision_map = [[]]
        self.w = len(self.collision_map[0])
        self.h = len(self.collision_map)
        self.default_spawn = self.get_default_spawn()


    
    def get_collision_map (self):
        file = open(f"Areas/{self.name}/collision.txt", "r")
        data = file.read().split("\n")
        file.close()
        collision_map = []
        for row in data:
            collision_map.append([int(x) for x in list(row)])
        for npc in self.npcs:
            collision_map[npc.pos[1]][npc.pos[0]] = npc
        return collision_map
    
    def get_default_spawn(self):
        y = 0
        for row in self.collision_map:
            try:
                if row.index(3):
                    return [row.index(3), y]
            except:
                y += 1

    
    
    def get_npcs(self):
        area_npcs = []
        for npc in list(all_npcs):
            if(npc.location == self.name):
                area_npcs.append(npc)
        return area_npcs

    def get_items(self):
        return json.load(open(f"Areas/{self.name}/items.txt", "r"))

    
    


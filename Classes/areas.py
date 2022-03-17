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
        self.x, self.y = self.default_spawn
        self.previous_location = previous_location

    def get_collision_map (self):
        file = open(f"areas/{self.name}/{self.name}.txt", "r")
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
    
plains = Map("plains")
from displays import *

class Npc:
    def __init__(self, id):
        self.id = id
        self.text = self.get_text()
        self.sprite = pygame.image.load(f"Assets/{self.id}.png")

    def get_text(self):
        file = open(f"Dialogue/{self.id}.txt", "r")
        data = file.read().split("\n")
        file.close()
        return data
    
    def interact(self):
        for line in self.text:
            print("pee")

npcs = {
    "sailor1": Npc("sailor1")
}

from Classes.areas import *

class Player:
    def __init__(self):
        self.location = "plains"
        self.pos = plains.default_spawn
        self.inventory = {
            "pokeballs": [],
            "healing": [],
            "tms": [],
            "key_items": []
        }

player = Player()
current_player_data = Player()
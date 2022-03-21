from ast import Str
from tokenize import String

class Save:
    def __init__(self):
        self.location = "plains"
        self.x = 3
        self.y = 10
        self.inventory = {
            "pokeballs": [],
            "healing": [],
            "tms": [],
            "key_items": []
        }
        


# if save_X.location = None then display unused save file
save_data = Save()
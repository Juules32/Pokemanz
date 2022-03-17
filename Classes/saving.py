from ast import Str
from tokenize import String

class Save:
    def __init__(self):
        self.x = 10
        self.y = 20
        self.location = ""


# if save_X.location = None then display unused save file
save_data = [
    Save(),
    Save(),
    Save(),
    Save(),
    Save(),
]
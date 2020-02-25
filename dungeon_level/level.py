import numpy as np

class Level:

    def __init__(self):
        self.time_limit = 0
        self.required_collectable_count = 0
        self.upper_layer = np.array([])
        self.lower_layer = np.array([])
        self.map_title = ""

    
    def convert_to_native_tiles(self, layer):
        pass


    @staticmethod
    def find_tiles(layer, tile):
        positions = np.argwhere(layer == tile)
        return positions
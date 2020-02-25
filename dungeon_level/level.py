import numpy as np

from dungeon_level.dungeon_tiles import Tiles

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
    

    def __repr__(self):
        string = "Title: {}\nTime Limit: {}\nRequired Collectables: {}\n".format(self.map_title, self.time_limit, self.required_collectable_count)
        h, w = self.upper_layer.shape
        for y in range(h):
            for x in range(w):
                tile = self.upper_layer[y,x]
                if tile == Tiles.empty:
                    string += "."
                if tile == Tiles.wall:
                    string += "w"
                if tile == Tiles.player:
                    string += "s"
                if tile == Tiles.finish:
                    string += "f"
                if tile == Tiles.key_red:
                    string += "k"
                if tile == Tiles.lock_red:
                    string += "l"
                if tile == Tiles.collectable:
                    string += "c"
            string += "\n"
        return string
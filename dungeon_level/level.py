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

    @staticmethod
    def is_position_within_layer_bounds(layer, position):
        h, w = layer.shape
        is_within_bounds = position[0] >= 0 and position[1] >= 0 and position[0] < h and position[1] < w
        return is_within_bounds
    

    def __repr__(self):
        string = "Title: {}\nTime Limit: {}\nRequired Collectables: {}\n".format(self.map_title, self.time_limit, self.required_collectable_count)
        h, w = self.upper_layer.shape
        for y in range(h):
            for x in range(w):
                tile = self.upper_layer[y,x]
                if tile == Tiles.empty:
                    string += ". "
                if tile == Tiles.wall:
                    string += "# "
                if tile == Tiles.player:
                    string += "s "
                if tile == Tiles.finish:
                    string += "f "
                if tile == Tiles.key_blue:
                    string += "kB"
                if tile == Tiles.lock_blue:
                    string += "lB"
                if tile == Tiles.key_red:
                    string += "kR"
                if tile == Tiles.lock_red:
                    string += "lR"
                if tile == Tiles.key_green:
                    string += "kG"
                if tile == Tiles.lock_green:
                    string += "lG"
                if tile == Tiles.key_yellow:
                    string += "kY"
                if tile == Tiles.lock_yellow:
                    string += "lY"
                if tile == Tiles.collectable:
                    string += "c "
                if tile == Tiles.required_collectable_barrier:
                    string += "@ "
                if tile == Tiles.water:
                    string += "w "
                if tile == Tiles.flippers:
                    string += "fl"
                if tile == Tiles.fire:
                    string += "F "
                if tile == Tiles.fire_boots:
                    string += "Fb"
                if tile == Tiles.sokoban_block:
                    string += "[]"
                if tile == Tiles.sokoban_goal:
                    string += "><"
            string += "\n"
        return string
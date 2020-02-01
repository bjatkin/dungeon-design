from validation.path_finder import PathFinder
from dungeon_level.dungeon_tiles import Tiles
from dungeon_level.level import Level

import numpy as np

class Solver:
    @staticmethod
    def is_solvable(level):
        player_position = Solver.find_tiles(level.upper_layer, Tiles.player)[0]
        required_reachables = [Tiles.finish, Tiles.collectable]
        for required_reachable in required_reachables:
            tiles = Solver.find_tiles(level.upper_layer, required_reachable)
            for tile in tiles:
                if not PathFinder.is_reachable(level.upper_layer, player_position, tile):
                    return False

        return True


    @staticmethod
    def find_tiles(layer, tile):
        positions = np.argwhere(layer == tile)
        return positions

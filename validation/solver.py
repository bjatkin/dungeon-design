from validation.path_finder import PathFinder
from validation.player_status import PlayerStatus
from dungeon_level.dungeon_tiles import Tiles
from dungeon_level.level import Level

import numpy as np

class Solver:
    @staticmethod
    def is_solvable(level):
        player_position = Solver.find_tiles(level.upper_layer, Tiles.player)[0]
        player_status = PlayerStatus()

        # We want the player to be able to reach the flippers so they can swim.
        if not Solver.can_reach_tiles_of_type(level, Tiles.flippers, player_position, player_status, True):
            return False

        # We don't want the player to be able to reach the finish initially, without collecting all collectables
        player_status.can_swim = True
        if Solver.can_reach_tiles_of_type(level, Tiles.finish, player_position, player_status, False):
            return False

        # We want the player to be able to reach all collectables.
        if not Solver.can_reach_tiles_of_type(level, Tiles.collectable, player_position, player_status, True):
            return False

        # Once the player collects all collectables, they should be able to reach the finish.
        player_status.has_all_collectables = True
        if not Solver.can_reach_tiles_of_type(level, Tiles.finish, player_position, player_status, False):
            return False

        return True


    @staticmethod
    def can_reach_tiles_of_type(level, tile_type, player_position, player_status, must_reach_all):
        tiles = Solver.find_tiles(level.upper_layer, tile_type)
        for tile_position in tiles:
            is_reachable = PathFinder.is_reachable(level.upper_layer, player_position, tile_position, player_status)
            if must_reach_all and not is_reachable:
                return False
            elif not must_reach_all and is_reachable:
                return True
        
        if must_reach_all:
            return True
        else:
            return False



    @staticmethod
    def find_tiles(layer, tile):
        positions = np.argwhere(layer == tile)
        return positions

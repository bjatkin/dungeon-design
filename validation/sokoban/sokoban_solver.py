import numpy as np
import copy
from dungeon_level.dungeon_tiles import Tiles, lock_tiles, key_tiles, item_tiles, hazard_tiles
from dungeon_level.level import Level
from validation.player_traverser import PlayerTraverser
from validation.path_finder import PathFinder

class SokobanSolver:
    @staticmethod
    def is_sokoban_solvable(level_layer, player_position, sokoban_key, sokoban_lock, get_solution=False):

        layer = copy.deepcopy(level_layer)
        layer[tuple(sokoban_key)] = Tiles.empty
        sokoban_traverser = SokobanTraverser(player_position)
        def can_traverse(layer, previous_position, current_position, next_position):
            return sokoban_traverser.can_traverse(layer, previous_position, current_position, next_position)

        is_solvable = PathFinder.find_path(layer, sokoban_key, sokoban_lock, can_traverse)
        return is_solvable


class SokobanTraverser:
    def __init__(self, player_start_position):
        self.player_start_position = player_start_position


    def print_status(self, layer, push_from_position, current_block_position, previous_block_position):
        current_player_position = self.get_current_player_position(previous_block_position)
        string = Level.layer_to_string(layer, {"*":push_from_position, "P":current_player_position, "[]":current_block_position})
        print("\n{}".format(string))


    def can_traverse(self, layer, previous_block_position, current_block_position, next_block_position):
        if not Level.is_position_within_layer_bounds(layer, next_block_position):
            return False

        push_direction = next_block_position - current_block_position
        push_from_position = current_block_position - push_direction
        current_player_position = self.get_current_player_position(previous_block_position)

        if not self.is_tile_empty(layer, push_from_position):
            return False
        
        if not self.is_tile_empty(layer, next_block_position):
            return False

        if not self.can_player_reach_push_position(layer, push_from_position, current_block_position, current_player_position):
            return False

        return True

    def get_current_player_position(self, previous_block_position):
        # This may seem like an obvious line of code, but
        # the position that the player currently is in is the location
        # of the previous block since the player had to be there in order
        # to push the block from its previous position to the current position.
        # If there is no previous block position however, we use the start position of the player.
        if previous_block_position is not None:
            return previous_block_position
        else:
            return self.player_start_position


    def is_tile_empty(self, layer, next_block_position):
        if not Level.is_position_within_layer_bounds(layer, next_block_position):
            return False
        return layer[tuple(next_block_position)] in {Tiles.empty, Tiles.sokoban_goal, Tiles.player, Tiles.collectable, Tiles.fire_boots, Tiles.flippers, Tiles.key_blue, Tiles.key_green, Tiles.key_red, Tiles.key_yellow}

        
    def can_player_reach_push_position(self, layer, push_from_position, current_block_position, current_player_position):
        current_block_position_t = tuple(current_block_position)
        previous_tile = layer[current_block_position_t]
        layer[current_block_position_t] = Tiles.sokoban_block
        can_player_reach_push_position = PathFinder.find_path(layer, current_player_position, push_from_position, PlayerTraverser.can_traverse)
        layer[current_block_position_t] = previous_tile
        return can_player_reach_push_position
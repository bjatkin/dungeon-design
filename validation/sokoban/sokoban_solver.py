import numpy as np
import copy
from dungeon_level.dungeon_tiles import Tiles, lock_tiles, key_tiles, item_tiles, hazard_tiles
from dungeon_level.level import Level
from validation.player_traverser import PlayerTraverser
from validation.path_finder import PathFinder

class SokobanSolver:
    @staticmethod
    def is_sokoban_solvable(level_layer, player_position, sokoban_key, sokoban_lock, return_type="moves"):

        layer = copy.deepcopy(level_layer)
        layer[tuple(sokoban_key)] = Tiles.empty
        sokoban_traverser = SokobanTraverser(player_position)
        def can_traverse(layer, previous_position, current_position, next_position):
            return sokoban_traverser.can_traverse(layer, previous_position, current_position, next_position)

        sokoban_path = PathFinder.find_path(layer, sokoban_key, sokoban_lock, can_traverse, return_type="path")

        if return_type == "path_exists":
            return sokoban_path is not None
        else:
            if sokoban_path is not None:
                sokoban_moves = sokoban_traverser.insert_player_moves(sokoban_path)
            else:
                sokoban_moves = None
            return sokoban_moves


class SokobanTraverser:
    def __init__(self, player_start_position):
        self.player_start_position = player_start_position
        self.player_moves = dict()


    def print_status(self, layer, push_from_position, current_block_position, previous_block_position):
        current_player_position = self.get_current_player_position(previous_block_position)
        string = Level.layer_to_string(layer, {"*":push_from_position, "P":current_player_position, "[]":current_block_position})
        print("\n{}".format(string))

    
    def insert_player_moves(self, sokoban_path):
        new_sokoban_moves = []
        sokoban_path.insert(0, None)
        for i in range(2, len(sokoban_path)):
            previous_position = sokoban_path[i - 2]
            if previous_position is not None:
                previous_position = tuple(previous_position)
            current_position = tuple(sokoban_path[i - 1])
            next_position = tuple(sokoban_path[i])
            move_key = (previous_position, current_position, next_position)
            player_move = self.player_moves[move_key]
            new_sokoban_moves.extend(player_move)
        return new_sokoban_moves


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

        player_to_push_position_moves = self.can_player_reach_push_position(layer, push_from_position, current_block_position, current_player_position)
        if player_to_push_position_moves is None:
            return False
        else:
            if previous_block_position is not None:
                previous_block_position = tuple(previous_block_position)
            move_key = (previous_block_position, tuple(current_block_position), tuple(next_block_position))
            player_to_push_position_moves.append(push_direction)
            self.player_moves[move_key] = player_to_push_position_moves

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
        player_to_push_position_moves = PathFinder.find_path(layer, current_player_position, push_from_position, PlayerTraverser.can_traverse, return_type="moves")
        layer[current_block_position_t] = previous_tile
        return player_to_push_position_moves
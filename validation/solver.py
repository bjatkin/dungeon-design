from validation.path_finder import PathFinder
from validation.player_status import PlayerStatus
from dungeon_level.dungeon_tiles import Tiles
from dungeon_level.level import Level
from graph_structure.graph_node import GNode, Start, End, Key, Lock

import numpy as np

class Solver:
    @staticmethod
    def does_level_follow_mission(level, mission_start_node, mission_final_node, positions_map, give_failure_reason=False):
        layer = np.array(level.upper_layer)
        player_position = Level.find_tiles(layer, Tiles.player)
        if player_position.shape[0] == 0:
            return False
        else:
            player_position = player_position[0]

        unreached = set(GNode.find_all_nodes(mission_start_node))
        reached_node_too_soon = False
        reached_final_node = False
        player_status = PlayerStatus(level.required_collectable_count)

        def visit_method(node, visited_nodes):
            nonlocal unreached
            nonlocal player_status
            nonlocal player_position
            nonlocal reached_node_too_soon
            nonlocal reached_final_node

            player_position = positions_map[node]
            Solver.update_player_and_layer_status(layer, player_status, node, positions_map)

            unreached = unreached - visited_nodes - set(node.child_s)
            for unreached_node in unreached:
                if can_reach_node(node, unreached_node):
                    reached_node_too_soon = True
            
            if node == mission_final_node:
                reached_final_node = True
        

        def can_reach_node(node, child, _=None):
            if child not in positions_map:
                return False

            tile_position = positions_map[child]
            is_reachable = PathFinder.is_reachable(layer, player_position, tile_position, player_status)
            return is_reachable

        GNode.traverse_nodes_depth_first(mission_start_node, visit_method, can_reach_node)

        if give_failure_reason:
            if reached_node_too_soon:
                return False, "trivial"
            if not reached_final_node:
                return False, "unsolvable"
            return True, ""
        else:
            return reached_final_node and not reached_node_too_soon


    @staticmethod
    def update_player_and_layer_status(layer, player_status, current_node, positions_map):
        current_position = tuple(positions_map[current_node])
        current_tile = layer[current_position]
        if isinstance(current_node, Start):
            pass
        elif isinstance(current_node, End):
            pass
        elif isinstance(current_node, Key):
            player_status.add_to_key_count(current_tile)
        elif isinstance(current_node, Lock):
            player_status.remove_from_key_count(current_tile)
            layer[current_position] = Tiles.empty
        elif isinstance(current_node, GNode):
            player_status.collectable_count += 1
        pass
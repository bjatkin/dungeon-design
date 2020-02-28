from validation.path_finder import PathFinder
from validation.player_status import PlayerStatus
from dungeon_level.dungeon_tiles import Tiles
from dungeon_level.level import Level
from graph_structure.graph_node import GNode, Start, End, Key, Lock

import numpy as np

class Solver:
    @staticmethod
    def does_level_follow_mission(level, solution_node_order, positions_map, give_failure_reason=False):
        layer = np.array(level.upper_layer)
        visited_nodes = set()
        player_status = PlayerStatus(level.required_collectable_count)
        unreached = set(solution_node_order)

        for i, node in enumerate(solution_node_order):
            if i > 0: # We don't need to check if we can reach the first node, since we start there
                if not Solver.can_reach_node(node, positions_map, layer, player_status):
                    return Solver.get_return_result(False, False, give_failure_reason)

            Solver.update_state(layer, player_status, node, positions_map, visited_nodes)

            if not Solver.are_correct_nodes_reachable(node, unreached, solution_node_order, positions_map, layer, player_status):
                return Solver.get_return_result(True, False, give_failure_reason)
            
        # We've made it to the final node, rejoice!
        return Solver.get_return_result(False, True, give_failure_reason)


    @staticmethod
    def are_correct_nodes_reachable(current_node, unreached, solution_node_order, positions_map, layer, player_status):
        unreached -= set(current_node.child_s)
        if current_node in unreached:
            unreached.remove(current_node)
        # unreached -= set([current_node])
        # unreached -= visited_nodes.union(set(current_node.child_s))
        can_reach_unreachables = [Solver.can_reach_node(n, positions_map, layer, player_status) for n in unreached]
        if isinstance(current_node, Key):
            can_reach_reachables = [True]
        else:
            new_reachable_nodes = set(current_node.child_s).intersection(solution_node_order)
            can_reach_reachables = [Solver.can_reach_node(n, positions_map, layer, player_status) for n in new_reachable_nodes]

        are_correct_nodes_reachable = all(can_reach_reachables) and not any(can_reach_unreachables)
        return are_correct_nodes_reachable


    @staticmethod
    def get_return_result(reached_node_too_soon, reached_final_node, give_failure_reason):
        if give_failure_reason:
            if reached_node_too_soon:
                return False, "trivial"
            if not reached_final_node:
                return False, "unsolvable"
            return True, ""
        else:
            return reached_final_node and not reached_node_too_soon


    @staticmethod
    def can_reach_node(node, positions_map, layer, player_status):
        if node not in positions_map:
            return False
        tile_position = positions_map[node]
        is_reachable = PathFinder.is_reachable(layer, player_status.player_position, tile_position, player_status)
        return is_reachable


    @staticmethod
    def update_state(layer, player_status, current_node, positions_map, visited_nodes):
        visited_nodes.add(current_node)
        player_status.player_position = positions_map[current_node]
        current_position = tuple(player_status.player_position)
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
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
    def update_player_and_layer_status(layer, player_status, child_node, positions_map):
        if isinstance(child_node, Start):
            pass
        elif isinstance(child_node, End):
            pass
        elif isinstance(child_node, Key):
            player_status.red_key_count += 1
        elif isinstance(child_node, Lock):
            player_status.red_key_count -= 1
            layer[tuple(positions_map[child_node])] = Tiles.empty
        elif isinstance(child_node, GNode):
            player_status.collectable_count += 1
        pass



    # @staticmethod
    # def find_level_solution_from_mission(level, mission_start_node, positions_map):
    #     player_position = Level.find_tiles(level.upper_layer, Tiles.player)
    #     if player_position.shape[0] == 0:
    #         return False
    #     else:
    #         player_position = player_position[0]

    #     player_status = PlayerStatus(level.required_collectable_count)
    #     end_node = Solver._get_end_node(positions_map.keys())
    #     reached_finish = False
    #     solution_path = [player_position]

    #     def visit_method(node, visited_nodes):
    #         nonlocal player_status
    #         nonlocal player_position
    #         nonlocal reached_finish

    #         player_position = positions_map[node]
    #         Solver.update_player_status(player_status, node)
    #         if isinstance(node, End):
    #             reached_finish = True

    #         if can_reach_node(node, end_node):
    #             reached_finish = True



    #     def can_reach_node(node, child, _=None):
    #         nonlocal solution_path
    #         if reached_finish:
    #             return False

    #         tile_position = positions_map[child]
    #         path = PathFinder.find_path(level.upper_layer, player_position, tile_position, player_status)
    #         if path is not None:
    #             solution_path.extend(path[1:])
    #             return True
    #         else:
    #             return False
        
    #     GNode.traverse_nodes(mission_start_node, visit_method, can_reach_node)

    #     return solution_path

    # @staticmethod
    # def does_solution_path_follow_mission(positions_map, solution_path):
    #     end_position = positions_map[Solver._get_end_node(positions_map.keys())]

    #     if not np.array_equal(solution_path[-1], end_position):
    #         return False

    #     for position in positions_map.values():
    #         has_position = False
    #         for path_position in solution_path:
    #             if np.array_equal(position, path_position):
    #                 has_position = True
    #                 break
    #         if not has_position:
    #             return False

    #     return True


    # @staticmethod
    # def _get_end_node(nodes):
    #     return [node for node in nodes if isinstance(node, End)][0]


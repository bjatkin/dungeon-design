from validation.path_finder import PathFinder
from validation.player_status import PlayerStatus
from validation.sokoban.sokoban_solver import SokobanSolver
from dungeon_level.dungeon_tiles import Tiles, lock_tiles, TileTypes, hazard_tiles
from dungeon_level.level import Level
from graph_structure.graph_node import Start, End, Key, Lock, Collectable, CollectableBarrier
from scipy.ndimage.measurements import label as label_connected_components

import numpy as np

class Solver:
    @staticmethod
    def does_level_follow_mission(level, solution_node_order, positions_map, give_failure_reason=False):
        print(level)
        layer = np.array(level.upper_layer)
        visited_nodes = set()
        reached = set()
        unreached = set(solution_node_order)
        player_status = PlayerStatus(level.required_collectable_count)

        for i, node in enumerate(solution_node_order):
            if not Solver.can_solve_sokoban(layer, player_status, node, positions_map):
                return Solver.get_return_result(False, False, give_failure_reason)

            if i > 0: # We don't need to check if we can reach the first node, since we start there
                if not Solver.can_reach_node(node, positions_map, layer, player_status):
                    return Solver.get_return_result(False, False, give_failure_reason)

            Solver.update_state(layer, player_status, node, positions_map, visited_nodes)

            new_reachable_nodes = Solver.update_reachability(node, unreached, reached, solution_node_order)

            if not Solver.do_keys_open_correct_locks(node, reached, positions_map, layer, player_status):
                return Solver.get_return_result(True, False, give_failure_reason)

            if not Solver.are_correct_nodes_reachable(unreached, new_reachable_nodes, positions_map, layer, player_status):
                return Solver.get_return_result(True, False, give_failure_reason)
            
        # We've made it to the final node, rejoice!
        return Solver.get_return_result(False, True, give_failure_reason)


    @staticmethod
    def get_sokoban_key_position_from_lock(layer, current_node, positions_map):
        if isinstance(current_node, Lock):
            key_node = next(iter(current_node.key_s))
            key_position = positions_map[key_node]
            key_tile = layer[tuple(key_position)]
            if key_tile == Tiles.sokoban_block:
                return key_position
        return None


    @staticmethod
    def can_solve_sokoban(layer, player_status, current_node, positions_map):
        sokoban_key_position = Solver.get_sokoban_key_position_from_lock(layer, current_node, positions_map)
        if not sokoban_key_position is None:
            lock_position = positions_map[current_node]
            can_solve_sokoban = SokobanSolver.is_sokoban_solvable(layer, lock_position, sokoban_key_position, lock_position)
            if can_solve_sokoban:
                layer[tuple(lock_position)] = Tiles.empty
                layer[tuple(sokoban_key_position)] = Tiles.empty
            
            return can_solve_sokoban
        else:
            return True
        


    # We should only be able to unlock a lock if we have reached its key
    @staticmethod
    def do_keys_open_correct_locks(current_node, reached, positions_map, layer, player_status):
        for node in reached:
            if isinstance(node, Lock) and node in positions_map:
                tile = layer[tuple(positions_map[node])]
                if next(iter(node.key_s)) not in reached:
                    if tile.get_tile_type() == TileTypes.key_lock and player_status.get_key_count(tile) > 0:
                        return False
                    elif tile.get_tile_type() == TileTypes.item_hazard and player_status.get_item_count(tile) > 0:
                        return False
        return True


    @staticmethod
    def update_reachability(current_node, unreached, reached, solution_node_order):
        reached.add(current_node)
        if not isinstance(current_node, Key):
            new_reachable_nodes = set(current_node.child_s).intersection(solution_node_order)
            reached.update(new_reachable_nodes)
        else:
            new_reachable_nodes = set()

        unreached -= reached

        return new_reachable_nodes


    @staticmethod
    def are_correct_nodes_reachable(unreached, new_reachable_nodes, positions_map, layer, player_status):
        can_reach_unreachables = [Solver.can_reach_node(n, positions_map, layer, player_status) for n in unreached]

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
        tile_type = current_tile.get_tile_type()

        if isinstance(current_node, Start):
            pass
        elif isinstance(current_node, End):
            pass
        elif isinstance(current_node, Collectable):
            player_status.collectable_count += 1
        elif isinstance(current_node, CollectableBarrier):
            if player_status.collectable_count >= player_status.required_collectable_count:
                layer[current_position] = Tiles.empty
        elif isinstance(current_node, Key):
            if tile_type == TileTypes.key_lock:
                player_status.add_to_key_count(current_tile)
            elif tile_type == TileTypes.item_hazard:
                player_status.add_to_item_count(current_tile)
        elif isinstance(current_node, Lock):
            if tile_type == TileTypes.key_lock:
                player_status.remove_from_key_count(current_tile)
                layer[current_position] = Tiles.empty
            elif tile_type == TileTypes.item_hazard:
                Solver.remove_hazard_component(layer, current_position, current_tile)
        pass

    @staticmethod
    def remove_hazard_component(layer, hazard_position, hazard_tile):
        hazard_mask = (layer == hazard_tile)
        labeled_components, component_count = label_connected_components(hazard_mask)
        hazard_label = labeled_components[hazard_position]
        layer[labeled_components == hazard_label] = Tiles.empty
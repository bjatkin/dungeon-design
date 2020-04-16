from validation.path_finder import PathFinder
from validation.player_traverser import PlayerTraverser
from validation.player_status import PlayerStatus
from validation.sokoban.sokoban_solver import SokobanSolver
from analysis.solution import Solution
from dungeon_level.dungeon_tiles import Tiles, lock_tiles, TileTypes, hazard_tiles
from dungeon_level.level import Level
from graph_structure.graph_node import Start, End, Key, Lock, Collectable, CollectableBarrier, Room, SokobanKey, SokobanLock
from scipy.ndimage.measurements import label as label_connected_components
import copy

import numpy as np

class Solver:
    @staticmethod
    def does_level_follow_mission(level, solution_node_order, positions_map, return_path=False):
        print(level)
        layer = np.array(level.upper_layer)
        solution_node_order = [n for n in solution_node_order if not isinstance(n, Room)]
        visited_nodes = set()
        reached = set()
        unreached = set(solution_node_order)
        player_status = PlayerStatus(level.required_collectable_count)
        solution = Solution(positions_map[solution_node_order[0]])
        player_status.player_position = solution.start_position.copy()

        for i, current_node in enumerate(solution_node_order):
            moves = Solver.can_reach_node(current_node, positions_map, layer, player_status.player_position, return_type="moves")
            if moves is None:
                return False, solution

            is_sokoban_step, sokoban_moves = Solver.get_sokoban_moves(layer, player_status.player_position, current_node, positions_map)
            if is_sokoban_step and sokoban_moves is None:
                return False, solution

            solution.add_step(current_node, moves, sokoban_moves)
            Solver.update_state(layer, player_status, current_node, positions_map, visited_nodes, solution)

            new_reachable_nodes = Solver.update_reachability(current_node, unreached, reached, solution_node_order)

            if not Solver.do_keys_open_correct_locks(current_node, reached, positions_map, layer, player_status):
                return False, solution

            if not Solver.are_correct_nodes_reachable(unreached, new_reachable_nodes, positions_map, layer, player_status.player_position):
                return False, solution
            
        # We've made it to the final node, rejoice!
        return True, solution
    

    @staticmethod
    def remove_rooms_from_solution_nodes(solution_node_order):
        new_nodes = copy.deepcopy(solution_node_order)
        for node in new_nodes:
            if isinstance(node, Room):
                parent = next(iter(node.parent_s))
                for child in node.child_s:
                    child.remove_parent_s(node)
                    child.add_parent_s(parent)
        new_nodes = [n for n in new_nodes if not isinstance(n, Room)]
        return new_nodes


    @staticmethod
    def get_sokoban_key_and_lock(layer, current_node, positions_map):
        if isinstance(current_node, SokobanLock):
            key_node = next(iter(current_node.key_s))
            key_position = positions_map[key_node]
            lock_position = positions_map[current_node]
            return key_position, lock_position
        return None, None


    @staticmethod
    def get_sokoban_moves(layer, player_position, current_node, positions_map):
        sokoban_key_position, sokoban_lock_position = Solver.get_sokoban_key_and_lock(layer, current_node, positions_map)
        if sokoban_key_position is not None:
            sokoban_moves = SokobanSolver.is_sokoban_solvable(layer, player_position, sokoban_key_position, sokoban_lock_position, return_type="moves")
            return True, sokoban_moves
        else:
            return False, None


    # We should only be able to unlock a lock if we have reached its key
    @staticmethod
    def do_keys_open_correct_locks(current_node, reached, positions_map, layer, player_status):
        for node in reached:
            if isinstance(node, Lock) and node in positions_map:
                tile = layer[tuple(positions_map[node])]
                if len(node.key_s) > 0 and next(iter(node.key_s)) not in reached:
                    if tile.get_tile_type() == TileTypes.key_lock and player_status.get_key_count(tile) > 0:
                        return False
                    elif tile.get_tile_type() == TileTypes.item_hazard and player_status.get_item_count(tile) > 0:
                        return False
        return True


    @staticmethod
    def update_reachability(current_node, unreached, reached, solution_node_order):
        reached.add(current_node)
        if not isinstance(current_node, Key):
            children = Solver.get_nodes_skipping_rooms(current_node.child_s, direction="children")
            new_reachable_nodes = set(children).intersection(solution_node_order)
            reached.update(new_reachable_nodes)
        else:
            new_reachable_nodes = set()

        unreached -= reached

        return new_reachable_nodes

    
    @staticmethod
    def get_nodes_skipping_rooms(nodes, direction="children"):
        new_nodes = set()
        for node in nodes:
            if not isinstance(node, Room):
                new_nodes.add(node)
            else:
                if direction == 'children':
                    add_nodes = node.child_s
                else:
                    add_nodes = node.parent_s
                new_nodes.update(add_nodes)
        return new_nodes



    @staticmethod
    def are_correct_nodes_reachable(unreached, new_reachable_nodes, positions_map, layer, player_position):
        can_reach_unreachables = [Solver.can_reach_node(n, positions_map, layer, player_position) for n in unreached]

        can_reach_reachables = [Solver.can_reach_node(n, positions_map, layer, player_position) for n in new_reachable_nodes]

        are_correct_nodes_reachable = all(can_reach_reachables) and not any(can_reach_unreachables)
        return are_correct_nodes_reachable


    @staticmethod
    def can_reach_node(node, positions_map, layer, player_position, return_type="path_exists"):
        if node not in positions_map:
            if return_type == "path_exists":
                return False
            else:
                return None
        tile_position = positions_map[node]
        result = PathFinder.find_path(layer, player_position, tile_position, PlayerTraverser.can_traverse, return_type=return_type)
        return result


    @staticmethod
    def update_state(layer, player_status, current_node, positions_map, visited_nodes, solution):
        visited_nodes.add(current_node)
        current_node_position = tuple(positions_map[current_node])
        current_tile = layer[current_node_position]
        tile_type = current_tile.get_tile_type()
        player_status.player_position = solution.get_final_solution_position()

        if isinstance(current_node, Start):
            pass
        elif isinstance(current_node, End):
            pass
        elif isinstance(current_node, Collectable):
            player_status.collectable_count += 1
        elif isinstance(current_node, CollectableBarrier):
            if player_status.collectable_count >= player_status.required_collectable_count:
                layer[current_node_position] = Tiles.empty
        elif isinstance(current_node, SokobanLock):
            sokoban_key_position, sokoban_lock_position = Solver.get_sokoban_key_and_lock(layer, current_node, positions_map)
            layer[tuple(sokoban_lock_position)] = Tiles.empty
            layer[tuple(sokoban_key_position)] = Tiles.empty
        elif isinstance(current_node, Key):
            if tile_type == TileTypes.key_lock:
                player_status.add_to_key_count(current_tile)
            elif tile_type == TileTypes.item_hazard:
                player_status.add_to_item_count(current_tile)
        elif isinstance(current_node, Lock):
            if tile_type == TileTypes.key_lock:
                player_status.remove_from_key_count(current_tile)
                layer[current_node_position] = Tiles.empty
            elif tile_type == TileTypes.item_hazard:
                Solver.remove_hazard_component(layer, current_node_position, current_tile)


    @staticmethod
    def remove_hazard_component(layer, hazard_position, hazard_tile):
        hazard_mask = (layer == hazard_tile)
        labeled_components, component_count = label_connected_components(hazard_mask)
        hazard_label = labeled_components[hazard_position]
        layer[labeled_components == hazard_label] = Tiles.empty
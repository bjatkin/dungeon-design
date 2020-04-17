import numpy as np
from graph_to_level.spatial_graph import SpatialGraph, SpatialGraphNode
from graph_to_level.subgraph_finder import SubgraphFinder
from dungeon_level.dungeon_tiles import Tiles, mission_tiles, TileTypes, key_tiles, item_tiles, item_to_hazard, key_to_lock
from dungeon_level.level import Level
from validation.solver import Solver
from graph_structure.graph_node import Node, Key, Lock, Start, End, Collectable, CollectableBarrier, Room, SokobanKey, SokobanLock
from log import Log

class MissionGenerator:
    @staticmethod
    def generate_mission(level, mission_aesthetic):
        node_to_tile = dict()
        solution_node_order = Node.find_all_nodes(level.mission, method="topological-sort")

        spatial_graph = SpatialGraph(level.upper_layer)
        mission_spatial_nodes, mission_to_mission_spatial = MissionGenerator.convert_mission_graph_to_spatial_subgraph_form(solution_node_order)
        mission_to_spaces_mapping = SubgraphFinder.get_subgraph_mapping(spatial_graph.nodes, mission_spatial_nodes)
        if mission_to_spaces_mapping is not None:
            MissionGenerator.apply_mission_mapping_to_level(level, solution_node_order, mission_to_mission_spatial, mission_to_spaces_mapping, node_to_tile, mission_aesthetic)

            level.required_collectable_count = np.count_nonzero(level.upper_layer == Tiles.collectable)
            return Solver.does_level_follow_mission(level)
        return False, None


    @staticmethod
    def apply_mission_mapping_to_level(level, solution_node_order, mission_to_mission_spatial, mission_to_spaces_mapping, node_to_tile, mission_aesthetic):
        for mission_node in solution_node_order:
            space_node = mission_to_spaces_mapping[mission_to_mission_spatial[mission_node]]

            if isinstance(mission_node, Lock) or isinstance(mission_node, Room):
                mission_node_parent = [parent for parent in mission_node.parent_s if not isinstance(parent, Key)][0]
                parent_space_node = mission_to_spaces_mapping[mission_to_mission_spatial[mission_node_parent]]
                mask = SpatialGraph.get_shared_edge_mask_between_nodes(space_node, parent_space_node)
            else:
                mask = space_node.mask

            MissionGenerator.add_mission_tile_in_mask(level, mission_node, mask, node_to_tile, mission_aesthetic)


    @staticmethod
    def add_mission_tile_in_mask(level, mission_node, mask, node_to_tile, mission_aesthetic):
        available_space = np.clip(mask - MissionGenerator.get_mission_mask(level.upper_layer), 0, 1)
        random_position = MissionGenerator.get_random_positions_in_mask(available_space)
        if len(random_position) > 0:
            random_position = random_position[0]
        else:
            return
        MissionGenerator.add_mission_tile(level, mission_node, random_position, node_to_tile, mission_aesthetic)


    @staticmethod
    def add_mission_tile(level, node, position, node_to_tile, mission_aesthetic):
        level.add_node_position(node, position)
        position = tuple(position)
        layer = level.upper_layer

        if isinstance(node, Start):
            layer[position] = Tiles.player
        elif isinstance(node, End):
            layer[position] = Tiles.finish
        elif isinstance(node, Collectable):
            layer[position] = Tiles.collectable
        elif isinstance(node, CollectableBarrier):
            layer[position] = Tiles.required_collectable_barrier
        elif isinstance(node, Key):
            key_tile = MissionGenerator.get_matching_tile(node_to_tile, node, mission_aesthetic, get='key')
            layer[position] = key_tile
        elif isinstance(node, Lock):
            lock_tile = MissionGenerator.get_matching_tile(node_to_tile, node, mission_aesthetic, get='lock')
            if lock_tile.get_tile_type() == TileTypes.item_hazard:
                MissionGenerator.spread_hazard(layer, lock_tile, position, mission_aesthetic)
            else:
                layer[position] = lock_tile
        elif isinstance(node, Room):
            layer[position] = Tiles.empty


    @staticmethod
    def spread_hazard(layer, hazard_tile, position, aesthetic_settings):
        offsets = [np.array([-1, 0]), np.array([1, 0]), np.array([0, -1]), np.array([0, 1])]
        spread_probability = aesthetic_settings.hazard_spread_probability[hazard_tile]
        hazard_tile_positions = [position]
        while len(hazard_tile_positions) > 0:
            hazard_tile_position = hazard_tile_positions.pop()

            layer[tuple(hazard_tile_position)] = hazard_tile
            for offset in offsets:
                if np.random.random() < spread_probability:
                    neighbor_hazard_tile_position = tuple(hazard_tile_position + offset)
                    if Level.is_position_within_layer_bounds(layer, neighbor_hazard_tile_position) and layer[neighbor_hazard_tile_position] == Tiles.empty:
                        hazard_tile_positions.append(neighbor_hazard_tile_position)


    @staticmethod
    def get_matching_tile(node_to_tile, node, mission_aesthetic, get='key'):
        if isinstance(node, Key):
            key_node = node
        elif isinstance(node, Lock):
            key_node = next(iter(node.key_s))
        else:
            return None
        
        if key_node not in node_to_tile:
            if isinstance(key_node, SokobanKey):
                node_to_tile[key_node] = Tiles.sokoban_block
            else:
                if len(key_node.lock_s) > 1 or np.random.random() < mission_aesthetic.single_lock_is_hazard_probability:
                    node_to_tile[key_node] = np.random.choice(item_tiles)
                else:
                    node_to_tile[key_node] = np.random.choice(key_tiles)

        tile = node_to_tile[key_node]

        if get == 'key':
            return tile
        elif get == 'lock':
            if tile == Tiles.sokoban_block:
                return Tiles.sokoban_goal
            elif tile.get_tile_type() == TileTypes.key_lock:
                return key_to_lock[tile]
            elif tile.get_tile_type() == TileTypes.item_hazard:
                return item_to_hazard[tile]


    @staticmethod
    def convert_mission_graph_to_spatial_subgraph_form(solution_node_order):
        def is_mission_node_spatial_subgraph_node(node):
            return not (isinstance(node, Key) or isinstance(node, End) or isinstance(node, Collectable))

        subgraph_nodes = set()
        solution_nodes_to_subgraph_nodes = dict()
        for node in solution_node_order:
            if is_mission_node_spatial_subgraph_node(node):
                subgraph_node = Node(node.name)
                subgraph_nodes.add(subgraph_node)
                solution_nodes_to_subgraph_nodes[node] = subgraph_node
        
        for node in solution_node_order:
            if not is_mission_node_spatial_subgraph_node(node):
                solution_nodes_to_subgraph_nodes[node] = solution_nodes_to_subgraph_nodes[next(iter(node.parent_s))]
            else:
                subgraph_node = solution_nodes_to_subgraph_nodes[node]
                for child in node.child_s:
                    if is_mission_node_spatial_subgraph_node(child):
                        subgraph_adjacent_node = solution_nodes_to_subgraph_nodes[child]
                        subgraph_node.add_adjacent_nodes(subgraph_adjacent_node)

        return subgraph_nodes, solution_nodes_to_subgraph_nodes


        

    @staticmethod
    def merge_spaces(layer, spatial_graph, mission_node_to_spatial_node, space_node_a, space_node_b):
        shared_edge_mask = SpatialGraph.get_shared_edge_mask_between_nodes(space_node_a, space_node_b)
        shared_edge_opening_position = MissionGenerator.get_random_positions_in_mask(shared_edge_mask)
        layer[tuple(shared_edge_opening_position)] = Tiles.empty
        spatial_graph.merge_node_b_into_a(space_node_a, space_node_b)


    @staticmethod
    def get_random_positions_in_mask(mask, position_count=1):
        positions_in_mask = np.argwhere(mask == 1)
        if positions_in_mask.shape[0] > 0:
            samples_count = np.minimum(position_count, positions_in_mask.shape[0])
            indices = np.random.choice(positions_in_mask.shape[0], size=samples_count, replace=False)
            random_positions = positions_in_mask[indices,:]
        else:
            random_positions = np.zeros((0,2))

        return random_positions

    @staticmethod
    def get_mission_mask(layer):
        mission_mask = np.zeros(layer.shape)
        for mission_tile in mission_tiles:
            mission_mask = np.logical_or(mission_mask, layer == mission_tile)

        return mission_mask.astype(int)
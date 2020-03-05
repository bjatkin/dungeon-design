from dungeon_level.dungeon_tiles import Tiles, key_to_lock, key_tiles, TileTypes, item_to_hazard, item_tiles, lock_tiles, mission_tiles
from validation.solver import Solver
from graph_structure.graph_node import GNode, Start, End, Key, Lock
from dungeon_level.level import Level
from scipy.ndimage.measurements import label as label_connected_components
from scipy.ndimage import convolve
from skimage.morphology import binary_dilation
from graph_structure.graph import Graph
from log import Log
import numpy as np
import copy

class MissionGenerator:
    @staticmethod
    def generate_mission(level, solution_node_order):
        Log.print(level)
        positions_map = dict()
        node_to_tile = dict()

        start_position = MissionGenerator.get_start_position(level)

        was_successful, level_with_mission = MissionGenerator._generate_mission(level, 0, solution_node_order, positions_map, node_to_tile, start_position)
        level.upper_layer = level_with_mission.upper_layer
        Log.print(level)
        return was_successful


    @staticmethod
    def _generate_mission(level, node_index, solution_node_order, positions_map, node_to_tile, start_position):
        if node_index >= len(solution_node_order):
            return True, level

        level = copy.deepcopy(level)
        positions_map = copy.deepcopy(positions_map)
        node_to_tile = copy.deepcopy(node_to_tile)

        node = solution_node_order[node_index]
        random_positions = MissionGenerator.get_random_positions(level.upper_layer, start_position, node, node_to_tile)
        was_add_successful, level = MissionGenerator.add_mission_node(level, solution_node_order, node, node_index, positions_map, node_to_tile, random_positions, start_position)
        if not was_add_successful:
            return False, level

        return True, level



    @staticmethod
    def add_mission_node(level, solution_node_order, node, node_index, positions_map, node_to_tile, random_positions, start_position):
        original_layer = level.upper_layer.copy()
        for position in random_positions:
            level.upper_layer = original_layer.copy()
            MissionGenerator.add_mission_tile(level.upper_layer, node, position, positions_map, node_to_tile)

            Log.print("\n\n")
            Log.print(level)

            if Solver.does_level_follow_mission(level, solution_node_order[:node_index + 1], positions_map):
                was_successful, level = MissionGenerator._generate_mission(level, node_index + 1, solution_node_order, positions_map, node_to_tile, start_position)
                if was_successful:
                    return was_successful, level
        return False, level


    @staticmethod
    def get_start_position(level):
        components, component_count = MissionGenerator.get_rooms_components(level.upper_layer)
        start_position = MissionGenerator.get_random_positions_per_component(components, component_count)[0]
        return start_position

    @staticmethod
    def get_random_positions(layer, start_position, node, node_to_tile):
        if isinstance(node, Lock):
            return MissionGenerator.get_random_positions_for_lock(layer, start_position)
        elif isinstance(node, Key) or isinstance(node, End):
            return MissionGenerator.get_random_positions_for_key(layer, start_position)
        elif isinstance(node, Start):
            return np.array([start_position])


    @staticmethod
    def get_space_connected_to_position(layer, position):
        empty_mask = (layer != Tiles.wall)
        labeled_components, component_count = label_connected_components(empty_mask)
        label = labeled_components[tuple(position)]
        connected_space = (labeled_components == label)
        return connected_space

    @staticmethod
    def get_walls_and_corridors_connected_to_space(layer, space):
        space = binary_dilation(space)
        wall_corridor_mask = MissionGenerator.get_wall_corridor_mask(layer)
        connected_walls_and_corridors = np.logical_and(space, wall_corridor_mask)
        return connected_walls_and_corridors


    @staticmethod
    def get_random_positions_for_key(layer, start_position):
        connected_space = MissionGenerator.get_space_connected_to_position(layer, start_position).astype(int)
        mission_mask = MissionGenerator.get_mission_mask(layer)
        np.clip(connected_space - mission_mask, 0, 1, out=connected_space)
        random_positions = MissionGenerator.get_random_positions_in_component(connected_space, 1, 3)
        return random_positions
        

    @staticmethod
    def get_random_positions_for_lock(layer, start_position):
        connected_space = MissionGenerator.get_space_connected_to_position(layer, start_position)
        connected_walls_and_corridors = MissionGenerator.get_walls_and_corridors_connected_to_space(layer, connected_space)
        connected_walls_and_corridors_components, component_count = label_connected_components(connected_walls_and_corridors)
        random_positions = MissionGenerator.get_random_positions_per_component(connected_walls_and_corridors_components, component_count, 1)
        return random_positions
    

    @staticmethod
    def get_random_positions_per_component(components_mask, component_count, positions_per_component=1):
        random_position_list = []
        for component_number in range(1, component_count + 1):
            random_positions = MissionGenerator.get_random_positions_in_component(components_mask, component_number, positions_per_component)
            random_position_list.extend(random_positions)
        if len(random_position_list) > 0:
            random_positions = np.vstack(random_position_list)
        else:
            random_positions = np.zeros((0,2))
        np.random.shuffle(random_positions)
        return random_positions

    @staticmethod
    def get_matching_tile(node_to_tile, node, get='key'):
        if isinstance(node, Key):
            key_node = node
        elif isinstance(node, Lock):
            key_node = node.key_s[0]
        else:
            return None
        
        if key_node not in node_to_tile:
            if len(key_node.lock_s) == 1:
                node_to_tile[key_node] = np.random.choice(key_tiles)
            else:
                node_to_tile[key_node] = np.random.choice(item_tiles)

        tile = node_to_tile[key_node]

        if get == 'key':
            return tile
        elif get == 'lock':
            if tile.get_tile_type() == TileTypes.key_lock:
                return key_to_lock[tile]
            elif tile.get_tile_type() == TileTypes.item_hazard:
                return item_to_hazard[tile]


    @staticmethod
    def add_mission_tile(layer, node, position, positions_map, node_to_tile):
            positions_map[node] = position
            position = tuple(position)

            if isinstance(node, Start):
                layer[position] = Tiles.player
            elif isinstance(node, End):
                layer[position] = Tiles.finish
            elif isinstance(node, Key):
                key_tile = MissionGenerator.get_matching_tile(node_to_tile, node, get='key')
                layer[position] = key_tile
            elif isinstance(node, Lock):
                lock_tile = MissionGenerator.get_matching_tile(node_to_tile, node, get='lock')
                if lock_tile.get_tile_type() == TileTypes.item_hazard:
                    MissionGenerator.spread_hazard(layer, lock_tile, position)
                else:
                    layer[position] = lock_tile
            elif isinstance(node, GNode):
                layer[position] = Tiles.collectable

    @staticmethod
    def spread_hazard(layer, hazard_tile, position):
        offsets = [np.array([-1, 0]), np.array([1, 0]), np.array([0, -1]), np.array([0, 1])]
        spread_probability = [0.9, 0.3]
        hazard_tile_positions = [position]
        spread_probability_index = 0
        while len(hazard_tile_positions) > 0:
            hazard_tile_position = hazard_tile_positions.pop()

            layer[tuple(hazard_tile_position)] = hazard_tile
            for offset in offsets:
                if np.random.random() < spread_probability[spread_probability_index]:
                    neighbor_hazard_tile_position = tuple(hazard_tile_position + offset)
                    if Level.is_position_within_layer_bounds(layer, neighbor_hazard_tile_position) and layer[neighbor_hazard_tile_position] == Tiles.empty:
                        hazard_tile_positions.append(neighbor_hazard_tile_position)
            spread_probability_index += 1
            spread_probability_index = np.clip(spread_probability_index, 0, len(spread_probability) - 1)




    @staticmethod
    def get_random_positions_in_component(labeled_layer, component_number, position_count=1):
        mask = (labeled_layer == component_number)
        return MissionGenerator.get_random_positions_in_mask(mask, position_count)


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


    # https://docs.scipy.org/doc/scipy-0.16.0/reference/generated/scipy.ndimage.measurements.label.html
    @staticmethod
    def get_rooms_components(layer):
        empty_mask = (layer == Tiles.empty)
        labeled_components, component_count = label_connected_components(empty_mask)
        return labeled_components, component_count


    @staticmethod
    def get_potential_lock_components(layer):
        potential_lock_mask = MissionGenerator.get_wall_corridor_mask(layer)
        labeled_components, component_count = label_connected_components(potential_lock_mask)
        return labeled_components, component_count


    @staticmethod
    def get_mission_mask(layer):
        mission_mask = np.zeros(layer.shape)
        for mission_tile in mission_tiles:
            mission_mask = np.logical_or(mission_mask, layer == mission_tile)

        return mission_mask.astype(int)


    # Returns a mask representing all the possible locations for a lock
    # https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.filters.convolve.html
    @staticmethod
    def get_wall_corridor_mask(layer):
        convolutional_result1 = 2 # Based on the filter, a horizontal wall has a result == 2
        convolutional_result2 = 8 # Based on the filter, a vertical wall has a result == 8
        # We can't just use a symmetric kernel because we need to ignore corners.
        wall_kernel = np.array([
            [0., 4., 0.],
            [1., 0, 1.],
            [0., 4., 0.],])

        wall_mask = (layer == Tiles.wall).astype(int)
        mission_mask = MissionGenerator.get_mission_mask(layer)
        np.clip(wall_mask - mission_mask, 0, 1, out=wall_mask)
        conv_result = convolve(wall_mask, wall_kernel, mode='constant', cval=1.0)
        wall_corridor_mask = (np.logical_or(conv_result == convolutional_result1, conv_result == convolutional_result2)).astype(int)
        np.clip(wall_corridor_mask - mission_mask, 0, 1, out=wall_corridor_mask)
        return wall_corridor_mask


    @staticmethod
    def generate_mission_graph():
        # graph = Graph()
        # return GNode.find_all_nodes(graph.start, method="topological-sort")


        start = Start()
        key_red = Key("red")
        lock_red = Lock("red")
        flippers = Key("flippers")
        water1 = Lock("water1")
        water2 = Lock("water2")
        key_green = Key("green")
        lock_green = Lock("green")
        fire_boots = Key("fireboots")
        fire1 = Lock("fire1")
        fire2 = Lock("fire2")
        end = End()
        start.add_child_s([fire2, key_red, lock_red])
        key_red.add_lock_s(lock_red)
        lock_red.add_child_s([flippers, water1])
        flippers.add_lock_s([water1, water2])
        water1.add_child_s(water2)
        water2.add_child_s([fire_boots, fire1])
        fire_boots.add_lock_s([fire1, fire2])
        fire1.add_child_s(key_green)
        key_green.add_lock_s(lock_green)
        fire2.add_child_s(lock_green)
        lock_green.add_child_s(end)

        graph = Graph()
        graph.start = start
        graph.end = end
        # graph.draw()

        return GNode.find_all_nodes(start, method="topological-sort")

        # return start, [start, key1, lock1, key2, lock2, key3, lock3, key4, lock4, end]
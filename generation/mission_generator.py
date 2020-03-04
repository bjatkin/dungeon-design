from dungeon_level.dungeon_tiles import Tiles, key_to_lock, key_tiles, TileTypes, item_to_hazard, item_tiles
from validation.solver import Solver
from graph_structure.graph_node import GNode, Start, End, Key, Lock
from scipy.ndimage.measurements import label as label_connected_components
from scipy.ndimage import convolve
from graph_structure.graph import Graph
from log import Log
import numpy as np

class MissionGenerator:
    @staticmethod
    def generate_mission(level, size, solution_node_order):
        positions_map = dict()
        node_to_tile = dict()
        for node_index, node in enumerate(solution_node_order):
            Log.print("Adding {}".format(node))
            if isinstance(node, Lock):
                random_positions = MissionGenerator.find_random_positions_for_lock(level.upper_layer)
            else:
                random_positions = MissionGenerator.find_random_positions_for_key(level.upper_layer)

            i = 0
            previous_tile = None
            previous_position = None
            does_level_follow_mission = False
            while not does_level_follow_mission:
                if previous_tile is not None:
                    level.upper_layer[tuple(previous_position)] = previous_tile

                position = random_positions[i]

                previous_tile = level.upper_layer[tuple(position)]
                previous_position = position

                MissionGenerator.add_mission_tile(level.upper_layer, node, position, positions_map, node_to_tile)
                i += 1
                if i >= random_positions.shape[0]:
                    return positions_map
                Log.print("\n\n")
                Log.print(level)

                does_level_follow_mission = Solver.does_level_follow_mission(level, solution_node_order[:node_index + 1], positions_map)

        return positions_map


    @staticmethod
    def find_random_positions_for_key(layer):
        rooms_mask, rooms_count = MissionGenerator.find_rooms_components(layer)
        random_positions = MissionGenerator.get_random_positions_per_component(rooms_mask, rooms_count)
        return random_positions
        

    @staticmethod
    def find_random_positions_for_lock(layer):
        potential_lock_mask, potential_lock_count = MissionGenerator.find_potential_lock_components(layer)
        random_positions = MissionGenerator.get_random_positions_per_component(potential_lock_mask, potential_lock_count)
        return random_positions
    

    @staticmethod
    def get_random_positions_per_component(components_mask, component_count, positions_per_component=1):
        random_position_list = []
        for component_number in range(1, component_count + 1):
            random_positions = MissionGenerator.get_random_positions_in_component(components_mask, component_number, positions_per_component)
            random_position_list.extend(random_positions)
        random_positions = np.vstack(random_position_list)
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
                layer[position] = lock_tile
            elif isinstance(node, GNode):
                layer[position] = Tiles.collectable


    @staticmethod
    def get_random_positions_in_component(labeled_layer, component_number, position_count=1):
        mask = (labeled_layer == component_number)
        return MissionGenerator.get_random_positions_in_mask(mask, position_count)


    @staticmethod
    def get_random_positions_in_mask(mask, position_count=1):
        positions_in_mask = np.argwhere(mask == 1)
        indices = np.random.choice(positions_in_mask.shape[0], size=position_count, replace=False)
        random_positions = positions_in_mask[indices,:]

        return random_positions


    # https://docs.scipy.org/doc/scipy-0.16.0/reference/generated/scipy.ndimage.measurements.label.html
    @staticmethod
    def find_rooms_components(layer):
        empty_mask = (layer == Tiles.empty)
        labeled_components, component_count = label_connected_components(empty_mask)
        return labeled_components, component_count


    @staticmethod
    def find_potential_lock_components(layer):
        potential_lock_mask = MissionGenerator.find_potential_lock_mask(layer)
        labeled_components, component_count = label_connected_components(potential_lock_mask)
        return labeled_components, component_count


    # Returns a mask representing all the possible locations for a lock
    # https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.filters.convolve.html
    @staticmethod
    def find_potential_lock_mask(layer):
        convolutional_result1 = 2 # Based on the filter, a horizontal wall has a result == 2
        convolutional_result2 = 8 # Based on the filter, a vertical wall has a result == 8
        # We can't just use a symmetric kernel because we need to ignore corners.
        wall_kernel = np.array([
            [0., 4., 0.],
            [1., 0, 1.],
            [0., 4., 0.],])

        wall_mask = (layer == Tiles.wall).astype(int)
        conv_result = convolve(wall_mask, wall_kernel, mode='constant', cval=1.0)
        potential_lock_mask = (np.logical_or(conv_result == convolutional_result1, conv_result == convolutional_result2))
        return potential_lock_mask


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
        graph.draw()

        return GNode.find_all_nodes(start, method="topological-sort")

        # return start, [start, key1, lock1, key2, lock2, key3, lock3, key4, lock4, end]
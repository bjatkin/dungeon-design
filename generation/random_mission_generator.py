from dungeon_level.dungeon_tiles import Tiles, key_to_lock, key_tiles
from generation.drawing import Drawing
from graph_structure.graph_node import GNode, Start, End, Key, Lock
from graph_structure.graph import Graph
from validation.solver import Solver
from scipy.ndimage.measurements import label as label_connected_components
from scipy.ndimage import convolve
import numpy as np

class RandomMissionGenerator:
    @staticmethod
    def generate(level, size):
        size = np.array(size)

        is_solvable = False
        while not is_solvable:
            start_node, mission_graph_nodes = RandomMissionGenerator.generate_mission_graph()
            RandomMissionGenerator.create_initial_level(level, size, mission_graph_nodes)
            print(level)
            positions_map = RandomMissionGenerator.add_mission(level, size, mission_graph_nodes)
            is_solvable = Solver.does_level_follow_mission(level, start_node, mission_graph_nodes[-1], positions_map)


    @staticmethod
    def create_initial_level(level, size, mission_graph_nodes):
        level.upper_layer = np.full(size, Tiles.empty)
        level.lower_layer = np.full(size, Tiles.empty)


        for _ in range(20):
            p0 = RandomMissionGenerator.get_random_positions(size, 1)[0]
            p1 = p0 + RandomMissionGenerator.get_random_positions(np.array([10, 10]), 1)[0] + 4

            Drawing.fill_rectangle(level.upper_layer, p0 + 1, p1 - 1, Tiles.empty)
            Drawing.draw_rectangle(level.upper_layer, p0, p1, Tiles.wall)

        random_positions = RandomMissionGenerator.get_random_positions(size)
        percentage = 0.4
        percentage_index = int(percentage * random_positions.shape[0])
        random_positions = random_positions[:percentage_index]
        for position in random_positions:
            if np.random.randint(2) == 0:
                level.upper_layer[tuple(position)] = Tiles.wall
            else:
                level.upper_layer[tuple(position)] = Tiles.empty

        Drawing.draw_rectangle(level.upper_layer, (0,0), size - 1, Tiles.wall)


    @staticmethod
    def add_mission(level, size, mission_graph_nodes):
        positions_map = dict()
        node_to_key_color = dict()
        for node in mission_graph_nodes:
            print("Adding {}".format(node))
            if isinstance(node, Lock):
                random_positions = RandomMissionGenerator.find_random_positions_for_lock(level.upper_layer)
            else:
                random_positions = RandomMissionGenerator.find_random_positions_for_key(level.upper_layer)

            i = 0
            previous_tile = None
            previous_position = None
            while not Solver.does_level_follow_mission(level, mission_graph_nodes[0], node, positions_map):
                if previous_tile is not None:
                    level.upper_layer[tuple(previous_position)] = previous_tile

                position = random_positions[i]

                previous_tile = level.upper_layer[tuple(position)]
                previous_position = position

                RandomMissionGenerator.add_mission_tile(level.upper_layer, node, position, positions_map, node_to_key_color)
                i += 1
                if i >= random_positions.shape[0]:
                    return positions_map
                print("\n\n")
                print(level)

        return positions_map


    @staticmethod
    def find_random_positions_for_key(layer):
        rooms_mask, rooms_count = RandomMissionGenerator.find_rooms_components(layer)
        random_positions = RandomMissionGenerator.get_random_positions_per_component(rooms_mask, rooms_count)
        return random_positions
        

    @staticmethod
    def find_random_positions_for_lock(layer):
        potential_lock_mask, potential_lock_count = RandomMissionGenerator.find_potential_lock_components(layer)
        random_positions = RandomMissionGenerator.get_random_positions_per_component(potential_lock_mask, potential_lock_count)
        return random_positions
    

    @staticmethod
    def get_random_positions_per_component(components_mask, component_count, positions_per_component=1):
        random_position_list = []
        for component_number in range(1, component_count + 1):
            random_positions = RandomMissionGenerator.get_random_positions_in_component(components_mask, component_number, positions_per_component)
            random_position_list.extend(random_positions)
        random_positions = np.vstack(random_position_list)
        np.random.shuffle(random_positions)
        return random_positions

    @staticmethod
    def get_matching_color(node_to_key_color, node, get='key'):
        if isinstance(node, Key):
            key_node = node
        elif isinstance(node, Lock):
            key_node = node.key_s[0]
        else:
            return None
        
        if key_node not in node_to_key_color:
            node_to_key_color[key_node] = np.random.choice(key_tiles)

        key_color = node_to_key_color[key_node]

        if get == 'key':
            return key_color
        elif get == 'lock':
            return key_to_lock[key_color]


    @staticmethod
    def add_mission_tile(layer, node, position, positions_map, node_to_key_color):
            positions_map[node] = position
            position = tuple(position)
            if isinstance(node, Start):
                layer[position] = Tiles.player
            elif isinstance(node, End):
                layer[position] = Tiles.finish
            elif isinstance(node, Key):
                key_tile = RandomMissionGenerator.get_matching_color(node_to_key_color, node, get='key')
                layer[position] = key_tile
            elif isinstance(node, Lock):
                lock_tile = RandomMissionGenerator.get_matching_color(node_to_key_color, node, get='lock')
                layer[position] = lock_tile
            elif isinstance(node, GNode):
                layer[position] = Tiles.collectable


    @staticmethod
    def get_random_positions_in_component(labeled_layer, component_number, position_count=1):
        mask = (labeled_layer == component_number)
        return RandomMissionGenerator.get_random_positions_in_mask(mask, position_count)


    @staticmethod
    def get_random_positions_in_mask(mask, position_count=1):
        positions_in_mask = np.argwhere(mask == 1)
        indices = np.random.choice(positions_in_mask.shape[0], size=position_count, replace=False)
        random_positions = positions_in_mask[indices,:]

        return random_positions
    

    @staticmethod
    def get_random_positions(size, count=None):
        BORDER = 2
        max_index = np.prod(size - BORDER)
        if count == None:
            count = max_index
        random_indices = np.random.choice(max_index, count, replace=False)
        y_vals = random_indices // (size[1] - BORDER)
        x_vals = random_indices - y_vals * (size[1] - BORDER)
        random_positions = np.stack([y_vals, x_vals], axis=1)
        random_positions += BORDER // 2
        return random_positions


    # https://docs.scipy.org/doc/scipy-0.16.0/reference/generated/scipy.ndimage.measurements.label.html
    @staticmethod
    def find_rooms_components(layer):
        empty_mask = (layer == Tiles.empty)
        labeled_components, component_count = label_connected_components(empty_mask)
        return labeled_components, component_count

    @staticmethod
    def find_potential_lock_components(layer):
        potential_lock_mask = RandomMissionGenerator.find_potential_lock_mask(layer)
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


    i = 0
    @staticmethod
    def generate_mission_graph():
        RandomMissionGenerator.i += 1
        if RandomMissionGenerator.i % 2 == 0:
            graph = Graph()
            graph.convert_graph_to_mission_format()

            return graph.start, GNode.find_all_nodes(graph.start, method="breadth-first")


        start = Start()
        key1 = Key("red")
        lock1 = Lock("red")
        key2 = Key("blue")
        lock2 = Lock("blue")
        key3 = Key("green")
        lock3 = Lock("green")
        key4 = Key("yellow")
        lock4 = Lock("yellow")
        end = End()
        start.add_child_s(key1)
        key1.add_child_s(lock1)
        key1.add_lock_s(lock1)
        lock1.add_child_s(key2)
        key2.add_child_s(lock2)
        key2.add_lock_s(lock2)
        lock2.add_child_s(key3)
        key3.add_child_s(lock3)
        key3.add_lock_s(lock3)
        lock3.add_child_s(key4)
        key4.add_child_s(lock4)
        key4.add_lock_s(lock4)
        lock4.add_child_s(end)

        return start, [start, key1, lock1, key2, lock2, key3, lock3, key4, lock4, end]
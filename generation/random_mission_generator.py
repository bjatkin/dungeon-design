from dungeon_level.dungeon_tiles import Tiles
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
        start_node, mission_graph_nodes = RandomMissionGenerator.generate_mission_graph()

        is_solvable = False
        while not is_solvable:
            RandomMissionGenerator.create_initial_level(level, size, mission_graph_nodes)
            positions_map = RandomMissionGenerator.add_mission(level, size, mission_graph_nodes)
            is_solvable = Solver.does_level_follow_mission(level, start_node, mission_graph_nodes[-1], positions_map)


    @staticmethod
    def create_initial_level(level, size, mission_graph_nodes):
        level.upper_layer = np.full(size, Tiles.empty)
        level.lower_layer = np.full(size, Tiles.empty)

        # random_positions = RandomMissionGenerator.get_random_positions(size)
        # percentage = 0.4
        # percentage_index = int(percentage * random_positions.shape[0])
        # random_positions = random_positions[:percentage_index]
        # for position in random_positions:
        #     level.upper_layer[tuple(position)] = Tiles.wall

        for _ in range(20):
            p0 = RandomMissionGenerator.get_random_positions(size, 1)[0]
            p1 = p0 + RandomMissionGenerator.get_random_positions(np.array([10, 10]), 1)[0] + 4
            # p1 = p0 + RandomMissionGenerator.get_random_positions(np.array([20, 20]), 1)[0] - 10
            # p1 = np.array(p0)
            # p1[np.random.randint(2)] += np.random.randint(10)

            Drawing.fill_rectangle(level.upper_layer, p0 + 1, p1 - 1, Tiles.empty)
            Drawing.draw_rectangle(level.upper_layer, p0, p1, Tiles.wall)


        Drawing.draw_rectangle(level.upper_layer, (0,0), size - 1, Tiles.wall)


    @staticmethod
    def add_mission(level, size, mission_graph_nodes):
        positions_map = dict()
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

                RandomMissionGenerator.add_mission_tile(level.upper_layer, node, position, positions_map)
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
        for component_number in range(component_count):
            random_positions = RandomMissionGenerator.get_random_positions_in_component(components_mask, component_number, positions_per_component)
            random_position_list.extend(random_positions)
        random_positions = np.vstack(random_position_list)
        np.random.shuffle(random_positions)
        return random_positions


    @staticmethod
    def add_mission_tile(layer, node, position, positions_map):
            positions_map[node] = position
            position = tuple(position)
            if isinstance(node, Start):
                layer[position] = Tiles.player
            elif isinstance(node, End):
                layer[position] = Tiles.finish
            elif isinstance(node, Key):
                layer[position] = Tiles.key_red
            elif isinstance(node, Lock):
                layer[position] = Tiles.lock_red
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


    @staticmethod
    def generate_mission_graph():
        graph = Graph()
        graph.convert_graph_to_mission_format()

        return graph.start, GNode.find_all_nodes(graph.start, method="breadth-first")


from dungeon_level.dungeon_tiles import Tiles
from generation.drawing import Drawing
from graph_structure.graph_node import GNode, Start, End, Key, Lock
from graph_structure.graph import Graph
from validation.solver import Solver
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
    def add_mission(level, size, mission_graph_nodes):
        positions_map = dict()
        for node in mission_graph_nodes:
            print("Adding {}".format(node))
            random_positions = RandomMissionGenerator.get_random_positions(size)
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
    def create_initial_level(level, size, mission_graph_nodes):
        level.upper_layer = np.full(size, Tiles.empty)
        level.lower_layer = np.full(size, Tiles.empty)

        random_positions = RandomMissionGenerator.get_random_positions(size)
        percentage = 0.4
        percentage_index = int(percentage * random_positions.shape[0])
        random_positions = random_positions[:percentage_index]
        for position in random_positions:
            level.upper_layer[tuple(position)] = Tiles.wall

        # for _ in range(20):
        #     p0 = RandomMissionGenerator.get_random_positions(size, 1)[0]
        #     p1 = p0 + RandomMissionGenerator.get_random_positions(np.array([20, 20]), 1)[0] - 10
        #     # p1 = np.array(p0)
        #     # p1[np.random.randint(2)] += np.random.randint(10)

        #     Drawing.draw_line(level.upper_layer, p0, p1, Tiles.wall)


        Drawing.draw_rectangle(level.upper_layer, (0,0), size - 1, Tiles.wall)



    @staticmethod
    def generate_mission_graph():
        graph = Graph()
        graph.convert_graph_to_mission_format()

        return graph.start, GNode.find_all_nodes(graph.start, method="breadth-first")




        # a = Start()
        # b = Key("key1")
        # c = Lock("lock1")
        # d = Key("key2")
        # e = Lock("lock2")
        # f = End()
        # a.add_child_s(b)
        # b.add_child_s(c)
        # c.add_child_s(d)
        # d.add_child_s(e)
        # e.add_child_s(f)

        # return a, GNode.find_all_nodes(a, method="breadth-first")

        # start = Start()
        # key1 = Key("key1")
        # lock1 = Lock("lock1")
        # key2 = Key("key2")
        # lock2 = Lock("lock2")
        # end = End()
        # start.add_child_s(lock1)
        # start.add_child_s(key1)
        # key1.add_child_s(lock1)
        # lock1.add_child_s(lock2)
        # lock1.add_child_s(key2)
        # key2.add_child_s(lock2)
        # lock2.add_child_s(end)

        # return start, GNode.find_all_nodes(start, method="breadth-first")
from dungeon_level.dungeon_tiles import Tiles
from generation.drawing import Drawing
from graph_structure.graph_node import GNode, Start, End, Key, Lock
from validation.solver import Solver
import numpy as np

class RandomMissionGenerator:
    @staticmethod
    def generate(level, size):
        size = np.array(size)
        start_node, mission_graph_nodes = RandomMissionGenerator.generate_mission_graph()
        positions_map = RandomMissionGenerator.create_level(level, size, mission_graph_nodes)

        while not Solver.does_level_follow_mission(level, start_node, positions_map):
            positions_map = RandomMissionGenerator.create_level(level, size, mission_graph_nodes)
        

    @staticmethod
    def create_level(level, size, mission_graph_nodes):
        positions_map = dict()
        level.upper_layer = np.full(size, Tiles.empty)
        level.lower_layer = np.full(size, Tiles.empty)

        for _ in range(5):
            p0 = RandomMissionGenerator.get_random_point(size)
            p1 = np.array(p0)
            p1[np.random.randint(2)] += np.random.randint(10)

            Drawing.draw_line(level.upper_layer, p0, p1, Tiles.wall)

        for node in mission_graph_nodes:
            position = RandomMissionGenerator.get_random_point(size)
            positions_map[node] = position
            if isinstance(node, Start):
                level.upper_layer[tuple(position)] = Tiles.player
            elif isinstance(node, End):
                level.upper_layer[tuple(position)] = Tiles.finish
            elif isinstance(node, Key):
                level.upper_layer[tuple(position)] = Tiles.key_red
            elif isinstance(node, Lock):
                level.upper_layer[tuple(position)] = Tiles.lock_red
            elif isinstance(node, GNode):
                level.upper_layer[tuple(position)] = Tiles.collectable

        Drawing.draw_rectangle(level.upper_layer, (0,0), size - 1, Tiles.wall)

        return positions_map



    @staticmethod
    def get_random_point(size):
        return np.array([
            np.random.randint(1, size[0] - 1),
            np.random.randint(1, size[1] - 1) ])


    @staticmethod
    def generate_mission_graph():
        a = Start()
        b = Key("key1")
        c = Lock("lock1")
        d = Key("key2")
        e = Lock("lock2")
        f = End()
        a.add_child_s(b)
        b.add_child_s(c)
        c.add_child_s(d)
        d.add_child_s(e)
        e.add_child_s(f)
        return a, [a, b, c, d, e, f]
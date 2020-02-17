from dungeon_level.dungeon_tiles import Tiles
from generation.drawing import Drawing
from generation.random_generator import RandomGenerator
from graph_structure.graph_node import GNode, Start, End, Key, Lock
from graph_to_level.spatial_graph_generator import SpatialGraphGenerator
from graph_to_level.spatial_graph_visualizer import SpatialGraphVisualizer
import matplotlib.pyplot as plt
import numpy as np

class MissionGenerator:
    @staticmethod
    def generate(level, size):
        start_node, mission_graph_nodes = MissionGenerator.generate_mission_graph()
        spatial_nodes, positions, adjacency_matrix = SpatialGraphGenerator.generate_spatial_graph(MissionGenerator.generate_spatial_graph()[0], size)

        # img = SpatialGraphVisualizer.visualize_graph(positions, adjacency_matrix)
        # plt.imshow(img)
        # plt.show()

        MissionGenerator.dig_dungeons(level, size, positions, adjacency_matrix)
        mission_space_map = MissionGenerator.map_mission_to_space(mission_graph_nodes, positions)
        collectables_count = MissionGenerator.place_mission_in_space(level, mission_space_map)
        level.required_collectable_count = collectables_count


    @staticmethod
    def place_mission_in_space(level, mission_space_map):
        collectables_count = 0
        for node, position in mission_space_map.items():
            position = tuple(position)
            if isinstance(node, Start):
                level.upper_layer[position] = Tiles.player
            elif isinstance(node, End):

                finish_offsets = [np.array([-1, 0]), np.array([1, 0]), np.array([0, -1]), np.array([0, 1]), np.array([0, 0])]
                finish_tiles = [Tiles.wall, Tiles.required_collectable_barrier, Tiles.wall, Tiles.wall, Tiles.finish]
                RandomGenerator.place_feature(level, level.upper_layer.shape, finish_tiles, finish_offsets, position)

            elif isinstance(node, Key):
                level.upper_layer[position] = Tiles.key_red
            elif isinstance(node, Lock):
                level.upper_layer[position] = Tiles.lock_red
                level.lower_layer[position] = Tiles.collectable
                collectables_count += 1

        return collectables_count

    @staticmethod
    def map_mission_to_space(mission_graph_nodes, positions):
        mission_space_map = dict()
        position_count, _ = positions.shape
        for node in mission_graph_nodes:
            position = positions[np.random.randint(position_count)]
            mission_space_map[node] = position

        return mission_space_map


    @staticmethod
    def dig_dungeons(level, size, positions, adjacency_matrix):
        level.upper_layer = np.full(size, Tiles.wall)
        level.upper_layer = np.pad(level.upper_layer, 1, mode='constant', constant_values=Tiles.wall)
        level.lower_layer = np.full(size, Tiles.empty)
        for position in positions:
            Drawing.fill_ellipse(level.upper_layer, position, 3, 3, Tiles.empty)
        
        count, _ = positions.shape
        for i in range(count):
            for j in range(count):
                if adjacency_matrix[i, j] == 1:
                    p1 = positions[i]
                    p2 = positions[j]
                    Drawing.draw_line(level.upper_layer, p1, p2, Tiles.empty)
                    Drawing.draw_line(level.upper_layer, (p1[0] - 1, p1[1]), (p2[0] - 1, p2[1]), Tiles.empty)


    @staticmethod
    def generate_spatial_graph():
        return MissionGenerator.generate_mission_graph()


    @staticmethod
    def generate_mission_graph():
        a = Start()
        b = GNode([], [], "b")
        c = Key(name="c")
        d = GNode([], [], "d")
        e = End()
        f = Lock(name="f")
        g = GNode([], [], "g")

        a.add_child_s(b)
        a.add_child_s(c)
        a.add_child_s(d)
        b.add_child_s(e)
        c.add_child_s(f)
        c.add_child_s(g)
        f.add_key_s(c)
        c.add_lock_s(f)

        return a, {a, b, c, d, e, f, g}
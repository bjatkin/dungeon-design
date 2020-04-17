from dungeon_level.dungeon_tiles import Tiles, key_to_lock, key_tiles
from graph_structure.graph_node import GNode, Start, End, Key, Lock, Node
from graph_structure.graph import Graph
from graph_structure.graph_visualizer import GraphVisualizer
from validation.solver import Solver
from generation.mission_generator import MissionGenerator
from generation.level_space_generator import LevelSpaceGenerator
from generation.image_level_generator import ImageLevelGenerator
from generation.level_tweaker import LevelTweaker
from log import Log
import numpy as np
import string
import time

class Generator:
    LEVEL_PASSWORD_LENGTH = 4
    @staticmethod
    def generate(level_type, size, aesthetic_settings, max_retry_count=500, pregenerated_solution_node_order=None, pregenerated_level_layer=None, draw_graph=False):
        level = level_type()
        size = np.array(size)

        start_time = time.time()
        for retry_count in range(max_retry_count):
            Generator._set_level_space(level, size, pregenerated_level_layer, aesthetic_settings.level_space_aesthetic)
            solution_node_order = Generator._get_mission_graph(pregenerated_solution_node_order, aesthetic_settings.mission_graph_aesthetic, draw_graph)
            is_solvable, solution = MissionGenerator.generate_mission(level, solution_node_order, aesthetic_settings.mission_aesthetic)
            if is_solvable:
                LevelTweaker.tweak_level(level, aesthetic_settings.tweaker_aesthetic)
                Generator._set_level_properties(level, solution, solution_node_order[0], aesthetic_settings)
                break

        end_time = time.time()
        # Log.print("Level generated in {} seconds".format(end_time - start_time))
        return is_solvable, level


    @staticmethod
    def _set_level_properties(level, solution, mission, aesthetic_settings):
        level.mission = mission
        level.solution = solution
        level.map_title = "Level"
        level.password = "".join(np.random.choice(list(string.ascii_uppercase), Generator.LEVEL_PASSWORD_LENGTH))

        min_seconds = aesthetic_settings.mission_aesthetic.min_seconds_per_move
        max_seconds = aesthetic_settings.mission_aesthetic.max_seconds_per_move
        seconds_per_move = np.random.uniform(min_seconds, max_seconds, len(level.solution.get_flattened_moves()))
        level.time_limit = int(sum(seconds_per_move))


    @staticmethod
    def _set_level_space(level, size, pregenerated_level_layer, level_space_aesthetic):
        if pregenerated_level_layer is None:
            LevelSpaceGenerator.generate(level, size, level_space_aesthetic)
        else:
            level.upper_layer = pregenerated_level_layer.copy()


    @staticmethod
    def _get_mission_graph(pregenerated_solution_node_order, mission_graph_aesthetic, draw=False):
        if pregenerated_solution_node_order is None:
            return Generator._generate_mission_graph(mission_graph_aesthetic, draw)
        else:
            return pregenerated_solution_node_order

    @staticmethod
    def _generate_mission_graph(mission_graph_aesthetic, draw=False):
        graph = Graph(mission_graph_aesthetic)
        if draw:
            GraphVisualizer.show_graph(graph.start)

        return Node.find_all_nodes(graph.start, method="topological-sort")
        # return Generator._get_simple_graph()


    @staticmethod
    def _get_simple_graph():
        start = Start()
        key = Key()
        lock = Lock()
        end = End()
        start.add_child_s([key, lock])
        key.add_lock_s(lock)
        lock.add_child_s(end)

        return Node.find_all_nodes(start, method="topological-sort")


    @staticmethod
    def _get_water_lock_graph():
        start = Start()
        key_red = Key("red")
        lock_red = Lock("red")
        flippers = Key("flippers")
        water = Lock("water")
        end = End()

        start.add_child_s([flippers, water, lock_red])
        flippers.add_lock_s(water)
        water.add_child_s(key_red)
        key_red.add_lock_s(lock_red)
        lock_red.add_child_s(end)

        return Node.find_all_nodes(start, method="topological-sort")

    @staticmethod
    def _get_lock_water_fire_lock_graph():
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


        return Node.find_all_nodes(start, method="topological-sort")
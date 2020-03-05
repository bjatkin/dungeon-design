from dungeon_level.dungeon_tiles import Tiles, key_to_lock, key_tiles
from graph_structure.graph_node import GNode, Start, End, Key, Lock
from graph_structure.graph import Graph
from validation.solver import Solver
import numpy as np
from generation.mission_generator import MissionGenerator
from generation.level_space_generator import LevelSpaceGenerator
from generation.image_level_generator import ImageLevelGenerator
import time

class Generator:
    @staticmethod
    def generate(level, size, max_retry_count=500, pregenerated_solution_node_order=None, pregenerated_level_layer=None):
        size = np.array(size)

        start_time = time.time()
        for retry_count in range(max_retry_count):
            Generator._set_level_space(level, size, pregenerated_level_layer)
            solution_node_order = Generator._get_mission_graph(pregenerated_solution_node_order)
            is_solvable = MissionGenerator.generate_mission(level, solution_node_order)
            if is_solvable:
                break
        end_time = time.time()
        Log.print("Level generated in {} seconds".format(end_time - start_time))
        return is_solvable

    @staticmethod
    def _set_level_space(level, size, pregenerated_level_layer):
        if pregenerated_level_layer is None:
            LevelSpaceGenerator.generate(level, size)
        else:
            level.upper_layer = pregenerated_level_layer


    @staticmethod
    def _get_mission_graph(pregenerated_solution_node_order):
        if pregenerated_solution_node_order is None:
            return MissionGenerator.generate_mission_graph()
        else:
            return pregenerated_solution_node_order

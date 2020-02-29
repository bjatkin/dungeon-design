from dungeon_level.dungeon_tiles import Tiles, key_to_lock, key_tiles
from graph_structure.graph_node import GNode, Start, End, Key, Lock
from graph_structure.graph import Graph
from validation.solver import Solver
import numpy as np
from generation.mission_generator import MissionGenerator
from generation.level_space_generator import LevelSpaceGenerator
from generation.image_level_generator import ImageLevelGenerator

class Generator:
    @staticmethod
    def generate(level, size):
        size = np.array(size)

        is_solvable = False
        while not is_solvable:
            # Comment this out and uncomment the code below to go back to normal random generation...
            ImageLevelGenerator.generate(level, size)
            is_solvable = True

            # LevelSpaceGenerator.generate(level, size)
            # solution_node_order = MissionGenerator.generate_mission_graph()
            # positions_map = MissionGenerator.generate_mission(level, size, solution_node_order)
            # is_solvable = Solver.does_level_follow_mission(level, solution_node_order, positions_map)
        pass
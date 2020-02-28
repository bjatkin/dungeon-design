from dungeon_level.dungeon_tiles import Tiles, key_to_lock, key_tiles
from graph_structure.graph_node import GNode, Start, End, Key, Lock
from graph_structure.graph import Graph
from validation.solver import Solver
import numpy as np
from generation.mission_generator import MissionGenerator
from generation.level_space_generator import LevelSpaceGenerator

class Generator:
    @staticmethod
    def generate(level, size):
        size = np.array(size)

        is_solvable = False
        while not is_solvable:
            LevelSpaceGenerator.generate_level_space(level, size)

            solution_node_order = MissionGenerator.generate_mission_graph()
            positions_map = MissionGenerator.generate_mission(level, size, solution_node_order)
            is_solvable = Solver.does_level_follow_mission(level, solution_node_order, positions_map)
        pass
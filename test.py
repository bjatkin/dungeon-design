import unittest
from tile_world.tile_world_writer.test_level_writer import TestTileWorldLevel
from validation.test_path_finder import TestPathFinder
from validation.test_solver import TestSolver
from graph_structure.test_graph_node import TestGraphNode
from graph_to_level.test_unraveler import TestUnraveler
from graph_to_level.test_spatial_graph_generator import TestSpatialGraphGenerator
from generation.test_drawing import TestDrawing
from generation.test_mission_generator import TestMissionGenerator
from log import Log

Log.verbose = True

unittest.main()
import unittest
import numpy as np
from tile_world.tile_world_writer.tile_world_solution_writer import TileWorldSolutionWriter

class TestTileWorldSolutionWriter(unittest.TestCase):
    def test_convert_solution_to_json(self):
        solution = np.array([
            [1,0],
            [0,1],
            [-1,0],
            [0,-1]])

        json_data = TileWorldSolutionWriter.convert_solution_to_json(solution)
        expected_json_data = "{\"Moves\": \"d-r-u-l\", \"Seed\": \"0\", \"Step\": \"EVEN\"}"
        self.assertEqual(json_data, expected_json_data)


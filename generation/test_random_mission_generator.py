import unittest
from generation.random_mission_generator import RandomMissionGenerator
from dungeon_level.dungeon_tiles import Tiles
import numpy as np

e = Tiles.empty
w = Tiles.wall
s = Tiles.player
f = Tiles.finish
l = Tiles.lock_red
k = Tiles.key_red

class TestRandomMissionGenerator(unittest.TestCase):
    def test_find_rooms(self):
        layer = np.array([
            [e, e, w, w, e, w],
            [e, e, e, w, w, w],
            [w, w, e, w, e, e],
            [e, e, e, w, e, w],
            [w, w, w, e, e, w],
            [e, e, e, w, w, w]], dtype=object)
        
        labels, count = RandomMissionGenerator.find_rooms(layer)
        expected_labels = np.array([
            [1, 1, 0, 0, 2, 0],
            [1, 1, 1, 0, 0, 0],
            [0, 0, 1, 0, 3, 3],
            [1, 1, 1, 0, 3, 0],
            [0, 0, 0, 3, 3, 0],
            [4, 4, 4, 0, 0, 0]])
        
        self.assertTrue(np.array_equal(labels, expected_labels))
    
    def test_get_random_position_in_component(self):
        labeled_layer = np.array([
            [1, 1, 0, 0, 2, 0],
            [1, 1, 1, 0, 0, 0],
            [0, 0, 1, 0, 3, 3],
            [1, 1, 1, 0, 3, 0],
            [0, 0, 0, 3, 3, 0],
            [4, 4, 4, 0, 0, 0]])
        
        np.random.seed(1)
        position = RandomMissionGenerator.get_random_positions_in_component(labeled_layer, 1)
        self.assertTrue(np.array_equal(position, np.array([3, 2])))

        position = RandomMissionGenerator.get_random_positions_in_component(labeled_layer, 1, 6)

        self.assertTrue(np.array_equal(position, np.array([
            [1, 1],
            [3, 1],
            [3, 0],
            [1, 0],
            [2, 2],
            [1, 2],
            ])))

        position = RandomMissionGenerator.get_random_positions_in_component(labeled_layer, 2)
        self.assertTrue(np.array_equal(position, np.array([0, 4])))

        position = RandomMissionGenerator.get_random_positions_in_component(labeled_layer, 3, 3)
        self.assertTrue(np.array_equal(position, np.array([
            [4, 3],
            [2, 4],
            [2, 5],
            ])))

    def test_find_potential_lock_mask(self):
        layers = np.array([
            [[e, w, e],
            [e, w, e],
            [e, w, e]],

            [[e, w, e],
            [e, e, e],
            [e, w, e]],

            [[e, e, e],
            [w, w, w],
            [e, e, e]],

            [[e, e, e],
            [w, e, w],
            [e, e, e]],

            [[e, w, e],
            [w, w, w],
            [e, w, e]],

            [[e, w, e],
            [w, e, w],
            [e, w, e]],

            [[e, e, e],
            [e, w, e],
            [e, e, e]],

            [[e, e, e],
            [e, e, e],
            [e, e, e]],

            [[e, w, e],
            [e, w, e],
            [e, e, e]],

            [[e, w, e],
            [e, e, e],
            [e, e, e]],

            [[e, e, e],
            [w, w, e],
            [e, e, e]],

            [[e, e, e],
            [w, e, e],
            [e, e, e]],

            [[e, w, e],
            [w, w, e],
            [e, e, e]],

            [[e, w, e],
            [w, e, e],
            [e, e, e]],

            [[e, w, e],
            [e, w, w],
            [e, e, e]],

            [[e, w, e],
            [e, e, w],
            [e, e, e]],

            ], dtype=object)

        expected_results = [True] * 4 + [False] * 12

        for i, layer in enumerate(layers):
            single_walls = RandomMissionGenerator.find_potential_lock_mask(layer)
            self.assertEqual(single_walls[1,1], expected_results[i])


        
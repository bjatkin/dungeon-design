import unittest
from graph_structure.graph_node import GNode, Start, End, Key, Lock
from generation.mission_generator import MissionGenerator
from dungeon_level.dungeon_tiles import Tiles
from dungeon_level.level import Level
from validation.solver import Solver
from log import Log

import numpy as np

e = Tiles.empty
w = Tiles.wall
s = Tiles.player
f = Tiles.finish
l = Tiles.lock_red
k = Tiles.key_red

class TestMissionGenerator(unittest.TestCase):
    def test_find_rooms_components(self):
        layer = np.array([
            [e, e, w, w, e, w],
            [e, e, e, w, w, w],
            [w, w, e, w, e, e],
            [e, e, e, w, e, w],
            [w, w, w, e, e, w],
            [e, e, e, w, w, w]], dtype=object)
        
        labels, count = MissionGenerator.find_rooms_components(layer)
        expected_labels = np.array([
            [1, 1, 0, 0, 2, 0],
            [1, 1, 1, 0, 0, 0],
            [0, 0, 1, 0, 3, 3],
            [1, 1, 1, 0, 3, 0],
            [0, 0, 0, 3, 3, 0],
            [4, 4, 4, 0, 0, 0]])
        
        self.assertTrue(np.array_equal(labels, expected_labels))

    def test_find_rooms_components_with_other_tiles(self):
        layer = np.array([
            [e, e, w, w, s, w],
            [e, e, e, w, w, w],
            [w, w, l, w, e, e],
            [e, e, e, w, k, w],
            [w, w, w, e, e, w],
            [e, f, e, w, w, w]], dtype=object)

        labels, count = MissionGenerator.find_rooms_components(layer)
        expected_labels = np.array([
            [1, 1, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 2, 2],
            [3, 3, 3, 0, 0, 0],
            [0, 0, 0, 4, 4, 0],
            [5, 0, 6, 0, 0, 0]])
        
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
        position = MissionGenerator.get_random_positions_in_component(labeled_layer, 1)
        self.assertTrue(np.array_equal(position[0], np.array([3, 2])))

        position = MissionGenerator.get_random_positions_in_component(labeled_layer, 1, 6)

        self.assertTrue(np.array_equal(position, np.array([
            [1, 1],
            [3, 1],
            [3, 0],
            [1, 0],
            [2, 2],
            [1, 2],
            ])))

        position = MissionGenerator.get_random_positions_in_component(labeled_layer, 2)
        self.assertTrue(np.array_equal(position[0], np.array([0, 4])))

        position = MissionGenerator.get_random_positions_in_component(labeled_layer, 3, 3)
        self.assertTrue(np.array_equal(position, np.array([
            [4, 3],
            [2, 4],
            [2, 5],
            ])))

    def test_find_potential_lock_mask_edges(self):
        layer = np.array([
            [w, w, w, w, w],
            [w, e, e, e, w],
            [w, e, e, e, w],
            [w, e, e, e, w],
            [w, w, w, w, w]], dtype=object)

        expected_results = np.zeros([5,5])
        results = MissionGenerator.find_potential_lock_mask(layer)
        self.assertTrue(np.array_equal(results, expected_results))

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
            single_walls = MissionGenerator.find_potential_lock_mask(layer)
            self.assertEqual(single_walls[1,1], expected_results[i])


        
    def test_works_with_branched_graphs(self):
        # S
        # |-----------
        # |    |     |
        # L1   K2    L2
        # |          |
        # E          K1
        n0 = Start()
        n1 = Lock("1")
        n2 = Key("2")
        n3 = Lock("2")
        n4 = Key("1")
        n5 = End()

        n0.add_child_s([n1, n2, n3])
        n1.add_child_s(n5)
        n2.add_child_s(n3)
        n2.add_lock_s(n3)
        n3.add_child_s(n4)
        n4.add_child_s(n1)
        n4.add_lock_s(n1)

        # Seed 2 incorrectly places lock1 in a different room
        np.random.seed(2)
        
        level = Level()
        w = Tiles.wall
        e = Tiles.empty
        layer = np.array([
            [w, w, w, w, w, w, w, w],
            [w, e, e, e, e, e, e, w],
            [w, e, e, e, e, e, e, w],
            [w, w, w, w, w, w, w, w],
            [w, e, e, w, e, e, e, w],
            [w, e, e, w, e, e, e, w],
            [w, e, e, w, e, e, e, w],
            [w, w, w, w, w, w, w, w]], dtype=object)

        solution_node_order = GNode.find_all_nodes(n0, method="topological-sort")
        is_solvable = False
        i = 0
        MAX_LOOP_COUNT = 50
        while not is_solvable:
            level.upper_layer = layer.copy()
            positions_map = MissionGenerator.generate_mission(level, level.upper_layer.shape, solution_node_order)
            is_solvable = Solver.does_level_follow_mission(level, solution_node_order[0], solution_node_order[-1], positions_map)
            i += 1
            self.assertTrue(i < MAX_LOOP_COUNT) # We're checking to make sure we haven't gotten stuck in a loop
        Log.print(level)
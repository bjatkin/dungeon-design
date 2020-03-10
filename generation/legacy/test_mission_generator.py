import unittest
from graph_structure.graph_node import Node, GNode, Start, End, Key, Lock
from generation.aesthetic_settings import AestheticSettings
from generation.mission_generator import MissionGenerator
from generation.generator import Generator
from dungeon_level.dungeon_tiles import Tiles
from dungeon_level.level import Level
from validation.solver import Solver
from log import Log
import time

import numpy as np

e = Tiles.empty
w = Tiles.wall
s = Tiles.player
f = Tiles.finish
l = Tiles.lock_red
k = Tiles.key_red
W = Tiles.water
F = Tiles.fire
fl= Tiles.flippers
Fb= Tiles.fire_boots

class TestMissionGenerator(unittest.TestCase):
    def test_get_rooms_components(self):
        layer = np.array([
            [e, e, w, w, e, w],
            [e, e, e, w, w, w],
            [w, w, e, w, e, e],
            [e, e, e, w, e, w],
            [w, w, w, e, e, w],
            [e, e, e, w, w, w]], dtype=object)
        
        labels, count = MissionGenerator.get_rooms_components(layer)
        expected_labels = np.array([
            [1, 1, 0, 0, 2, 0],
            [1, 1, 1, 0, 0, 0],
            [0, 0, 1, 0, 3, 3],
            [1, 1, 1, 0, 3, 0],
            [0, 0, 0, 3, 3, 0],
            [4, 4, 4, 0, 0, 0]])
        
        self.assertTrue(np.array_equal(labels, expected_labels))

    def test_get_rooms_components_with_other_tiles(self):
        layer = np.array([
            [e, e, w, w, s, w],
            [e, e, e, w, w, w],
            [w, w, l, w, e, e],
            [e, e, e, w, k, w],
            [w, w, w, e, e, w],
            [e, f, e, w, w, w]], dtype=object)

        labels, count = MissionGenerator.get_rooms_components(layer)
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

    def test_get_potential_lock_mask_edges(self):
        layer = np.array([
            [w, w, w, w, w],
            [w, e, e, e, w],
            [w, e, e, e, w],
            [w, e, e, e, w],
            [w, w, w, w, w]], dtype=object)

        expected_results = np.zeros([5,5])
        results = MissionGenerator.get_wall_corridor_mask(layer)
        self.assertTrue(np.array_equal(results, expected_results))

    def test_get_potential_lock_mask(self):
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
            single_walls = MissionGenerator.get_wall_corridor_mask(layer)
            self.assertEqual(single_walls[1,1], expected_results[i])


        
    def test_works_with_branched_graphs(self):
        # return
        # S
        # |-----------
        # |    |     |
        # L1   K2    L2
        # |          |
        # E          K1
        start = Start()
        key1 = Key("1")
        key2 = Key("2")
        lock1 = Lock("1")
        lock2 = Lock("2")
        end = End()

        start.add_child_s([lock1, key2, lock2])
        lock1.add_child_s(end)
        lock2.add_child_s(key1)
        key1.add_child_s(lock1)
        key2.add_child_s(lock2)
        key1.add_lock_s(lock1)
        key2.add_lock_s(lock2)

        np.random.seed(4)
        
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

        solution_node_order = Node.find_all_nodes(start, method="topological-sort")

        aesthetic_settings = AestheticSettings()
        was_successful = Generator.generate(
            level=level, 
            size=layer.shape, 
            aesthetic_settings=aesthetic_settings,
            max_retry_count=10, 
            pregenerated_level_layer=layer, 
            pregenerated_solution_node_order=solution_node_order)
        self.assertTrue(was_successful)

        Log.print(level)

    def test_get_space_connected_to_position(self):
        layer = np.array([
            [w, w, w, w, w, w],
            [w, s, W, f, F, e],
            [w, e, W, w,Fb, w],
            [w, w, w, w, w, e],
            [e, e, w, e, e, e],
            [e, W, e, w, w, w],
            [e, e, e, k, w, e],
            [e, e, e, e, l, e]], dtype=object)

        connected_space = MissionGenerator.get_space_connected_to_position(layer, np.array([1, 1]))
        expected_connected_space = np.array([
            [0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1],
            [0, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]])
        self.assertTrue(np.array_equal(connected_space, expected_connected_space))

        connected_space = MissionGenerator.get_space_connected_to_position(layer, np.array([5, 2]))
        expected_connected_space = np.array([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0],
            [1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1]])
        self.assertTrue(np.array_equal(connected_space, expected_connected_space))

    def test_get_walls_and_corridors_connected_to_space(self):
        layer = np.array([
            [w, w, w, w, w, w],
            [w, s, W, f, F, e],
            [w, e, W, w,Fb, w],
            [w, w, w, w, w, w],
            [e, e, w, e, e, e],
            [e, W, e, w, w, w],
            [e, e, e, k, w, e],
            [e, e, e, e, l, e]], dtype=object)

        connected_space = np.array([
            [0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1],
            [0, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]])

        expected_connected_walls_and_corridors = np.array([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]])
        connected_walls_and_corridors = MissionGenerator.get_walls_and_corridors_connected_to_space(layer, connected_space)
        self.assertTrue(np.array_equal(connected_walls_and_corridors, expected_connected_walls_and_corridors))

        connected_space = np.array([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0],
            [1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1]])

        expected_connected_walls_and_corridors = np.array([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]])
        connected_walls_and_corridors = MissionGenerator.get_walls_and_corridors_connected_to_space(layer, connected_space)
        self.assertTrue(np.array_equal(connected_walls_and_corridors, expected_connected_walls_and_corridors))



    def test_works_with_difficult_graph(self):
        return

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

        np.random.seed(12)
        
        level = Level()
        w = Tiles.wall
        e = Tiles.empty

        layer = np.array([
            [w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w],
            [w, e, e, w, e, e, w, e, e, w, e, e, w, e, e, w, e, e, w],
            [w, e, e, w, e, e, w, e, e, w, e, e, w, e, e, w, e, e, w],
            [w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w],
            [w, e, e, w, e, e, w, e, e, w, e, e, w, e, e, w, e, e, w],
            [w, e, e, w, e, e, w, e, e, w, e, e, w, e, e, w, e, e, w],
            [w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w],
            [w, e, e, w, e, e, w, e, e, w, e, e, w, e, e, w, e, e, w],
            [w, e, e, w, e, e, w, e, e, w, e, e, w, e, e, w, e, e, w],
            [w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w]], dtype=object)
            

        solution_node_order = Node.find_all_nodes(start, method="topological-sort")

        start_time = time.time()
        aesthetic_settings = AestheticSettings()
        aesthetic_settings.mission_aesthetic.single_lock_is_hazard_probability = 0
        aesthetic_settings.mission_aesthetic.hazard_spread_probability[Tiles.water] = 0
        aesthetic_settings.mission_aesthetic.hazard_spread_probability[Tiles.fire] = 0
        was_successful = Generator.generate(
            level=level, 
            size=layer.shape, 
            aesthetic_settings=aesthetic_settings,
            max_retry_count=10,
            pregenerated_level_layer=layer, 
            pregenerated_solution_node_order=solution_node_order)
        end_time = time.time()
        self.assertTrue(was_successful)

        Log.print(level)
        Log.print("Generated in {} seconds".format(end_time - start_time))
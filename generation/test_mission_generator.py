import unittest
from generation.mission_generator import MissionGenerator
from generation.generator import Generator
from generation.aesthetic_settings import AestheticSettings
import numpy as np
from dungeon_level.level import Level
from graph_structure.graph_node import Node, Start, Key, Lock, End, Collectable, CollectableBarrier, Room
from dungeon_level.dungeon_tiles import Tiles
from log import Log

e = Tiles.empty
w = Tiles.wall
s = Tiles.player
f = Tiles.finish
l = Tiles.lock_blue
k = Tiles.key_blue

class TestMissionGenerator(unittest.TestCase):
    def test_mission_generator_rooms(self):
        start = Start()
        key = Key()
        lock = Lock()
        room = Room()
        end = End()
        start.add_child_s([room, lock])
        room.add_child_s(key)
        key.add_lock_s(lock)
        lock.add_child_s(end)

        level = Level()
        w = Tiles.wall
        e = Tiles.empty
        layer = np.array([
            [w, w, w, w, w, w, w, w],
            [w, e, e, w, e, e, e, w],
            [w, e, e, w, e, e, e, w],
            [w, w, w, w, w, w, w, w],
            [w, e, e, w, e, e, e, w],
            [w, e, e, w, e, e, e, w],
            [w, e, e, w, e, e, e, w],
            [w, w, w, w, w, w, w, w]], dtype=object)

        solution_node_order = Node.find_all_nodes(start, method="topological-sort")

        aesthetic_settings = AestheticSettings()
        was_successful = Generator.generate(
            level_type=Level,
            size=layer.shape, 
            aesthetic_settings=aesthetic_settings,
            max_retry_count=10, 
            pregenerated_level_layer=layer, 
            pregenerated_solution_node_order=solution_node_order)
        self.assertTrue(was_successful)


    def test_mission_generator(self):    
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
        key1.add_lock_s(lock1)
        key2.add_lock_s(lock2)

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
            level_type=Level,
            size=layer.shape, 
            aesthetic_settings=aesthetic_settings,
            max_retry_count=10, 
            pregenerated_level_layer=layer, 
            pregenerated_solution_node_order=solution_node_order)
        self.assertTrue(was_successful)


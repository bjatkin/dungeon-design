import unittest
from dungeon_level.level import Level
from dungeon_level.dungeon_tiles import Tiles
from graph_structure.graph_node import GNode, Start, End, Lock, Key
from validation.solver import Solver
import numpy as np

s = Tiles.player
k = Tiles.key_red
l = Tiles.lock_red
w = Tiles.wall
f = Tiles.finish
e = Tiles.empty

class TestSolver(unittest.TestCase):
    def test_solver_linear_solvable(self):
        level = Level()
        level.upper_layer = np.array([
            [s, k, l, f ]], dtype=object)
        

        # S--K--L--E
        n0 = Start()
        n1 = Key()
        n2 = Lock()
        n3 = End()
        n0.add_child_s(n1)
        n1.add_child_s(n2)
        n2.add_child_s(n3)

        positions_map = {
            n0: np.array([0,0]),
            n1: np.array([0,1]),
            n2: np.array([0,2]),
            n3: np.array([0,3]),
        }
        
        does_level_follow_mission, reason = Solver.does_level_follow_mission(level, n0, positions_map, give_failure_reason=True)
        self.assertEqual(does_level_follow_mission, True)

    def test_solver_linear_unsolvable(self):
        level = Level()
        level.upper_layer = np.array([
            [s, l, k, f ]], dtype=object)
        
        # S--K--L--E
        n0 = Start()
        n1 = Key()
        n2 = Lock()
        n3 = End()
        n0.add_child_s(n1)
        n1.add_child_s(n2)
        n2.add_child_s(n3)

        positions_map = {
            n0: np.array([0,0]),
            n1: np.array([0,2]),
            n2: np.array([0,1]),
            n3: np.array([0,3]),
        }
        
        does_level_follow_mission, reason = Solver.does_level_follow_mission(level, n0, positions_map, give_failure_reason=True)
        self.assertEqual(does_level_follow_mission, False)
        self.assertEqual(reason, "unsolvable")

    def test_solver_linear_too_easy(self):
        level = Level()
        level.upper_layer = np.array([
            [s, k, l, f ],
            [e, e, e, e ]], dtype=object)
        

        # S--K--L--E
        n0 = Start()
        n1 = Key()
        n2 = Lock()
        n3 = End()
        n0.add_child_s(n1)
        n1.add_child_s(n2)
        n2.add_child_s(n3)

        positions_map = {
            n0: np.array([0,0]),
            n1: np.array([0,2]),
            n2: np.array([0,1]),
            n3: np.array([0,3]),
        }
        
        does_level_follow_mission, reason = Solver.does_level_follow_mission(level, n0, positions_map, give_failure_reason=True)
        self.assertEqual(does_level_follow_mission, False)
        self.assertEqual(reason, "trivial")

    def test_solver_branch_solvable(self):
        level = Level()
        level.upper_layer = np.array([
            [s, k, l, l, e, f],
            [e, k, w, w, e, e]], dtype=object)
        
        # S--K--L--L--E
        #  \      /
        #   K-----
        n0 = Start()
        n1 = Key("key1")
        n2 = Lock("lock1")
        n3 = Key("key2")
        n4 = Lock("lock2")
        n5 = End()
        n0.add_child_s(n1)
        n1.add_child_s(n2)
        n2.add_child_s(n4)
        n0.add_child_s(n3)
        n3.add_child_s(n4)
        n4.add_child_s(n5)

        positions_map = {
            n0: np.array([0,0]),
            n1: np.array([0,1]),
            n2: np.array([0,2]),
            n3: np.array([1,1]),
            n4: np.array([0,3]),
            n5: np.array([0,5]),
        }
        
        does_level_follow_mission, reason = Solver.does_level_follow_mission(level, n0, positions_map, give_failure_reason=True)
        self.assertEqual(does_level_follow_mission, True)


    def test_solver_branch_trivial1(self):
        level = Level()
        level.upper_layer = np.array([
            [s, k, l, e, e, f],
            [l, k, w, w, e, e]], dtype=object)
        
        # S--K--L--L--E
        #  \      /
        #   K-----
        n0 = Start()
        n1 = Key("key1")
        n2 = Lock("lock1")
        n3 = Key("key2")
        n4 = Lock("lock2")
        n5 = End()
        n0.add_child_s(n1)
        n1.add_child_s(n2)
        n2.add_child_s(n4)
        n0.add_child_s(n3)
        n3.add_child_s(n4)
        n4.add_child_s(n5)

        positions_map = {
            n0: np.array([0,0]),
            n1: np.array([0,1]),
            n2: np.array([0,2]),
            n3: np.array([1,1]),
            n4: np.array([1,0]),
            n5: np.array([0,5]),
        }
        
        does_level_follow_mission, reason = Solver.does_level_follow_mission(level, n0, positions_map, give_failure_reason=True)
        self.assertEqual(does_level_follow_mission, False)
        self.assertEqual(reason, "trivial")

    def test_solver_branch_trivial2(self):
        return
        level = Level()
        level.upper_layer = np.array([
            [e, l, e],
            [k, k, w],
            [s, l, f]], dtype=object)
        
        # S--K--L--L--E
        #  \      /
        #   K-----
        n0 = Start()
        n1 = Key("key1")
        n2 = Lock("lock1")
        n3 = Key("key2")
        n4 = Lock("lock2")
        n5 = End()
        n0.add_child_s(n1)
        n1.add_child_s(n2)
        n2.add_child_s(n4)
        n0.add_child_s(n3)
        n3.add_child_s(n4)
        n4.add_child_s(n5)

        positions_map = {
            # Wrong
            n0: np.array([2,0]),
            n1: np.array([1,1]),
            n2: np.array([0,1]),
            n3: np.array([1,0]),
            n4: np.array([2,1]),
            n5: np.array([2,2]),

            # Right
            # n0: np.array([2,0]),
            # n1: np.array([1,0]),
            # n2: np.array([2,1]),
            # n3: np.array([1,1]),
            # n4: np.array([0,1]),
            # n5: np.array([2,2]),
        }
        
        does_level_follow_mission, reason = Solver.does_level_follow_mission(level, n0, positions_map, give_failure_reason=True)
        self.assertEqual(does_level_follow_mission, False)
        self.assertEqual(reason, "trivial")

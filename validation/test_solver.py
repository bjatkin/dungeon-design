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
        start = Start()
        key = Key()
        lock = Lock()
        end = End()
        start.add_child_s(key)
        key.add_child_s(lock)
        lock.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key:    np.array([0,1]),
            lock:   np.array([0,2]),
            end:    np.array([0,3]),
        }

        does_level_follow_mission, failure_reason = Solver.does_level_follow_mission(level, start, end, positions_map, give_failure_reason=True)
        self.assertEqual(does_level_follow_mission, True)
        
        # solution = Solver.find_level_solution_from_mission(level, start, end, positions_map)
        # does_solution_follow_mission = Solver.does_solution_path_follow_mission(positions_map, solution)
        # self.assertEqual(does_solution_follow_mission, True)


    def test_solver_linear_unsolvable(self):
        level = Level()
        level.upper_layer = np.array([
            [s, l, k, f ]], dtype=object)
        
        # S--K--L--E
        start = Start()
        key = Key()
        lock = Lock()
        end = End()
        start.add_child_s(key)
        key.add_child_s(lock)
        lock.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key:    np.array([0,2]),
            lock:   np.array([0,1]),
            end:    np.array([0,3]),
        }

        does_level_follow_mission, failure_reason = Solver.does_level_follow_mission(level, start, end, positions_map, give_failure_reason=True)
        self.assertEqual(does_level_follow_mission, False)
        
        # solution = Solver.find_level_solution_from_mission(level, start, end, positions_map)
        # does_solution_follow_mission = Solver.does_solution_path_follow_mission(positions_map, solution)
        # self.assertEqual(does_solution_follow_mission, False)

    def test_solver_linear_unsolvable2(self):
        level = Level()
        level.upper_layer = np.array([
            [s, k, l, l, f ]], dtype=object)
        
        # S--K--L--E
        start = Start()
        key = Key()
        lock1 = Lock("lock1")
        lock2 = Lock("lock2")
        end = End()
        start.add_child_s(key)
        key.add_child_s(lock1)
        lock1.add_child_s(lock2)
        lock2.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key:    np.array([0,1]),
            lock1:  np.array([0,2]),
            lock2:  np.array([0,3]),
            end:    np.array([0,4]),
        }

        does_level_follow_mission, failure_reason = Solver.does_level_follow_mission(level, start, end, positions_map, give_failure_reason=True)
        self.assertEqual(does_level_follow_mission, False)
        
        # solution = Solver.find_level_solution_from_mission(level, start, end, positions_map)
        # does_solution_follow_mission = Solver.does_solution_path_follow_mission(positions_map, solution)
        # self.assertEqual(does_solution_follow_mission, False)

    def test_solver_linear_trivial(self):
        level = Level()
        level.upper_layer = np.array([
            [s, k, l, f ],
            [e, e, e, e ]], dtype=object)
        

        # S--K--L--E
        start = Start()
        key = Key()
        lock = Lock()
        end = End()
        start.add_child_s(key)
        key.add_child_s(lock)
        lock.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key:    np.array([0,1]),
            lock:   np.array([0,2]),
            end:    np.array([0,3]),
        }

        does_level_follow_mission, failure_reason = Solver.does_level_follow_mission(level, start, end, positions_map, give_failure_reason=True)
        self.assertEqual(does_level_follow_mission, False)
        
        # solution = Solver.find_level_solution_from_mission(level, start, end, positions_map)
        # does_solution_follow_mission = Solver.does_solution_path_follow_mission(positions_map, solution)
        # self.assertEqual(does_solution_follow_mission, False)


    def test_solver_branch_solvable(self):
        level = Level()
        level.upper_layer = np.array([
            [s, k, l, l, e, f],
            [e, k, w, w, e, e]], dtype=object)
        
        # S--K1--L1--L2--E
        #  \         /
        #   K2-------
        start = Start()
        key1 = Key("key1")
        lock1 = Lock("lock1")
        key2 = Key("key2")
        lock2 = Lock("lock2")
        end = End()
        start.add_child_s(key1)
        key1.add_child_s(lock1)
        lock1.add_child_s(lock2)
        start.add_child_s(key2)
        key2.add_child_s(lock2)
        lock2.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key1:   np.array([0,1]),
            lock1:  np.array([0,2]),
            key2:   np.array([1,1]),
            lock2:  np.array([0,3]),
            end:    np.array([0,5]),
        }

        does_level_follow_mission, failure_reason = Solver.does_level_follow_mission(level, start, end, positions_map, give_failure_reason=True)
        self.assertEqual(does_level_follow_mission, True)
        
        # solution = Solver.find_level_solution_from_mission(level, start, end, positions_map)
        # does_solution_follow_mission = Solver.does_solution_path_follow_mission(positions_map, solution)
        # self.assertEqual(does_solution_follow_mission, True)


    def test_solver_branch_trivial1(self):
        level = Level()
        level.upper_layer = np.array([
            [s, k, l, e, e, f],
            [l, k, w, w, e, e]], dtype=object)
        
        # S--K--L--L--E
        #  \      /
        #   K-----
        start = Start()
        key1 = Key("key1")
        lock1 = Lock("lock1")
        key2 = Key("key2")
        lock2 = Lock("lock2")
        end = End()
        start.add_child_s(key1)
        key1.add_child_s(lock1)
        lock1.add_child_s(lock2)
        start.add_child_s(key2)
        key2.add_child_s(lock2)
        lock2.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key1:   np.array([0,1]),
            lock1:  np.array([0,2]),
            key2:   np.array([1,1]),
            lock2:  np.array([1,0]),
            end:    np.array([0,5]),
        }
        
        does_level_follow_mission, reason = Solver.does_level_follow_mission(level, start, end, positions_map, give_failure_reason=True)
        self.assertEqual(does_level_follow_mission, False)
        self.assertEqual(reason, "trivial")

    def test_solver_branch_trivial2(self):
        level = Level()
        level.upper_layer = np.array([
            [e, l, e],
            [k, k, w],
            [s, l, f]], dtype=object)
        
        # S--K--L--L--E
        #  \      /
        #   K-----
        start = Start()
        key1 = Key("key1")
        lock1 = Lock("lock1")
        key2 = Key("key2")
        lock2 = Lock("lock2")
        end = End()
        start.add_child_s(key1)
        key1.add_child_s(lock1)
        lock1.add_child_s(lock2)
        start.add_child_s(key2)
        key2.add_child_s(lock2)
        lock2.add_child_s(end)

        positions_map = {
            # Wrong
            start:  np.array([2,0]),
            key1:   np.array([1,1]),
            lock1:  np.array([0,1]),
            key2:   np.array([1,0]),
            lock2:  np.array([2,1]),
            end:    np.array([2,2]),

            # Right
            # start:  np.array([2,0]),
            # key1:   np.array([1,0]),
            # lock1:  np.array([2,1]),
            # key2:   np.array([1,1]),
            # lock2:  np.array([0,1]),
            # end:    np.array([2,2]),
        }
        
        does_level_follow_mission, reason = Solver.does_level_follow_mission(level, start, end, positions_map, give_failure_reason=True)
        self.assertEqual(does_level_follow_mission, False)
        self.assertEqual(reason, "trivial")

    def test_solver_double_parent(self):
        level = Level()
        level.upper_layer = np.array([
            [s, l, e, l, f],
            [k, w, k, w, e]], dtype=object)

        # S--L--L--E
        #  \ |\ |
        #   \| \|
        #    K  K
        start = Start()
        key1 = Key("key1")
        lock1 = Lock("lock1")
        key2 = Key("key2")
        lock2 = Lock("lock2")
        end = End()
        start.add_child_s(lock1)
        start.add_child_s(key1)
        key1.add_child_s(lock1)
        lock1.add_child_s(lock2)
        lock1.add_child_s(key2)
        key2.add_child_s(lock2)
        lock2.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key1:   np.array([1,0]),
            lock1:  np.array([0,1]),
            key2:   np.array([1,2]),
            lock2:  np.array([0,3]),
            end:    np.array([0,4])
            }

        does_level_follow_mission, reason = Solver.does_level_follow_mission(level, start, end, positions_map, give_failure_reason=True)
        self.assertEqual(does_level_follow_mission, True)
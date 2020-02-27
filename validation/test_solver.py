import unittest
from dungeon_level.level import Level
from dungeon_level.dungeon_tiles import Tiles
from graph_structure.graph_node import GNode, Start, End, Lock, Key
from validation.solver import Solver
import numpy as np

s = Tiles.player
kB = Tiles.key_blue
lB = Tiles.lock_blue
kR = Tiles.key_red
lR = Tiles.lock_red
kG = Tiles.key_green
lG = Tiles.lock_green
kY = Tiles.key_yellow
lY = Tiles.lock_yellow
w = Tiles.wall
f = Tiles.finish
e = Tiles.empty

class TestSolver(unittest.TestCase):
    def test_solver_linear_solvable(self):
        level = Level()
        level.upper_layer = np.array([
            [s,kR,lR, f ]], dtype=object)
        

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



    def test_solver_linear_solvable_multicolored_keys(self):
        level = Level()
        level.upper_layer = np.array([
            [kY,lG,kB,lR, s,kR,lB,kG,lY, f]], dtype=object)
        

        # S--K--L--K--L--K--L--K--L--E
        start = Start()
        key1 = Key("red")
        lock1 = Lock("red")
        key2 = Key("blue")
        lock2 = Lock("blue")
        key3 = Key("green")
        lock3 = Lock("green")
        key4 = Key("yellow")
        lock4 = Lock("yellow")
        end = End()
        start.add_child_s(key1)
        key1.add_child_s(lock1)
        lock1.add_child_s(key2)
        key2.add_child_s(lock2)
        lock2.add_child_s(key3)
        key3.add_child_s(lock3)
        lock3.add_child_s(key4)
        key4.add_child_s(lock4)
        lock4.add_child_s(end)

        positions_map = {
            start:  np.array([0,4]),
            key1:   np.array([0,5]),
            lock1:  np.array([0,3]),
            key2:   np.array([0,2]),
            lock2:  np.array([0,6]),
            key3:   np.array([0,7]),
            lock3:  np.array([0,1]),
            key4:   np.array([0,0]),
            lock4:  np.array([0,8]),
            end:    np.array([0,9]),
        }

        does_level_follow_mission, failure_reason = Solver.does_level_follow_mission(level, start, end, positions_map, give_failure_reason=True)
        self.assertEqual(does_level_follow_mission, True)


    def test_solver_linear_unsolvable(self):
        level = Level()
        level.upper_layer = np.array([
            [s,lR,kR, f ]], dtype=object)
        
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
        

    def test_solver_linear_unsolvable2(self):
        level = Level()
        level.upper_layer = np.array([
            [s,kR,lR,lR, f ]], dtype=object)
        
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
        

    def test_solver_linear_trivial(self):
        level = Level()
        level.upper_layer = np.array([
            [s,kR,lR, f ],
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
        

    def test_solver_branch_solvable(self):
        level = Level()
        level.upper_layer = np.array([
            [s,kR,lR,lR, e, f],
            [e,kR, w, w, e, e]], dtype=object)
        
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
        

    def test_solver_branch_trivial1(self):
        level = Level()
        level.upper_layer = np.array([
            [ s,kR,lR, e, e, f],
            [lR,kR, w, w, e, e]], dtype=object)
        
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
            [ e,lR, e],
            [kR,kR, w],
            [ s,lR, f]], dtype=object)
        
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
            [ s,lR, e,lR, f],
            [kR, w,kR, w, e]], dtype=object)

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
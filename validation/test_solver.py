import unittest
from dungeon_level.level import Level
from dungeon_level.dungeon_tiles import Tiles
from graph_structure.graph_node import Node, Start, End, Lock, Key, Collectable, CollectableBarrier, SokobanKey, SokobanLock
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
F = Tiles.fire
Fb= Tiles.fire_boots
W = Tiles.water
fl= Tiles.flippers
c = Tiles.collectable
B = Tiles.required_collectable_barrier
b = Tiles.sokoban_block
g = Tiles.sokoban_goal

lM = [(0,-1)]
rM = [(0,1)]
uM = [(-1,0)]
dM = [(1,0)]

class TestSolver(unittest.TestCase):
    def assert_moves_equal(self, moves, expected_moves):
        self.assertEqual(len(moves), len(expected_moves))
        zipped_moves = zip(moves, expected_moves)
        for move, expected_move in zipped_moves:
            node, move = move
            expected_node, expected_move = expected_move
            self.assertEqual(node, expected_node)
            self.assertEqual(np.array(move).tolist(), np.array(expected_move).tolist())

    def test_solver_linear_solvable(self):
        level = Level()
        level.upper_layer = np.array([
            [s,kR,lR, f ]], dtype=object)
        

        # S--K--L--E
        start = Start()
        key = Key()
        lock = Lock()
        end = End()
        start.add_child_s([key, lock])
        key.add_lock_s(lock)
        lock.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key:    np.array([0,1]),
            lock:   np.array([0,2]),
            end:    np.array([0,3]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, True)

        expected_moves = [
            (key, rM),
            (lock, rM),
            (end, rM)]
        self.assert_moves_equal(moves, expected_moves)



    def test_solver_linear_solvable_multicolored_keys(self):
        level = Level()
        level.upper_layer = np.array([
            [kY,lG,kB,lR, s,kR,lB,kG,lY, f]], dtype=object)
        

        # S--K--L--K--L--K--L--K--L--E
        start = Start()
        key_red = Key("red")
        lock_red = Lock("red")
        key_blue = Key("blue")
        lock_blue = Lock("blue")
        key_green = Key("green")
        lock_green = Lock("green")
        key_yellow = Key("yellow")
        lock_yellow = Lock("yellow")
        end = End()

        start.add_child_s([lock_red, key_red, lock_blue])
        lock_red.add_child_s([lock_green, key_blue])
        lock_green.add_child_s(key_yellow)
        lock_blue.add_child_s([lock_yellow, key_green])
        lock_yellow.add_child_s(end)
        key_red.add_child_s(lock_red)
        key_red.add_lock_s(lock_red)
        key_blue.add_child_s(lock_blue)
        key_blue.add_lock_s(lock_blue)
        key_green.add_child_s(lock_green)
        key_green.add_lock_s(lock_green)
        key_yellow.add_child_s(lock_yellow)
        key_yellow.add_lock_s(lock_yellow)
        


        positions_map = {
            start:        np.array([0,4]),
            key_red:      np.array([0,5]),
            lock_red:     np.array([0,3]),
            key_blue:     np.array([0,2]),
            lock_blue:    np.array([0,6]),
            key_green:    np.array([0,7]),
            lock_green:   np.array([0,1]),
            key_yellow:   np.array([0,0]),
            lock_yellow:  np.array([0,8]),
            end:          np.array([0,9]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, True)

        expected_moves = [
            (key_red, rM),
            (lock_red, 2*lM),
            (key_blue, lM),
            (lock_blue, 4*rM),
            (key_green, rM),
            (lock_green, 6*lM),
            (key_yellow, lM),
            (lock_yellow, 8*rM),
            (end, rM)]
        self.assert_moves_equal(moves, expected_moves)


    def test_solver_linear_unsolvable(self):
        level = Level()
        level.upper_layer = np.array([
            [s,lR,kR, f ]], dtype=object)
        
        # S--K--L--E
        start = Start()
        key = Key("key")
        lock = Lock("lock")
        end = End()
        start.add_child_s(key)
        key.add_lock_s(lock)
        lock.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key:    np.array([0,2]),
            lock:   np.array([0,1]),
            end:    np.array([0,3]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
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
        key.add_lock_s(lock1)
        lock1.add_child_s(lock2)
        lock2.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key:    np.array([0,1]),
            lock1:  np.array([0,2]),
            lock2:  np.array([0,3]),
            end:    np.array([0,4]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, False)
        

    def test_solver_linear_trivial(self):
        level = Level()
        level.upper_layer = np.array([
            [s,kR,lR, f ],
            [e, e, e, e ]], dtype=object)
        

        # S--K--L--E
        start = Start()
        key = Key("key")
        lock = Lock("lock")
        end = End()
        start.add_child_s(key)
        key.add_lock_s(lock)
        lock.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key:    np.array([0,1]),
            lock:   np.array([0,2]),
            end:    np.array([0,3]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, False)
        

    def test_solver_branch_solvable(self):
        level = Level()
        level.upper_layer = np.array([
            [s,kR,lR,lB, e, f],
            [e,kB, w, w, e, e]], dtype=object)
        
        # S----------
        # |    |    |
        # lR   kR   kB
        # |
        # lB
        # |
        # E
        start = Start()
        key1 = Key("key1")
        lock1 = Lock("lock1")
        key2 = Key("key2")
        lock2 = Lock("lock2")
        end = End()
        start.add_child_s([lock1, key1, key2])
        lock1.add_child_s(lock2)
        lock2.add_child_s(end)
        key1.add_lock_s(lock1)
        key2.add_lock_s(lock2)

        positions_map = {
            start:  np.array([0,0]),
            key1:   np.array([0,1]),
            lock1:  np.array([0,2]),
            key2:   np.array([1,1]),
            lock2:  np.array([0,3]),
            end:    np.array([0,5]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, True)



        

    def test_solver_branch_trivial1(self):
        level = Level()
        level.upper_layer = np.array([
            [ s,kR,lR, e, e, f],
            [lB,kB, w, w, e, e]], dtype=object)
        
        # S--K--L--L--E
        #  \      /
        #   K-----
        start = Start()
        key1 = Key("key1")
        lock1 = Lock("lock1")
        key2 = Key("key2")
        lock2 = Lock("lock2")
        end = End()
        start.add_child_s([key1, key2])
        key1.add_child_s(lock1)
        key1.add_lock_s(lock1)
        lock1.add_child_s(lock2)
        key2.add_lock_s(lock2)
        lock2.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key1:   np.array([0,1]),
            lock1:  np.array([0,2]),
            key2:   np.array([1,1]),
            lock2:  np.array([1,0]),
            end:    np.array([0,5]),
        }
        
        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, False)


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
        start.add_child_s([key1, key2])
        key1.add_child_s(lock1)
        key1.add_lock_s(lock1)
        lock1.add_child_s(lock2)
        key2.add_lock_s(lock2)
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
        
        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, False)


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
        start.add_child_s([key1, lock1])
        key1.add_lock_s(lock1)
        lock1.add_child_s([key2, lock2])
        key2.add_lock_s(lock2)
        lock2.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key1:   np.array([1,0]),
            lock1:  np.array([0,1]),
            key2:   np.array([1,2]),
            lock2:  np.array([0,3]),
            end:    np.array([0,4])
            }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, True)

    def test_node_seen_too_soon_correct_layout(self):
        level = Level()
        level.upper_layer = np.array([
            [ s, e,lR,kB],
            [kR, e, w, w],
            [ e, e,lB, f]], dtype=object)
        
        # S---------
        # |   |    |
        # L1  L2   K1
        # |   |
        # K2  E
        start = Start()
        key1 = Key("key1")
        lock1 = Lock("lock1")
        key2 = Key("key2")
        lock2 = Lock("lock2")
        end = End()
        start.add_child_s([lock1, lock2, key1])
        key1.add_lock_s(lock1)
        key2.add_lock_s(lock2)
        lock1.add_child_s(key2)
        lock2.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key1:   np.array([1,0]),
            lock1:  np.array([0,2]),
            key2:   np.array([0,3]),
            lock2:  np.array([2,2]),
            end:    np.array([2,3]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, True)

    def test_node_seen_too_soon_incorrect_layout(self):
        level = Level()
        level.upper_layer = np.array([
            [ s,lR, e,lB, f],
            [kR, w,kB, w, w]], dtype=object)

        # S---------
        # |   |    |
        # L1  L2   K1
        # |   |
        # K2  E
        start = Start()
        key1 = Key("key1")
        lock1 = Lock("lock1")
        key2 = Key("key2")
        lock2 = Lock("lock2")
        end = End()
        start.add_child_s([lock1, lock2, key1])
        key1.add_lock_s(lock1)
        key2.add_lock_s(lock2)
        lock1.add_child_s(key2)
        lock2.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key1:   np.array([1,0]),
            lock1:  np.array([0,1]),
            key2:   np.array([1,2]),
            lock2:  np.array([0,3]),
            end:    np.array([0,4]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, False)


    def test_node_seen_too_soon_correct_layout2(self):
        level = Level()
        level.upper_layer = np.array([
            [ s,lR, e,lB, f],
            [kR, w,kB, w, w]], dtype=object)
        
        # S----
        # |   |
        # L1  K1
        # |----
        # |   |
        # L2  K2
        # |
        # F
        start = Start()
        key1 = Key("key1")
        lock1 = Lock("lock1")
        key2 = Key("key2")
        lock2 = Lock("lock2")
        end = End()
        start.add_child_s([key1, lock1])
        key1.add_lock_s(lock1)
        key2.add_lock_s(lock2)
        lock1.add_child_s([key2, lock2])
        lock2.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key1:   np.array([1,0]),
            lock1:  np.array([0,1]),
            key2:   np.array([1,2]),
            lock2:  np.array([0,3]),
            end:    np.array([0,4]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, True)


    def test_node_seen_too_soon_incorrect_layout2(self):
        level = Level()
        level.upper_layer = np.array([
            [ s, e,lR,kB],
            [kR, e, w, w],
            [ e, e,lB, f]], dtype=object)
        
        # S----
        # |   |
        # L1  K1
        # |----
        # |   |
        # L2  K2
        # |
        # F
        start = Start()
        key1 = Key("key1")
        lock1 = Lock("lock1")
        key2 = Key("key2")
        lock2 = Lock("lock2")
        end = End()
        start.add_child_s([key1, lock1])
        key1.add_lock_s(lock1)
        key2.add_lock_s(lock2)
        lock1.add_child_s([key2, lock2])
        lock2.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key1:   np.array([1,0]),
            lock1:  np.array([0,2]),
            key2:   np.array([0,3]),
            lock2:  np.array([2,2]),
            end:    np.array([2,3]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, False)


    def test_degenerate_loop_layout(self):
        level = Level()
        level.upper_layer = np.array([
            [w, w, w, w, w, w, w, w, w],
            [w, s, w, e, e, e, e, f, w],
            [w,kR, w, w, w, w,lG, w, w],
            [w,kG,lR, e, e, e, e, e, w],
            [w, e, w, e, e, e, e,kR, w],
            [w, e, w, w,lR, w, e, w, w],
            [w, e, w, e, e, e, e, e, w],
            [w, w, w, w, w, w, w, w, w]], dtype=object)

        start = Start()
        key0 = Key("key0")
        lock0 = Lock("lock0")
        key1 = Key("key1")
        lock1 = Lock("lock1")
        key2 = Key("key2")
        lock2 = Lock("lock2")
        end = End()
        start.add_child_s([lock0, key0, key2])
        lock0.add_child_s([lock1, key1])
        lock1.add_child_s(lock2)
        lock2.add_child_s(end)
        key0.add_lock_s(lock0)
        key1.add_lock_s(lock1)
        key2.add_lock_s(lock2)

        positions_map = {
            start:  np.array([1,1]),
            key0:   np.array([2,1]),
            key2:   np.array([3,1]),
            lock0:  np.array([3,2]),
            key1:   np.array([4,7]),
            lock1:  np.array([5,4]),
            lock2:  np.array([2,6]),
            end:    np.array([1,7]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, False)


    def test_wrong_key_color(self):
        level = Level()
        level.upper_layer = np.array([
            [ s, e,lR,kR],
            [kR, e, w, w],
            [ e, e,lR, f]], dtype=object)

        start = Start()
        key1 = Key("key1")
        lock1 = Lock("lock1")
        key2 = Key("key2")
        lock2 = Lock("lock2")
        end = End()
        start.add_child_s([key1, lock1, lock2])
        lock1.add_child_s(key2)
        lock2.add_child_s(end)
        key1.add_lock_s(lock1)
        key2.add_lock_s(lock2)

        positions_map = {
            start:  np.array([0,0]),
            key1:   np.array([1,0]),
            lock1:  np.array([0,2]),
            key2:   np.array([0,3]),
            lock2:  np.array([2,2]),
            end:    np.array([2,3]),
        }
        
        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, False)


    def test_two_keys_soon(self):
        level = Level()
        level.upper_layer = np.array([
            [s,kR,lR,lR, e, f],
            [e,kR, w, w, e, e]], dtype=object)
        
        # S----------
        # |    |    |
        # lR   kR   kB
        # |
        # lB
        # |
        # E
        start = Start()
        key1 = Key("key1")
        lock1 = Lock("lock1")
        key2 = Key("key2")
        lock2 = Lock("lock2")
        end = End()
        start.add_child_s([lock1, key1, key2])
        lock1.add_child_s(lock2)
        lock2.add_child_s(end)
        key1.add_lock_s(lock1)
        key2.add_lock_s(lock2)

        positions_map = {
            start:  np.array([0,0]),
            key1:   np.array([1,1]),
            lock1:  np.array([0,2]),
            key2:   np.array([0,1]),
            lock2:  np.array([0,3]),
            end:    np.array([0,5]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, True)


    def test_two_keys_soon_unneeded(self):
        level = Level()
        level.upper_layer = np.array([
            [s,kR,lR, e, e, f],
            [e,kR,lR, e, e, e]], dtype=object)
        
        # S----------
        # |    |    |
        # lR   kR   kB
        # |
        # lB
        # |
        # E
        start = Start()
        key1 = Key("key1")
        lock1 = Lock("lock1")
        key2 = Key("key2")
        lock2 = Lock("lock2")
        end = End()
        start.add_child_s([lock1, key1, key2])
        lock1.add_child_s(lock2)
        lock2.add_child_s(end)
        key1.add_lock_s(lock1)
        key2.add_lock_s(lock2)

        positions_map = {
            start:  np.array([0,0]),
            key1:   np.array([1,1]),
            lock1:  np.array([0,2]),
            key2:   np.array([0,1]),
            lock2:  np.array([0,3]),
            end:    np.array([0,5]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, False)


    def test_solver_hazard_solvable(self):
        level = Level()
        level.upper_layer = np.array([
            [s, e, fl, W, W, W, e, Fb, e, F, F, e, F, F, e, f]], dtype=object)
        

        # S--K--L--E
        start = Start()
        key1 = Key("flippers")
        lock1 = Lock("water")
        key2 = Key("fireboots")
        lock2 = Lock("fire1")
        lock3 = Lock("fire2")
        end = End()
        start.add_child_s([key1, lock1])
        key1.add_lock_s(lock1)
        lock1.add_child_s([key2, lock2])
        key2.add_lock_s([lock2, lock3])
        lock2.add_child_s(lock3)
        lock3.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key1:   np.array([0,2]),
            lock1:  np.array([0,4]),
            key2:   np.array([0,7]),
            lock2:  np.array([0,10]),
            lock3:  np.array([0,13]),
            end:    np.array([0,15]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, True)


    def test_solver_hazard_unsolvable(self):
        level = Level()
        level.upper_layer = np.array([
            [s, e, Fb, W, W, W, e, fl, e, F, F, e, F, F, e, f]], dtype=object)
        

        # S--K--L--E
        start = Start()
        key1 = Key("flippers")
        lock1 = Lock("water")
        key2 = Key("fireboots")
        lock2 = Lock("fire1")
        lock3 = Lock("fire2")
        end = End()
        start.add_child_s([key1, lock1])
        key1.add_lock_s(lock1)
        lock1.add_child_s([key2, lock2])
        key2.add_lock_s([lock2, lock3])
        lock2.add_child_s(lock3)
        lock3.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key1:   np.array([0,7]),
            lock1:  np.array([0,4]),
            key2:   np.array([0,2]),
            lock2:  np.array([0,10]),
            lock3:  np.array([0,13]),
            end:    np.array([0,15]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, False)


    def test_solver_hazard_too_soon(self):
        level = Level()
        level.upper_layer = np.array([
            [ s, e, W, e,fl],
            [ e,fl, w, w, w],
            [ e, e, W, e, f]], dtype=object)
        

        # S--K--L--E
        start = Start()
        flippers1 = Key("flippers 1")
        water1 = Lock("water 1")
        flippers2 = Key("flippers 2")
        water2 = Lock("water 2")
        end = End()

        start.add_child_s([flippers1, water1, water2])
        flippers1.add_lock_s(water1)
        water1.add_child_s(flippers2)
        flippers2.add_lock_s(water2)
        water2.add_child_s(end)

            # [ s, e, W, e,fl],
            # [ e,fl, w, w, w],
            # [ e, e, W, e, f]], dtype=object)

        positions_map = {
            start:      np.array([0,0]),
            flippers1:  np.array([1,1]),
            water1:     np.array([0,2]),
            flippers2:  np.array([0,4]),
            water2:     np.array([2,2]),
            end:        np.array([2,4]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, False)


    def test_solver_difficult(self):
        level = Level()
        level.upper_layer = np.array([
            [ f, e, e, w, e, W, e, w],
            [ e, w,lG, w, e, w,Fb, w],
            [ e, w, F, w, W, w, e, w],
            [ e, w, s, w, e, w, F, w],
            [ e, w,kR, w,fl, w, e, w],
            [ e, w, e,lR, e, w,kG, w]], dtype=object)

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

            # [ f, e, e, w, e, W, e, w],
            # [ e, w,lG, w, e, w,Fb, w],
            # [ e, w, F, w, W, w, e, w],
            # [ e, w, s, w, e, w, F, w],
            # [ e, w,kR, w,fl, w, e, w],
            # [ e, w, e,lR, e, w,kG, w]], dtype=object)
        positions_map = {
            start:      np.array([3,2]),
            key_red:    np.array([4,2]),
            lock_red:   np.array([5,3]),
            flippers:   np.array([4,4]),
            water1:     np.array([2,4]),
            water2:     np.array([0,5]),
            key_green:  np.array([5,6]),
            lock_green: np.array([1,2]),
            fire_boots: np.array([1,6]),
            fire1:      np.array([3,6]),
            fire2:      np.array([2,2]),
            end:        np.array([0,0])
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, True)


    def test_solver_collectables(self):
        level = Level()
        level.upper_layer = np.array([
            [s, e, B, f ],
            [c, c, w, e ]], dtype=object)
        level.required_collectable_count = 2

        start = Start()
        c0 = Collectable("c0")
        c1 = Collectable("c1")
        barrier = CollectableBarrier("B", collectables=[c0, c1])
        end = End()

        start.add_child_s([c0, c1, barrier])
        barrier.add_child_s(end)

        positions_map = {
            start:   np.array([0,0]),
            c0:      np.array([1,0]),
            c1:      np.array([1,1]),
            barrier: np.array([0,2]),
            end:     np.array([0,3]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, True)

        if moves[0][0] == c1:
            expected_moves = [
                (c1, dM + rM),
                (c0, lM),
                (barrier, rM + uM + rM),
                (end, rM)]
        else:
            expected_moves = [
                (c0, dM),
                (c1, rM),
                (barrier, uM + rM),
                (end, rM)]
        self.assert_moves_equal(moves, expected_moves)


    def test_solver_collectables_too_many_required_collectables(self):
        level = Level()
        level.upper_layer = np.array([
            [s, e, B, f ],
            [c, c, w, e ]], dtype=object)
        level.required_collectable_count = 3
        

        start = Start()
        c0 = Collectable("c0")
        c1 = Collectable("c1")
        barrier = CollectableBarrier("B", collectables=[c0, c1])
        end = End()

        start.add_child_s([c0, c1, barrier])
        barrier.add_child_s(end)

        positions_map = {
            start:   np.array([0,0]),
            c0:      np.array([1,0]),
            c1:      np.array([1,1]),
            barrier: np.array([0,2]),
            end:     np.array([0,3]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, False)


    def test_solver_collectables_unreachable_collectable(self):
        level = Level()
        level.upper_layer = np.array([
            [s, e, B, f ],
            [c, e, w, c ]], dtype=object)
        level.required_collectable_count = 2
        

        start = Start()
        c0 = Collectable("c0")
        c1 = Collectable("c1")
        barrier = CollectableBarrier("B", collectables=[c0, c1])
        end = End()

        start.add_child_s([c0, barrier])
        barrier.add_child_s([c1, end])

        positions_map = {
            start:   np.array([0,0]),
            c0:      np.array([1,0]),
            c1:      np.array([1,3]),
            barrier: np.array([0,2]),
            end:     np.array([0,3]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, False)


    def test_sokoban_solvable(self):
        level = Level()
        level.upper_layer = np.array([
            [s,kR, b, e, e, e, g,lR, f ],
            [e, e, e, e, e, e, w, w, e ]], dtype=object)
        

        start = Start()
        key = Key("key")
        block = SokobanKey("block")
        water = SokobanLock("water")
        lock = Lock("lock")
        end = End()
        start.add_child_s([key, block, water])
        block.add_lock_s([water])
        key.add_lock_s(lock)
        water.add_child_s(lock)
        lock.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key:    np.array([0,1]),
            block:  np.array([0,2]),
            water:  np.array([0,6]),
            lock:   np.array([0,7]),
            end:    np.array([0,8]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, True)

        if moves[0][0] == water:
            expected_moves = [
                (water, 5*rM),
                (key, 4*lM),
                (lock, 6*rM),
                (end, rM)]
        else:
            expected_moves = [
                (key, rM),
                (water, 4*rM),
                (lock, 2*rM),
                (end, rM)]
        self.assert_moves_equal(moves, expected_moves)


    def test_sokoban_solvable_lock_in_middle(self):
        level = Level()
        level.upper_layer = np.array([
            [s,kR, b, e,lR, e, g, e, f ],
            [e, e, e, e, w, e, w, w, e ]], dtype=object)
        

        start = Start()
        key = Key("key")
        block = SokobanKey("block")
        water = SokobanLock("water")
        lock = Lock("lock")
        end = End()
        start.add_child_s([key, block, lock])
        block.add_lock_s([water])
        key.add_lock_s(lock)
        lock.add_child_s(water)
        water.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key:    np.array([0,1]),
            block:  np.array([0,2]),
            water:  np.array([0,6]),
            lock:   np.array([0,4]),
            end:    np.array([0,8]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, True)

        expected_moves = [
            (key, rM),
            (lock, dM + 2*rM + uM + rM),
            (water, lM + dM + 2*lM + uM + 4*rM),
            (end, 3*rM)]
        self.assert_moves_equal(moves, expected_moves)


    def test_sokoban_unsolvable(self):
        level = Level()
        level.upper_layer = np.array([
            [s,kR, e, e, e, e, g,lR, f ],
            [e, e, b, e, e, e, w, w, e ]], dtype=object)
        

        start = Start()
        key = Key("key")
        block = SokobanKey("block")
        water = SokobanLock("water")
        lock = Lock("lock")
        end = End()
        start.add_child_s([key, block, water])
        block.add_lock_s(water)
        key.add_lock_s(lock)
        water.add_child_s(lock)
        lock.add_child_s(end)

        positions_map = {
            start:  np.array([0,0]),
            key:    np.array([0,1]),
            block:  np.array([1,2]),
            water:  np.array([0,6]),
            lock:   np.array([0,7]),
            end:    np.array([0,8]),
        }

        does_level_follow_mission, moves = Solver.does_level_follow_mission(level, Node.find_all_nodes(start, method="topological-sort"), positions_map)
        self.assertEqual(does_level_follow_mission, False)
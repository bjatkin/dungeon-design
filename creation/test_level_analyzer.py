import numpy as np
import unittest
from creation.level_analyzer import LevelAnalyzer
from dungeon_level.dungeon_tiles import Tiles
from dungeon_level.level import Level
from dungeon_level.solution import Solution
from graph_structure.graph_node import Start, Key, Lock, End, SokobanKey, SokobanLock, Collectable, CollectableBarrier
from validation.solver import Solver

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

class TestLevelAnalyzer(unittest.TestCase):
    def get_level(self):
        start = Start()
        key = Key()
        lock = Lock()
        c0 = Collectable()
        sokoban_key = SokobanKey()
        sokoban_lock = SokobanLock()
        c1 = Collectable()
        key2 = Key()
        lock2 = Lock()
        barrier = CollectableBarrier()
        end = End()
        start.add_child_s([key, lock, c0])
        key.add_lock_s(lock)
        lock.add_child_s([sokoban_key, sokoban_lock, c1])
        sokoban_key.add_lock_s(sokoban_lock)
        sokoban_lock.add_child_s([key2, lock2])
        key2.add_lock_s(lock2)
        lock2.add_child_s(barrier)
        barrier.add_key_s([c0, c1])
        barrier.add_child_s(end)

        level = Level()
        level.mission = start
        level.upper_layer = np.array([
            [s, e, w, e, e, e, w, e],
            [e, e, w,kB, e, e,lB, B],
            [e, e, w, e, e, e, w, e],
            [e,kR, w, g, w, w, w, f],
            [e, e, w, e, c, e, w, e],
            [e, e, w, e, e, e, w, e],
            [c, e,lR, e, b, e, w, e],
            [e, e, w, e, e, e, w, e]
        ])
        level.positions_map = {
            start:          np.array([0,0]),
            key:            np.array([3,1]),
            lock:           np.array([6,2]),
            c0:             np.array([6,0]),
            c1:             np.array([4,4]),
            sokoban_key:    np.array([6,4]),
            sokoban_lock:   np.array([3,3]),
            key2:           np.array([1,3]),
            lock2:          np.array([1,6]),
            barrier:        np.array([1,7]),
            end:            np.array([3,7])}

        solution = Solver.does_level_follow_mission(level)

        level.solution = Solution(np.array([0, 0]))
        level.solution.add_step(start, [])
        level.solution.add_step(c0, 6*dM)
        level.solution.add_step(key, 3*uM + rM)
        level.solution.add_step(lock, 3*dM + rM)
        level.solution.add_step(c1, rM + uM + rM + uM)
        level.solution.add_step(sokoban_key, [])
        level.solution.add_step(sokoban_lock, dM + rM + dM + lM + dM + lM + 3*uM)
        level.solution.add_step(key2, 3*uM)
        level.solution.add_step(lock2, 3*rM)
        level.solution.add_step(barrier, rM)
        level.solution.add_step(end, dM)

        return level


    def test_scores(self):
        level = self.get_level()
        scores = LevelAnalyzer.get_score_from_metrics(level, LevelAnalyzer.quality_metrics, return_type="individual", raw_scores=True)
        score = LevelAnalyzer.get_score_from_metrics(level, LevelAnalyzer.quality_metrics)
        expected_scores = [
        11,            # _get_mission_length_score
        35,           # _get_moves_length_score
        6,            # _get_sokoban_turn_score
        1,            # _get_sokoban_count_score
        3.1818181818, # _get_average_length_of_step_score
        9,            # _get_decision_count_score
        2.25,         # _get_average_decisions_per_step_score
        3.5]          # _get_average_distance_between_locks_and_keys
        self.assertTrue(np.allclose(scores, expected_scores))

        expected_score = 53.431818
        self.assertAlmostEqual(score, expected_score, places=4)
import unittest
import numpy as np
from validation.sokoban.sokoban_solver import SokobanSolver
from dungeon_level.level import Level
from dungeon_level.dungeon_tiles import Tiles

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
b = Tiles.movable_block

class TestSokobanSolver(unittest.TestCase):
    def test_sokoban_solver(self):
        level = Level()
        level.upper_layer = np.array([
            [w, w, w, w, w, w, w],
            [w, s, e, e, w, e, w],
            [w, e, b, e, e, w, w],
            [w, w, w, w, w, w, w]], dtype=object)
        
        player_start = np.array([1, 1])
        sokoban_key = np.array([2, 2])
        sokoban_lock = np.array([2, 4])
        is_solvable, solution = SokobanSolver.is_sokoban_solvable(level, player_start, sokoban_key, sokoban_lock, get_solution=True)
        self.assertTrue(is_solvable)


    def test_sokoban_solver2(self):
        level = Level()
        level.upper_layer = np.array([
            [w, w, w, w, w, w, w],
            [w, e, e, e, e, e, w],
            [w, e, b, s, e, w, w],
            [w, e, e, e, e, e, w],
            [w, w, w, w, w, w, w]], dtype=object)
        
        player_start = np.array([2, 3])
        sokoban_key = np.array([2, 2])
        sokoban_lock = np.array([1, 5])
        is_solvable, solution = SokobanSolver.is_sokoban_solvable(level, player_start, sokoban_key, sokoban_lock, get_solution=True)
        self.assertTrue(is_solvable)
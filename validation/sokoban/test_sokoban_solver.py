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
b = Tiles.sokoban_block
g = Tiles.sokoban_goal

class TestSokobanSolver(unittest.TestCase):
    def test_sokoban_solver(self):
        layer = np.array([
            [w, w, w, w, w, w, w],
            [w, s, e, e, w, e, w],
            [w, e, b, e, g, w, w],
            [w, w, w, w, w, w, w]], dtype=object)
        
        player_position = np.array([1, 1])
        sokoban_key = np.array([2, 2])
        sokoban_lock = np.array([2, 4])
        is_solvable = SokobanSolver.is_sokoban_solvable(layer, player_position, sokoban_key, sokoban_lock, return_type="moves")
        self.assertTrue(is_solvable)


    def test_sokoban_solver2(self):
        layer = np.array([
            [w, w, w, w, w, w, w],
            [w, e, e, e, e, g, w],
            [w, e, b, s, e, w, w],
            [w, e, e, e, e, e, w],
            [w, w, w, w, w, w, w]], dtype=object)
        
        player_position = np.array([2, 3])
        sokoban_key = np.array([2, 2])
        sokoban_lock = np.array([1, 5])
        is_solvable = SokobanSolver.is_sokoban_solvable(layer, player_position, sokoban_key, sokoban_lock, return_type="moves")
        self.assertTrue(is_solvable)


    def test_sokoban_player_on_goal(self):
        layer = np.array([
            [w, w, w, w, w, w, w],
            [w, e, e, e, e, e, w],
            [w, e, b, s, e, w, w],
            [w, e, e, e, e, e, w],
            [w, w, w, w, w, w, w]], dtype=object)
        
        player_position = np.array([2, 3])
        sokoban_key = np.array([2, 2])
        sokoban_lock = np.array([2, 3])
        is_solvable = SokobanSolver.is_sokoban_solvable(layer, player_position, sokoban_key, sokoban_lock, return_type="moves")
        self.assertTrue(is_solvable)


    def test_sokoban_solver_unsolvable(self):
        layer = np.array([
            [w, w, w, w, w, w, w],
            [w, s, e, e, w, g, w],
            [w, e, b, e, e, w, w],
            [w, w, w, w, w, w, w]], dtype=object)
        
        player_position = np.array([1, 1])
        sokoban_key = np.array([2, 2])
        sokoban_lock = np.array([1, 5])
        is_solvable = SokobanSolver.is_sokoban_solvable(layer, player_position, sokoban_key, sokoban_lock, return_type="moves")
        self.assertFalse(is_solvable)

    def test_sokoban_solver_cant_reach_push(self):
        layer = np.array([
            [w, w, w, w, w, w, w, w],
            [w, g, s, e, b, e, e, w],
            [w, w, w, w, w, w, w, w]], dtype=object)
        
        player_position = np.array([1, 2])
        sokoban_key = np.array([1, 4])
        sokoban_lock = np.array([1, 1])
        is_solvable = SokobanSolver.is_sokoban_solvable(layer, player_position, sokoban_key, sokoban_lock, return_type="moves")
        self.assertFalse(is_solvable)
        

    def test_sokoban_solver_push_off_wall(self):
        layer = np.array([
            [w, w, w, w, w, w, w, w],
            [w, e, e, e, e, e, g, w],
            [w, e, s, e, b, e, e, w],
            [w, e, e, w, w, w, w, w],
            [w, w, w, w, w, w, w, w]], dtype=object)
        
        player_position = np.array([2, 2])
        sokoban_key = np.array([2, 4])
        sokoban_lock = np.array([1, 6])
        is_solvable = SokobanSolver.is_sokoban_solvable(layer, player_position, sokoban_key, sokoban_lock, return_type="moves")
        self.assertTrue(is_solvable)
        

    def test_sokoban_solver_no_space(self):
        layer = np.array([
            [w, w, w, w, w, w, w, w],
            [w, e, e, e, e, e, g, w],
            [w, e, s, e, b, e, e, w],
            [w, w, e, w, w, w, w, w],
            [w, w, w, w, w, w, w, w]], dtype=object)
        
        player_position = np.array([2, 2])
        sokoban_key = np.array([2, 4])
        sokoban_lock = np.array([1, 6])
        is_solvable = SokobanSolver.is_sokoban_solvable(layer, player_position, sokoban_key, sokoban_lock, return_type="moves")
        self.assertFalse(is_solvable)
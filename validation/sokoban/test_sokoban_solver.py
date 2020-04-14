import unittest
import numpy as np
from validation.sokoban.sokoban_solver import SokobanSolver
from validation.sokoban.sokomap import SokoMap, SokobanTiles
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

class TestSokobanSolver(unittest.TestCase):
    def test_sokoban_solver(self):
        layer = np.array([
            [w, w, w, w, w, w, w],
            [w, s, e, e, w, e, w],
            [w, e, b, e, e, w, w],
            [w, w, w, w, w, w, w]], dtype=object)
        
        player_start = np.array([1, 1])
        sokoban_key = np.array([2, 2])
        sokoban_lock = np.array([2, 4])
        is_solvable, solution = SokobanSolver.is_sokoban_solvable(layer, player_start, sokoban_key, sokoban_lock, get_solution=True)
        self.assertTrue(is_solvable)
        self.assertTrue(np.array_equal(np.array(solution), np.array([(1,0), (0,1), (0,1)])))


    def test_sokoban_solver2(self):
        layer = np.array([
            [w, w, w, w, w, w, w],
            [w, e, e, e, e, e, w],
            [w, e, b, s, e, w, w],
            [w, e, e, e, e, e, w],
            [w, w, w, w, w, w, w]], dtype=object)
        
        player_start = np.array([2, 3])
        sokoban_key = np.array([2, 2])
        sokoban_lock = np.array([1, 5])
        is_solvable, solution = SokobanSolver.is_sokoban_solvable(layer, player_start, sokoban_key, sokoban_lock, get_solution=True)
        self.assertTrue(is_solvable)
        self.assertTrue(np.array_equal(np.array(solution), np.array([(1,0), (0,-1), (-1,0), (0,-1), (-1,0), (0,1), (0,1), (0,1)])))

    def test_sokoban_player_on_goal(self):
        layer = np.array([
            [w, w, w, w, w, w, w],
            [w, e, e, e, e, e, w],
            [w, e, b, s, e, w, w],
            [w, e, e, e, e, e, w],
            [w, w, w, w, w, w, w]], dtype=object)
        
        player_start = np.array([2, 3])
        sokoban_key = np.array([2, 2])
        sokoban_lock = np.array([2, 3])
        is_solvable, solution = SokobanSolver.is_sokoban_solvable(layer, player_start, sokoban_key, sokoban_lock, get_solution=True)
        self.assertTrue(is_solvable)
        self.assertTrue(np.array_equal(np.array(solution), np.array([(-1,0), (0,-1), (0,-1), (1,0), (0,1)])))

    def test_is_valid_position(self):
        sG = SokobanTiles.TILE_GOAL
        sB = SokobanTiles.TILE_BLOCK
        sE = SokobanTiles.TILE_SPACE
        sP = SokobanTiles.TILE_PLAYER
        sokomap = SokoMap()
        sokomap.set_map(np.array([[sE, sE, sE, sE],
                                  [sE, sP, sB, sG],
                                  [sE, sE, sE, sE]]), np.array([1,1]))
            
        for i in range(3):
            for j in range(4):
                self.assertTrue(SokoMap.is_legal_position(sokomap.sokomap, np.array([i, j])))

                self.assertFalse(SokoMap.is_legal_position(sokomap.sokomap, np.array([-i - 1, j])))
                self.assertFalse(SokoMap.is_legal_position(sokomap.sokomap, np.array([i, -j - 1])))
                self.assertFalse(SokoMap.is_legal_position(sokomap.sokomap, np.array([-i - 1, -j - 1])))
                self.assertFalse(SokoMap.is_legal_position(sokomap.sokomap, np.array([i, j + 4])))
                self.assertFalse(SokoMap.is_legal_position(sokomap.sokomap, np.array([i + 3, j])))
                self.assertFalse(SokoMap.is_legal_position(sokomap.sokomap, np.array([i + 3, j + 4])))
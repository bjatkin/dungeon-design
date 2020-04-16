import unittest
import numpy as np
from validation.path_finder import PathFinder
from validation.player_traverser import PlayerTraverser
from dungeon_level.dungeon_tiles import Tiles

class TestPathFinder(unittest.TestCase):
    def test_manhattan_distance(self):
        self.assertEqual(PathFinder.manhattan_distance(np.array([1, 2]), np.array([3, 7])), 7)
        self.assertEqual(PathFinder.manhattan_distance(np.array([5, -2]), np.array([2, 12])), 17)
        self.assertEqual(PathFinder.manhattan_distance(np.array([0,0]), np.array([0,0])), 0)


    def test_diagonal_manhattan(self):
        self.assertEqual(PathFinder.diagonal_manhattan_distance(np.array([1, 1]), np.array([3, 3])), 28)
        self.assertEqual(PathFinder.diagonal_manhattan_distance(np.array([1, 1]), np.array([1, 4])), 30)
        self.assertEqual(PathFinder.diagonal_manhattan_distance(np.array([1, 1]), np.array([6, 4])), 62)
    

    def test_path_finder(self):
        layer = np.array([Tiles.empty] * 7 * 6).reshape([6,7])
        layer[2,1:6] = Tiles.wall
        layer[1,1] = Tiles.wall

        f_costs, parents = PathFinder.a_star(layer, np.array([4,5]), np.array([1,2]), PlayerTraverser.can_traverse, True)

        expected_f_costs = np.array(
            [[np.inf, np.inf, 82,     76,     76,     82,     96],
             [np.inf, np.inf, 68,     68,     68,     68,     74],
             [82,     np.inf, np.inf, np.inf, np.inf, np.inf, 68],
             [82,     68,     54,     48,     42,     48,     62],
             [96,     74,     60,     54,     48,     np.inf, 62],
             [np.inf, 88,     74,     68,     62,     62,     70]])

        expected_parents = np.array(
            [[None, None, np.array([1,1]), np.array([1,1]), np.array([1,1]), np.array([1,0]), np.array([1,-1])],
             [None, None, np.array([0,1]), np.array([0,1]), np.array([0,1]), np.array([1,1]), np.array([1,0])], 
             [np.array([1, 1]), None, None, None, None, None, np.array([1, -1])],
             [np.array([0, 1]), np.array([0, 1]), np.array([0, 1]), np.array([0, 1]), np.array([1, 1]), np.array([1, 0]), np.array([1, -1])],
             [np.array([-1, 1]), np.array([0, 1]), np.array([0, 1]), np.array([0, 1]), np.array([0, 1]), None, np.array([0, -1])],
             [None, np.array([-1, 1]), np.array([-1, 1]), np.array([-1, 1]), np.array([-1, 1]), np.array([-1, 0]), np.array([-1, -1])]])

        self.assertTrue(np.array_equal(f_costs, expected_f_costs))
        
        expected_parents = expected_parents.flatten()
        parents = parents.flatten()
        for i in range(expected_parents.shape[0]):
            self.assertTrue(np.array_equal(parents[i], expected_parents[i]))


        path = PathFinder.find_path(layer, np.array([4,5]), np.array([1,2]), PlayerTraverser.can_traverse, True, return_type="path")
        expected_path = [
            [4,5],
            [3,5],
            [2,6],
            [1,5],
            [1,4],
            [1,3],
            [1,2]]

        self.assertTrue(np.array_equal(np.array(path), np.array(expected_path)))
        moves = PathFinder.find_path(layer, np.array([4,5]), np.array([1,2]), PlayerTraverser.can_traverse, True, return_type="moves")
        expected_moves = [
            [-1, 0],
            [-1, 1],
            [-1, -1],
            [0, -1],
            [0, -1],
            [0, -1]]
            
        self.assertTrue(np.array_equal(np.array(moves), np.array(expected_moves)))



    def test_path_finder_unconnected(self):
        layer = np.array([Tiles.empty] * 8 * 10).reshape([8,10])
        layer[:,4] = Tiles.wall

        f_costs, parents = PathFinder.a_star(layer, np.array([2,0]), np.array([2,8]), PlayerTraverser.can_traverse)
        self.assertEqual(parents, None)
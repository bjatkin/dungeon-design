import unittest
import numpy as np
from dungeon_level.dungeon_tiles import Tiles
from generation.drawing import Drawing

class TestDrawing(unittest.TestCase):
    def test_draw_line(self):
        e = Tiles.empty
        w = Tiles.wall
        layer = np.full((5,5), e)
        Drawing.draw_line(layer, (0,0), (4,4), w)
        expected_layer = np.array([
            [w, e, e, e, e],
            [e, w, e, e, e],
            [e, e, w, e, e],
            [e, e, e, w, e],
            [e, e, e, e, w] ])
        # Test normal line
        self.assertTrue((layer == expected_layer).all())

        layer = np.full((5,5), e)
        Drawing.draw_line(layer, (-2,1), (11,6), w)
        expected_layer = np.array([
            [e, e, w, e, e],
            [e, e, w, e, e],
            [e, e, e, w, e],
            [e, e, e, w, e],
            [e, e, e, w, e] ])
        # Test line clipping off side
        self.assertTrue((layer == expected_layer).all())


    def test_draw_ellipse(self):
        e = Tiles.empty
        w = Tiles.wall
        layer = np.full((8,8), e)
        Drawing.draw_ellipse(layer, (2, 2), 2, 2, w)
        expected_layer = np.array([
            [e, w, w, w, e, e, e, e],
            [w, e, e, e, w, e, e, e],
            [w, e, e, e, w, e, e, e],
            [w, e, e, e, w, e, e, e],
            [e, w, w, w, e, e, e, e],
            [e, e, e, e, e, e, e, e],
            [e, e, e, e, e, e, e, e],
            [e, e, e, e, e, e, e, e]])
        # Test normal circle
        self.assertTrue((layer == expected_layer).all())

        layer = np.full((8,8), e)
        Drawing.draw_ellipse(layer, (7, 5), 5, 3, w)
        expected_layer = np.array([
            [e, e, e, e, e, e, e, e],
            [e, e, e, e, e, e, e, e],
            [e, e, e, e, w, w, w, e],
            [e, e, e, w, e, e, e, w],
            [e, e, e, w, e, e, e, w],
            [e, e, w, e, e, e, e, e],
            [e, e, w, e, e, e, e, e],
            [e, e, w, e, e, e, e, e]])
        # Test ellipse clipping off side
        self.assertTrue((layer == expected_layer).all())


    def test_fill_ellipse(self):
        e = Tiles.empty
        w = Tiles.wall
        layer = np.full((8,8), e)
        Drawing.fill_ellipse(layer, (2, 2), 2, 2, w)
        expected_layer = np.array([
            [e, w, w, w, e, e, e, e],
            [w, w, w, w, w, e, e, e],
            [w, w, w, w, w, e, e, e],
            [w, w, w, w, w, e, e, e],
            [e, w, w, w, e, e, e, e],
            [e, e, e, e, e, e, e, e],
            [e, e, e, e, e, e, e, e],
            [e, e, e, e, e, e, e, e]])
        # Test normal circle
        self.assertTrue((layer == expected_layer).all())

        layer = np.full((8,8), e)
        Drawing.fill_ellipse(layer, (7, 5), 5, 3, w)
        expected_layer = np.array([
            [e, e, e, e, e, e, e, e],
            [e, e, e, e, e, e, e, e],
            [e, e, e, e, w, w, w, e],
            [e, e, e, w, w, w, w, w],
            [e, e, e, w, w, w, w, w],
            [e, e, w, w, w, w, w, w],
            [e, e, w, w, w, w, w, w],
            [e, e, w, w, w, w, w, w]])
        # Test ellipse clipping off side
        self.assertTrue((layer == expected_layer).all())


    def test_draw_rectangle(self):
        e = Tiles.empty
        w = Tiles.wall
        layer = np.full((5,5), e)
        Drawing.draw_rectangle(layer, (0,0), (3,2), w)
        expected_layer = np.array([
            [w, w, w, e, e],
            [w, e, w, e, e],
            [w, e, w, e, e],
            [w, w, w, e, e],
            [e, e, e, e, e] ])
        # Test normal rectangle
        self.assertTrue((layer == expected_layer).all())

        layer = np.full((5,5), e)
        Drawing.draw_rectangle(layer, (2,3), (8,6), w)
        expected_layer = np.array([
            [e, e, e, e, e],
            [e, e, e, e, e],
            [e, e, e, w, w],
            [e, e, e, w, e],
            [e, e, e, w, e] ])
        # Test rectangle clipping off side
        self.assertTrue((layer == expected_layer).all())


    def test_fill_rectangle(self):
        e = Tiles.empty
        w = Tiles.wall
        layer = np.full((5,5), e)
        Drawing.fill_rectangle(layer, (0,0), (3,2), w)
        expected_layer = np.array([
            [w, w, w, e, e],
            [w, w, w, e, e],
            [w, w, w, e, e],
            [w, w, w, e, e],
            [e, e, e, e, e] ])
        # Test normal rectangle
        self.assertTrue((layer == expected_layer).all())

        layer = np.full((5,5), e)
        Drawing.fill_rectangle(layer, (2,3), (8,6), w)
        expected_layer = np.array([
            [e, e, e, e, e],
            [e, e, e, e, e],
            [e, e, e, w, w],
            [e, e, e, w, w],
            [e, e, e, w, w] ])
        # Test rectangle clipping off side
        self.assertTrue((layer == expected_layer).all())


    def test_ensure_min_max_correct(self):
        a, b = Drawing.ensure_max_min_correct([0,0], [3,3])
        self.assertTrue((a == np.array([0,0])).all())
        self.assertTrue((b == np.array([3,3])).all())

        a, b = Drawing.ensure_max_min_correct([5,0], [3,2])
        self.assertTrue((a == np.array([3,0])).all())
        self.assertTrue((b == np.array([5,2])).all())

        a, b = Drawing.ensure_max_min_correct([3,5], [3,2])
        self.assertTrue((a == np.array([3,2])).all())
        self.assertTrue((b == np.array([3,5])).all())
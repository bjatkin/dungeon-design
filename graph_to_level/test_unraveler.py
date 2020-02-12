import unittest
import numpy as np
from graph_to_level.unraveler import Unraveler
from graph_structure.graph_node import GNode
from graph_to_level.spatial_graph_visualizer import SpatialGraphVisualizer
import matplotlib.pyplot as plt
from PIL import Image
import time

class TestUnraveler(unittest.TestCase):
    def get_graph(self):
        a = GNode([], [], "a")
        b = GNode([], [], "b")
        c = GNode([], [], "c")
        d = GNode([], [], "d")
        e = GNode([], [], "e")
        f = GNode([], [], "f")
        g = GNode([], [], "g")
        h = GNode([], [], "h")
        i = GNode([], [], "i")

        a.add_child_s(b)
        a.add_child_s(c)
        a.add_child_s(d)
        b.add_child_s(e)
        c.add_child_s(f)
        c.add_child_s(g)
        # c.add_child_s(h)
        # c.add_child_s(i)
        # h.add_child_s(i)

        return a, {a, b, c, d, e, f, g}


    def test_find_all_nodes(self):
        a, all_nodes = self.get_graph()

        nodes = set()
        Unraveler.find_all_nodes(a, nodes)
        self.assertEqual(nodes, all_nodes)

    def test_build_spatial_graph(self):
        a, all_nodes = self.get_graph()

        nodes, positions, adjacencies = Unraveler.build_spatial_graph(a)
        expected_positions = np.array([
            [0,0],
            [1,0],
            [2,0],
            [3,0],
            [4,0],
            [5,0],
            [6,0]], dtype=float)
        expected_adjacencies = np.array([
            #a  b  c  d  e  f  g
            [0, 1, 1, 1, 0, 0, 0], #a 
            [1, 0, 0, 0, 1, 0, 0], #b 
            [1, 0, 0, 0, 0, 1, 1], #c 
            [1, 0, 0, 0, 0, 0, 0], #d 
            [0, 1, 0, 0, 0, 0, 0], #e 
            [0, 0, 1, 0, 0, 0, 0], #f 
            [0, 0, 1, 0, 0, 0, 0]  #g 
        ])
        self.assertEqual(nodes, sorted(all_nodes, key=lambda x: x.name))
        # self.assertTrue((positions == expected_positions).all())
        self.assertTrue((adjacencies == expected_adjacencies).all())

    def test_unravel(self):
        def debug_method(node_positions, adjacency_matrix, debug_info):
            if debug_info == None:
                im = plt.imshow(Image.new('RGB', (1,1)))
                now = time.time()
                plt.draw()
                plt.pause(3)
            else:
                im = debug_info[0]
                now = debug_info[1]

            img = SpatialGraphVisualizer.visualize_graph(node_positions, adjacency_matrix, window_min=np.array([0,0]), window_max=np.array([8,8]))
            im.set_data(img)
            plt.draw()
            plt.pause(0.0001)
            print(time.time() - now)
            now = time.time()
            return im, now

        a = GNode([], [], "a")
        b = GNode([], [], "b")
        c = GNode([], [], "c")
        d = GNode([], [], "d")
        a.add_child_s(b)
        b.add_child_s(c)
        c.add_child_s(a)
        
        # a.add_child_s(d)
        # b.add_child_s(d)
        # c.add_child_s(d)
        a, all_nodes = self.get_graph()
        Unraveler.unravel(a, debug_method)
import unittest
import numpy as np
from graph_to_level.unraveler import Unraveler
from graph_structure.graph_node import GNode
from graph_to_level.spatial_graph_visualizer import SpatialGraphVisualizer
import matplotlib.pyplot as plt
from PIL import Image
import time

class TestUnraveler(unittest.TestCase):
    def get_man_graph(self):
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
        c.add_child_s(h)
        c.add_child_s(i)
        h.add_child_s(i)

        return a, {a, b, c, d, e, f, g, h, i}

    def get_house_graph(self):
        a = GNode([], [], "a")
        b = GNode([], [], "b")
        c = GNode([], [], "c")
        d = GNode([], [], "d")
        e = GNode([], [], "e")
        a.add_child_s(b)
        b.add_child_s(c)
        c.add_child_s(d)
        d.add_child_s(a)
        c.add_child_s(e)
        e.add_child_s(a)
        e.add_child_s(d)

        return a, {a, b, c, d, e}

    def get_triangle_graph(self):
        a = GNode([], [], "a")
        b = GNode([], [], "b")
        c = GNode([], [], "c")
        d = GNode([], [], "d")
        a.add_child_s(b)
        b.add_child_s(c)
        c.add_child_s(a)
        a.add_child_s(d)
        b.add_child_s(d)
        c.add_child_s(d)

        return a, {a, b, c, d}


    def test_find_all_nodes(self):
        a, all_nodes = self.get_man_graph()

        nodes = set()
        Unraveler.find_all_nodes(a, nodes)
        self.assertEqual(nodes, all_nodes)

    def test_build_spatial_graph(self):
        a, all_nodes = self.get_man_graph()

        nodes, positions, adjacencies = Unraveler.build_spatial_graph(a)
        expected_positions = np.array([
            [0,0],
            [1,0],
            [2,0],
            [3,0],
            [4,0],
            [5,0],
            [6,0],
            [7,0],
            [8,0]], dtype=float)
        expected_adjacencies = np.array([
            #a  b  c  d  e  f  g  h  i
            [0, 1, 1, 1, 0, 0, 0, 0, 0], #a 
            [1, 0, 0, 0, 1, 0, 0, 0, 0], #b 
            [1, 0, 0, 0, 0, 1, 1, 1, 1], #c 
            [1, 0, 0, 0, 0, 0, 0, 0, 0], #d 
            [0, 1, 0, 0, 0, 0, 0, 0, 0], #e 
            [0, 0, 1, 0, 0, 0, 0, 0, 0], #f 
            [0, 0, 1, 0, 0, 0, 0, 0, 0], #g 
            [0, 0, 1, 0, 0, 0, 0, 0, 1], #h
            [0, 0, 1, 0, 0, 0, 0, 1, 0], #i
        ])
        self.assertEqual(nodes, sorted(all_nodes, key=lambda x: x.name))
        # self.assertTrue((positions == expected_positions).all())
        self.assertTrue((adjacencies == expected_adjacencies).all())

    def draw_lines(self, p1, p2, p3, p4):
        plt.plot([p1[1], p2[1]], [p1[0], p2[0]], 'k-')
        plt.plot([p3[1], p4[1]], [p3[0], p4[0]], 'k-')
        plt.show()


    def test_intersection(self):
        p1 = np.array([1., 1.])
        p2 = np.array([5., 6.])
        p3 = np.array([3., 2.])
        p4 = np.array([0., 7.])
        # Line segments intersect
        self.assertTrue(np.allclose(Unraveler.find_intersection(p1, p2, p3, p4), np.array([2.49, 2.86]), rtol=0.1))

        p4 = np.array([2.5,2.5])
        # Line intersects, but line segment does not
        self.assertTrue(Unraveler.find_intersection(p1, p2, p3, p4) is None)

        p1 = np.array([1., 1.])
        p2 = np.array([5., 5.])
        p3 = np.array([0., 1.])
        p4 = np.array([4., 5.])
        # Parallel line check
        self.assertTrue(Unraveler.find_intersection(p1, p2, p3, p4) is None)

        p3 = np.array([5., 5.])
        p4 = np.array([4., 9.])
        # self.draw_lines(p1, p2, p3, p4)
        self.assertTrue(Unraveler.find_intersection(p1, p2, p3, p4) is None)

        self.assertTrue(np.allclose(Unraveler.find_intersection(p1, p2, p3, p4, count_endpoints=True), np.array([5., 5.]), rtol=0.0))

        

    def test_unravel(self):
        def debug_method(node_positions, adjacency_matrix, debug_info, last_frame):
            if debug_info == None:
                im = plt.imshow(Image.new('RGB', (1,1)))
                now = time.time()
                plt.draw()
                # plt.pause(3)
            else:
                im = debug_info[0]
                now = debug_info[1]

            img = SpatialGraphVisualizer.visualize_graph(node_positions, adjacency_matrix, resolution=25, window_min=np.array([-8, -8]), window_max=np.array([8,8]))
            im.set_data(img)
            plt.draw()
            plt.pause(0.0001)
            print(time.time() - now)
            now = time.time()
            if last_frame:
                plt.pause(1.0)
            return im, now

        graph, all_nodes = self.get_graph_a()
        Unraveler.unravel(graph, debug_method)

        graph, all_nodes = self.get_graph_b()
        Unraveler.unravel(graph, debug_method)

        graph, all_nodes = self.get_house_graph()
        Unraveler.unravel(graph, debug_method)

        graph, all_nodes = self.get_triangle_graph()
        Unraveler.unravel(graph, debug_method)
        
        graph, all_nodes = self.get_man_graph()
        Unraveler.unravel(graph, debug_method)


    def get_graph_a(self):
        n1 = GNode([], [], "a")
        n2 = GNode([], [], "b")
        n3 = GNode([], [], "c")
        n4 = GNode([], [], "d")
        n5 = GNode([], [], "e")

        n1.add_child_s([n3, n4, n5])
        n2.add_child_s([n3, n4, n5])
        n3.add_child_s([n1, n2, n4, n5])
        n4.add_child_s([n1, n2, n3, n5])
        n5.add_child_s([n1, n2, n3, n4])

        return n1, {n1, n2, n3, n4, n5}

    def get_graph_b(self):
        n1 = GNode([], [], "a")
        n2 = GNode([], [], "b")
        n3 = GNode([], [], "c")
        n4 = GNode([], [], "d")
        n5 = GNode([], [], "e")
        n6 = GNode([], [], "f")
        n7 = GNode([], [], "g")
        n8 = GNode([], [], "h")
        n9 = GNode([], [], "i")
        n10 = GNode([], [], "j")

        n1.add_child_s([n2, n3])
        n2.add_child_s(n4)
        n3.add_child_s([n4, n5])
        n5.add_child_s(n6)
        n6.add_child_s(n7)
        n7.add_child_s([n8, n9])
        n8.add_child_s(n10)
        n9.add_child_s(n10)

        return n1, {n1, n2, n3, n4, n5, n6, n7, n8, n9, n10}

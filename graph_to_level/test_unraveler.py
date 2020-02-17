import unittest
import numpy as np
from graph_to_level.unraveler import Unraveler
from graph_to_level.test_unraveler_debug_method import debug_method
from graph_structure.graph_node import GNode
from graph_to_level.test_graphs import TestGraphs
from graph_to_level.spatial_graph_generator import SpatialGraphGenerator


class TestUnraveler(unittest.TestCase):
    def test_unravel(self):
        return

        graph, all_nodes = TestGraphs.get_graph_a()
        _, nodes, adjacencies = SpatialGraphGenerator.init_spatial_graph(graph)
        Unraveler.unravel_spatial_graph(nodes, adjacencies, debug_method)

        graph, all_nodes = TestGraphs.get_graph_b()
        _, nodes, adjacencies = SpatialGraphGenerator.init_spatial_graph(graph)
        Unraveler.unravel_spatial_graph(nodes, adjacencies, debug_method)

        graph, all_nodes = TestGraphs.get_house_graph()
        _, nodes, adjacencies = SpatialGraphGenerator.init_spatial_graph(graph)
        Unraveler.unravel_spatial_graph(nodes, adjacencies, debug_method)

        graph, all_nodes = TestGraphs.get_triangle_graph()
        _, nodes, adjacencies = SpatialGraphGenerator.init_spatial_graph(graph)
        Unraveler.unravel_spatial_graph(nodes, adjacencies, debug_method)
        
        graph, all_nodes = TestGraphs.get_man_graph()
        _, nodes, adjacencies = SpatialGraphGenerator.init_spatial_graph(graph)
        Unraveler.unravel_spatial_graph(nodes, adjacencies, debug_method)




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

        

import unittest
import numpy as np
from graph_to_level.spatial_graph_generator import SpatialGraphGenerator
from graph_to_level.test_graphs import TestGraphs

class TestSpatialGraphGenerator(unittest.TestCase):

    def test_find_all_nodes(self):
        a, all_nodes = TestGraphs.get_man_graph()
        nodes = set()
        SpatialGraphGenerator.find_all_nodes(a, nodes)
        self.assertEqual(nodes, all_nodes)

        a, all_nodes = TestGraphs.get_house_graph()
        nodes = set()
        SpatialGraphGenerator.find_all_nodes(a, nodes)
        self.assertEqual(nodes, all_nodes)

        a, all_nodes = TestGraphs.get_graph_b()
        nodes = set()
        SpatialGraphGenerator.find_all_nodes(a, nodes)
        self.assertEqual(nodes, all_nodes)



    def test_init_spatial_graph(self):
        a, all_nodes = TestGraphs.get_man_graph()

        nodes, positions, adjacencies = SpatialGraphGenerator.init_spatial_graph(a, random_initial_positions=False)
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
        self.assertTrue((positions == expected_positions).all())
        self.assertTrue((adjacencies == expected_adjacencies).all())

    def test_center_graph_in_level(self):
        node_positions = np.array([
            [1,3],
            [3,3],
            [1,5],
            [3,5]], dtype=float)
        SpatialGraphGenerator.center_graph_in_level(node_positions, np.array([30,30]))

        expected_positions = np.array([
            [3.75,3.75],
            [26.25,3.75],
            [3.75,26.25],
            [26.25,26.25]])
        self.assertTrue(np.allclose(node_positions, expected_positions, rtol=0.1))


    def test_generate_spatial_graph_placement(self):
        node_positions = np.array([
            [1,3],
            [3,3],
            [1,5],
            [3,5]], dtype=float)
        SpatialGraphGenerator.center_graph_in_level(node_positions, np.array([30,30]))
        SpatialGraphGenerator.align_nodes_to_grid(node_positions)

        expected_positions = np.array([
            [4,4],
            [26,4],
            [4,26],
            [26,26]])
        self.assertTrue(np.allclose(node_positions, expected_positions, rtol=0.1))

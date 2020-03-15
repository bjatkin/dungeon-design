import unittest
import numpy as np
from graph_to_level.spatial_graph import SpatialGraph, SpatialGraphNode
from graph_to_level.subgraph_finder import SubgraphFinder

class TestSubgraphFinder(unittest.TestCase):
    def test_subgraph_finder_no_subgraph(self):
        a0 = SpatialGraphNode("0")
        a1 = SpatialGraphNode("1")
        a2 = SpatialGraphNode("2")
        a3 = SpatialGraphNode("3")
        a4 = SpatialGraphNode("4")
        a5 = SpatialGraphNode("5")
        a0.add_adjacent_nodes([a1, a2, a3, a4, a5])
        a_nodes = {a0, a1, a2, a3, a4, a5}
        

        b0 = SpatialGraphNode("0")
        b1 = SpatialGraphNode("1")
        b2 = SpatialGraphNode("2")
        b3 = SpatialGraphNode("3")
        b4 = SpatialGraphNode("4")
        b5 = SpatialGraphNode("5")
        b0.add_adjacent_nodes([b1, b3])
        b1.add_adjacent_nodes([b0, b2, b4])
        b2.add_adjacent_nodes([b1, b5])
        b3.add_adjacent_nodes([b0, b4])
        b4.add_adjacent_nodes([b3, b1, b5])
        b5.add_adjacent_nodes([b4, b2])
        b_nodes = {b0, b1, b2, b3, b4, b5}

        mapping = SubgraphFinder.get_subgraph_mapping(b_nodes, a_nodes)

        self.assertIs(mapping, None)


    def test_subgraph_finder(self):
        a0 = SpatialGraphNode("0")
        a1 = SpatialGraphNode("1")
        a2 = SpatialGraphNode("2")
        a3 = SpatialGraphNode("3")
        a0.add_adjacent_nodes([a1, a2, a3])
        a_nodes = {a0, a1, a2, a3}
        

        b0 = SpatialGraphNode("0")
        b1 = SpatialGraphNode("1")
        b2 = SpatialGraphNode("2")
        b3 = SpatialGraphNode("3")
        b4 = SpatialGraphNode("4")
        b5 = SpatialGraphNode("5")
        b0.add_adjacent_nodes([b1, b3])
        b1.add_adjacent_nodes([b0, b2, b4])
        b2.add_adjacent_nodes([b1, b5])
        b3.add_adjacent_nodes([b0, b4])
        b4.add_adjacent_nodes([b3, b1, b5])
        b5.add_adjacent_nodes([b4, b2])
        b_nodes = {b0, b1, b2, b3, b4, b5}

        mapping = SubgraphFinder.get_subgraph_mapping(b_nodes, a_nodes)

        possible_expected_mappings = [
            {a0:b1, a1:b0, a2:b2, a3:b4},
            {a0:b1, a1:b0, a3:b2, a2:b4},
            {a0:b1, a2:b0, a1:b2, a3:b4},
            {a0:b1, a2:b0, a3:b2, a1:b4},
            {a0:b1, a3:b0, a1:b2, a2:b4},
            {a0:b1, a3:b0, a2:b2, a1:b4},

            {a0:b4, a1:b3, a2:b1, a3:b5},
            {a0:b4, a1:b3, a3:b1, a2:b5},
            {a0:b4, a2:b3, a1:b1, a3:b5},
            {a0:b4, a2:b3, a3:b1, a1:b5},
            {a0:b4, a3:b3, a1:b1, a2:b5},
            {a0:b4, a3:b3, a2:b1, a1:b5},
        ]
        matches_possible_mapping = False
        for possible_expected_mapping in possible_expected_mappings:
            if possible_expected_mapping == mapping:
                matches_possible_mapping = True
        self.assertTrue(matches_possible_mapping)
import unittest
import numpy as np
from dungeon_level.dungeon_tiles import Tiles
from graph_to_level.spatial_graph import SpatialGraph, SpatialGraphNode

e = Tiles.empty
w = Tiles.wall
F = Tiles.fire
W = Tiles.water
s = Tiles.player
f = Tiles.finish

class TestSpatialGraph(unittest.TestCase):
    def test_get_graph_nodes_from_layer(self):
        layer = np.array([
            [e, e, w, e, e, w, e, e],
            [e, e, w, e, e, w, e, e],
            [w, w, w, w, w, w, w, w],
            [e, e, w, e, e, w, e, e],
            [e, e, w, e, e, w, e, e],
            [w, w, w, w, w, w, w, w],
            [e, e, w, e, e, w, e, e],
            [e, e, w, e, e, w, e, e]], dtype=object)

        nodes = SpatialGraph.get_graph_nodes_from_layer(layer)
        self.assertEqual(len(nodes), 9)
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for i, node in enumerate(nodes):
            x = i % 3
            y = i // 3
            node_mask = np.zeros((8,8))
            node_mask[3*y:3*y+2,3*x:3*x+2] = 1
            self.assertTrue(np.array_equal(node_mask, node.mask))
            expected_neighbor_names = set()
            for neighbor in neighbors:
                if (x + neighbor[1] >=0 and x + neighbor[1] <= 2 and 
                    y + neighbor[0] >=0 and y + neighbor[0] <= 2):
                    neighbor_index = 3 * (y + neighbor[0]) + (x + neighbor[1])
                    expected_neighbor_names.add(str(neighbor_index))
            neighbor_names = { node.name for node in node.adjacent_nodes }
            self.assertEqual(expected_neighbor_names, neighbor_names)

        
    def test_get_shared_edge_mask_between_nodes(self):
        layer = np.array([
            [e, e, w, e, e, w, e, e],
            [e, e, w, e, e, w, e, e],
            [w, w, w, w, w, w, w, w],
            [e, e, w, e, e, w, e, e],
            [e, e, w, e, e, w, e, e],
            [w, w, w, w, w, w, w, w],
            [e, e, w, e, e, w, e, e],
            [e, e, w, e, e, w, e, e]], dtype=object)

        nodes = SpatialGraph.get_graph_nodes_from_layer(layer)
        
        expected_shared_edge = np.array([
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]], dtype=object)
        self.assertTrue(np.array_equal(SpatialGraph.get_shared_edge_mask_between_nodes(nodes[0], nodes[1]), expected_shared_edge))

        expected_shared_edge = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]], dtype=object)
        self.assertTrue(np.array_equal(SpatialGraph.get_shared_edge_mask_between_nodes(nodes[0], nodes[3]), expected_shared_edge))

        expected_shared_edge = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]], dtype=object)
        self.assertTrue(np.array_equal(SpatialGraph.get_shared_edge_mask_between_nodes(nodes[0], nodes[4]), expected_shared_edge))


    def get_nodes(self):
        n0 = SpatialGraphNode("0", np.array([
            [1, 1, 0],
            [0, 1, 0],
            [0, 0, 0]]))
        n1 = SpatialGraphNode("1", np.array([
            [0, 0, 0],
            [0, 1, 0],
            [1, 1, 1]]))
        n2 = SpatialGraphNode("2", np.array([
            [0, 0, 1],
            [1, 0, 1],
            [0, 0, 0]]))
        n3 = SpatialGraphNode("3", np.array([
            [1, 0, 0],
            [1, 0, 0],
            [1, 1, 0]]))
        n4 = SpatialGraphNode("4", np.array([
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0]]))
        return n0, n1, n2, n3, n4


    def test_add_remove_adjacent_nodes(self):
        n0, n1, n2, n3, n4 = self.get_nodes()

        # Add single
        n0.add_adjacent_nodes(n1)
        n1.add_adjacent_nodes([n2])
        # Add multiple
        n2.add_adjacent_nodes([n3, n4])
        n3.add_adjacent_nodes(n4)

        self.assertEqual(n0.adjacent_nodes, {n1})
        self.assertEqual(n1.adjacent_nodes, {n0, n2})
        self.assertEqual(n2.adjacent_nodes, {n1, n3, n4})

        # Remove single
        n1.remove_adjacent_nodes(n0)
        self.assertEqual(n1.adjacent_nodes, {n2})
        self.assertEqual(n0.adjacent_nodes, set())

        # Remove multiple
        n2.remove_adjacent_nodes([n1, n3])
        self.assertEqual(n2.adjacent_nodes, {n4})
        self.assertEqual(n1.adjacent_nodes, set())
        self.assertEqual(n3.adjacent_nodes, {n4})

    
    def test_merge_nodes(self):
        # Test merging adjacent nodes (should work)
        n0, n1, n2, n3, n4 = self.get_nodes()
        n0.add_adjacent_nodes([n1, n2])
        n1.add_adjacent_nodes([n0, n4])
        n2.add_adjacent_nodes([n0, n3, n4])
        n3.add_adjacent_nodes(n2)
        n4.add_adjacent_nodes([n1, n2])

        n0.merge_node(n1)

        expected_mask = np.array([
            [1, 1, 0],
            [0, 1, 0],
            [1, 1, 1]])
        self.assertTrue(np.array_equal(expected_mask, n0.mask))

        self.assertEqual(n0.adjacent_nodes, {n2, n4})
        self.assertEqual(n1.adjacent_nodes, set())
        self.assertEqual(n2.adjacent_nodes, {n0, n3, n4})
        self.assertEqual(n4.adjacent_nodes, {n0, n2})


        # Test merging non-adjacent nodes (shouldn't work)
        n0, n1, n2, n3, n4 = self.get_nodes()
        n0.add_adjacent_nodes([n1, n2])
        n1.add_adjacent_nodes([n0, n4])
        n2.add_adjacent_nodes([n0, n3, n4])
        n3.add_adjacent_nodes(n2)
        n4.add_adjacent_nodes([n1, n2])

        n2.merge_node(n1)

        expected_mask = np.array([
            [0, 0, 1],
            [1, 0, 1],
            [0, 0, 0]])
        self.assertTrue(np.array_equal(expected_mask, n2.mask))

        self.assertEqual(n0.adjacent_nodes, {n1, n2})
        self.assertEqual(n1.adjacent_nodes, {n0, n4})
        self.assertEqual(n2.adjacent_nodes, {n0, n3, n4})
        self.assertEqual(n3.adjacent_nodes, {n2})
        self.assertEqual(n4.adjacent_nodes, {n1, n2})
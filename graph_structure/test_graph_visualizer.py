import unittest
from graph_structure.graph import Graph
from graph_structure.graph_visualizer import GraphVisualizer
from graph_structure.graph_node import Node, Start, End, Key, Lock, Collectable, CollectableBarrier, GNode

class TestGraphVisualizer(unittest.TestCase):
    def assert_no_overlapping_layout(self, layout):
        layout_positions = set([(v[0], v[1]) for v in layout.values()])
        self.assertEqual(len(layout_positions), len(layout.values()))


    def test_layout(self):
        n = [GNode("n{}".format(i)) for i in range(13)]
        connections = {
            0: [1, 2],
            1: [3, 4],
            2: [5, 6],
            3: [7, 8],
            4: [9],
            5: [9, 10],
            6: [11, 12]
        }
        for parent, children in connections.items():
            n[parent].add_child_s([n[child] for child in children])
        
        layout = GraphVisualizer.get_node_layout(n[0])
        self.assert_no_overlapping_layout(layout)


    def test_graph_with_collectables_and_locks(self):
        start = Start()
        key = Key("K0")
        lock = Lock("L0", key_s=key)
        c0 = Collectable("C0")
        c1 = Collectable("C1")
        b = CollectableBarrier("B", collectables=[c0, c1])
        end = End()
        start.add_child_s([key, lock, c0])
        lock.add_child_s([c1, b])
        b.add_child_s(end)

        layout = GraphVisualizer.get_node_layout(start)
        self.assert_no_overlapping_layout(layout)
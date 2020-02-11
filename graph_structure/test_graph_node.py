import unittest
from graph_structure.graph_node import GNode
from graph_structure.graph_node import Start
from graph_structure.graph_node import End
from graph_structure.graph_node import Key
from graph_structure.graph_node import Lock

class TestGraphNode(unittest.TestCase):

    def testNodeToStrings(self):
        start = Start([])
        a = GNode([],[], "a")
        c = End([])
        d = Key([], [], [], "key")
        e = Lock([], [], [], "e")
        start.add_child_s([a])
        start.add_child_s([d])
        self.assertEqual(str(start), "Start(\'Start\', parents=[], children=[\'a\', \'key\'])")
        c.add_parent_s([e, d])
        self.assertEqual(str(c), "End(\'End\', parents=[\'e\', \'key\'], children=[])")
        self.assertEqual(str(d), "Key(\'key\', parents=[], children=[])")
        self.assertEqual(str(e), "Lock(\'e\', parents=[], children=[])")
        self.assertEqual(str(a), "GNode(\'a\', parents=[], children=[])")
        

    def testAddRemoveChild(self):
        a = GNode([], [], "a")
        b = GNode([], [], "b")
        c = GNode([], [], "c")
        d = GNode([], [], "d")
        e = GNode([], [], "e")
        f = GNode([], [], "f")
        return
        # Add single
        a.add_child_s([b])
        self.assertEqual(a.child_s, [b])
        # Add multiple
        a.add_child_s([c, d, e])
        self.assertEqual(a.child_s, [b, c, d, e])
        # Add empty list
        a.add_child_s([])
        self.assertEqual(a.child_s, [b, c, d, e])

        # Remove name not in children
        a.remove_child_s("f")
        self.assertEqual(a.child_s, [b, c, d, e])

        # Remove middle child
        a.remove_child_s("c")
        self.assertEqual(a.child_s, [b, d, e])

        # Remove end child
        a.remove_child_s("e")
        self.assertEqual(a.child_s, [b, d])

        # Remove first child
        a.remove_child_s("b")
        self.assertEqual(a.child_s, [d])

        # Remove last child
        a.remove_child_s("d")
        self.assertEqual(a.child_s, [])


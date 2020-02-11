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

    def testAdd(self):
        l = []
        n1 = GNode([], [], "1")
        n2 = GNode([], [], "2")
        n3 = GNode([], [], "3")
        n4 = GNode([], [], "4")
        n5 = GNode([], [], "5")
        GNode.add(l, [n1])
        self.assertEqual(l, [n1])
        GNode.add(l, [n2, n3, n4, n5])
        self.assertEqual(l, [n1, n2, n3, n4, n5])

    def testRemove(self):
        n1 = GNode([], [], "1")
        n2 = GNode([], [], "2")
        n3 = GNode([], [], "3")
        n4 = GNode([], [], "4")
        n5 = GNode([], [], "5")

        l = [n1, n2, n3, n4, n5]
        GNode.remove(l, n2.name)
        self.assertEqual(l, [n1, n3, n4, n5])
        

    def AddRemoveItem_test(self, node, add_method, remove_method, get_method):
        b = GNode([], [], "b")
        c = GNode([], [], "c")
        d = GNode([], [], "d")
        e = GNode([], [], "e")

        # Add single
        add_method(node, [b])
        self.assertEqual(get_method(node), [b])
        # Add multiple
        add_method(node, [c, d, e])
        self.assertEqual(get_method(node), [b, c, d, e])
        # Add empty list
        add_method(node, [])
        self.assertEqual(get_method(node), [b, c, d, e])

        # Remove name not in children
        remove_method(node, "f")
        self.assertEqual(get_method(node), [b, c, d, e])

        # Remove middle child
        remove_method(node, "c")
        self.assertEqual(get_method(node), [b, d, e])

        # Remove end child
        remove_method(node, "e")
        self.assertEqual(get_method(node), [b, d])

        # Remove first child
        remove_method(node, "b")
        self.assertEqual(get_method(node), [d])

        # Remove last child
        remove_method(node, "d")
        self.assertEqual(get_method(node), [])




    def testAddRemoveChild(self):
        add_method = lambda n, c: n.add_child_s(c)
        remove_method = lambda n, c: n.remove_child_s(c)
        get_method = lambda n: n.child_s
        node = GNode([], [], "node")

        self.AddRemoveItem_test(node, add_method, remove_method, get_method)

    def testAddRemoveParent(self):
        add_method = lambda n, c: n.add_parent_s(c)
        remove_method = lambda n, c: n.remove_parent_s(c)
        get_method = lambda n: n.parent_s
        node = GNode([], [], "node")

        self.AddRemoveItem_test(node, add_method, remove_method, get_method)

    def testAddRemoveKey(self):
        add_method = lambda n, c: n.add_key_s(c)
        remove_method = lambda n, c: n.remove_key_s(c)
        get_method = lambda n: n.key_s
        node = Lock([], [], "lock")

        self.AddRemoveItem_test(node, add_method, remove_method, get_method)

    def testAddRemoveLock(self):
        add_method = lambda n, c: n.add_lock_s(c)
        remove_method = lambda n, c: n.remove_lock_s(c)
        get_method = lambda n: n.lock_s
        node = Key([], [], "key")

        self.AddRemoveItem_test(node, add_method, remove_method, get_method)
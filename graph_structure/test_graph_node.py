import unittest
from graph_structure.graph_node import GNode, Start, End, Key, Lock
from graph_to_level.test_graphs import TestGraphs


class TestGraphNode(unittest.TestCase):

    def test_node_to_strings(self):
        start = Start()
        a = GNode("a")
        c = End()
        d = Key("key")
        e = Lock("e")
        start.add_child_s(a)
        start.add_child_s(d)
        self.assertEqual(str(start), "Start(\'Start\', parents=[], children=[\'a\', \'key\'])")
        c.add_parent_s([e, d])
        self.assertEqual(str(c), "End(\'End\', parents=[\'e\', \'key\'], children=[])")
        self.assertEqual(str(d), "Key(\'key\', parents=[\'Start\'], children=[\'End\'])")
        self.assertEqual(str(e), "Lock(\'e\', parents=[], children=[\'End\'])")
        self.assertEqual(str(a), "GNode(\'a\', parents=[\'Start\'], children=[])")

    def test_add(self):
        n0 = GNode("0")
        n1 = GNode("1")
        n2 = GNode("2")
        n3 = GNode("3")
        n4 = GNode("4")
        n5 = GNode("5")
        GNode._add(n0, [n1], lambda x: x.child_s, lambda x: x.parent_s)
        self.assertEqual(n0.child_s, [n1])
        self.assertEqual(n1.parent_s, [n0])
        GNode._add(n0, [n2, n3, n4, n5], lambda x: x.child_s, lambda x: x.parent_s)
        self.assertEqual(n0.child_s, [n1, n2, n3, n4, n5])
        self.assertEqual(n1.parent_s, [n0])
        self.assertEqual(n2.parent_s, [n0])
        self.assertEqual(n3.parent_s, [n0])
        self.assertEqual(n4.parent_s, [n0])
        self.assertEqual(n5.parent_s, [n0])

    def test_remove(self):
        n1 = GNode("1")
        n2 = GNode("2")
        n3 = GNode("3")
        n4 = GNode("4")
        n5 = GNode("5")

        n0 = GNode("0")
        n0.child_s = [n1, n2, n3, n4, n5]
        n1.parent_s.append(n0)
        n2.parent_s.append(n0)
        n2.parent_s.append(n0)
        n3.parent_s.append(n0)
        n4.parent_s.append(n0)
        n5.parent_s.append(n0)
        GNode._remove(n0, n2.name, lambda x: x.child_s, lambda x: x.parent_s)
        self.assertEqual(n0.child_s, [n1, n3, n4, n5])
        self.assertEqual(n1.parent_s, [n0])
        self.assertEqual(n2.parent_s, [])
        self.assertEqual(n3.parent_s, [n0])
        self.assertEqual(n4.parent_s, [n0])
        self.assertEqual(n5.parent_s, [n0])
        

    def add_remove_item_test(self, node, add_method, remove_method, get_method, get_inverse_method, constructor_method):
        b = constructor_method("b")
        c = constructor_method("c")
        d = constructor_method("d")
        e = constructor_method("e")
        f = constructor_method("f")

        # Add single
        add_method(node, b)
        self.assertEqual(get_method(node), [b])
        self.assertEqual(get_inverse_method(b), [node])
        self.assertEqual(get_inverse_method(c), [])
        self.assertEqual(get_inverse_method(d), [])
        self.assertEqual(get_inverse_method(e), [])
        self.assertEqual(get_inverse_method(f), [])
        # Add single, array
        add_method(node, [c])
        self.assertEqual(get_method(node), [b, c])
        self.assertEqual(get_inverse_method(b), [node])
        self.assertEqual(get_inverse_method(c), [node])
        self.assertEqual(get_inverse_method(d), [])
        self.assertEqual(get_inverse_method(e), [])
        self.assertEqual(get_inverse_method(f), [])
        # Add multiple
        add_method(node, [d, e, f])
        self.assertEqual(get_method(node), [b, c, d, e, f])
        self.assertEqual(get_inverse_method(b), [node])
        self.assertEqual(get_inverse_method(c), [node])
        self.assertEqual(get_inverse_method(d), [node])
        self.assertEqual(get_inverse_method(e), [node])
        self.assertEqual(get_inverse_method(f), [node])
        # Add empty list
        add_method(node, [])
        self.assertEqual(get_method(node), [b, c, d, e, f])

        # Remove name not in children
        remove_method(node, "g")
        self.assertEqual(get_method(node), [b, c, d, e, f])
        self.assertEqual(get_inverse_method(b), [node])
        self.assertEqual(get_inverse_method(c), [node])
        self.assertEqual(get_inverse_method(d), [node])
        self.assertEqual(get_inverse_method(e), [node])
        self.assertEqual(get_inverse_method(f), [node])

        # Remove multiple, remove middle
        remove_method(node, ["c", "d"])
        self.assertEqual(get_method(node), [b, e, f])
        self.assertEqual(get_inverse_method(b), [node])
        self.assertEqual(get_inverse_method(c), [])
        self.assertEqual(get_inverse_method(d), [])
        self.assertEqual(get_inverse_method(e), [node])
        self.assertEqual(get_inverse_method(f), [node])

        # Remove end child
        remove_method(node, "f")
        self.assertEqual(get_method(node), [b, e])
        self.assertEqual(get_inverse_method(b), [node])
        self.assertEqual(get_inverse_method(c), [])
        self.assertEqual(get_inverse_method(d), [])
        self.assertEqual(get_inverse_method(e), [node])
        self.assertEqual(get_inverse_method(f), [])

        # Remove first child, remove single in array
        remove_method(node, ["b"])
        self.assertEqual(get_method(node), [e])
        self.assertEqual(get_inverse_method(b), [])
        self.assertEqual(get_inverse_method(c), [])
        self.assertEqual(get_inverse_method(d), [])
        self.assertEqual(get_inverse_method(e), [node])
        self.assertEqual(get_inverse_method(f), [])

        # Remove final child
        remove_method(node, "e")
        self.assertEqual(get_method(node), [])
        self.assertEqual(get_inverse_method(b), [])
        self.assertEqual(get_inverse_method(c), [])
        self.assertEqual(get_inverse_method(d), [])
        self.assertEqual(get_inverse_method(e), [])
        self.assertEqual(get_inverse_method(f), [])




    def test_add_remove_child(self):
        add_method = lambda n, c: n.add_child_s(c)
        remove_method = lambda n, c: n.remove_child_s(c)
        get_method = lambda n: n.child_s
        get_inverse_method = lambda n: n.parent_s
        constructor_method = lambda x: GNode(x)
        node = GNode("node")

        self.add_remove_item_test(node, add_method, remove_method, get_method, get_inverse_method, constructor_method)

    def test_add_remove_parent(self):
        add_method = lambda n, c: n.add_parent_s(c)
        remove_method = lambda n, c: n.remove_parent_s(c)
        get_method = lambda n: n.parent_s
        get_inverse_method = lambda n: n.child_s
        constructor_method = lambda x: GNode(x)
        node = GNode("node")

        self.add_remove_item_test(node, add_method, remove_method, get_method, get_inverse_method, constructor_method)

    def test_add_remove_key(self):
        add_method = lambda n, c: n.add_key_s(c)
        remove_method = lambda n, c: n.remove_key_s(c)
        get_method = lambda n: n.key_s
        get_inverse_method = lambda n: n.lock_s
        constructor_method = lambda x: Key(x)
        node = Lock("lock")

        self.add_remove_item_test(node, add_method, remove_method, get_method, get_inverse_method, constructor_method)

    def test_add_remove_lock(self):
        add_method = lambda n, c: n.add_lock_s(c)
        remove_method = lambda n, c: n.remove_lock_s(c)
        get_method = lambda n: n.lock_s
        get_inverse_method = lambda n: n.key_s
        constructor_method = lambda x: Lock(x)
        node = Key("key")

        self.add_remove_item_test(node, add_method, remove_method, get_method, get_inverse_method, constructor_method)


    def test_traverse_depth_first(self):
        node, all_nodes = TestGraphs.get_man_graph()
        visited_expected = ["Start", "b", "e", "c", "End", "g", "h", "i", "d"]

        def visit_method(node, visited_nodes):
            visited.append(node)

        def will_traverse_method(node, child, visited_nodes):
            return True

        # Traverse with no will_traverse_method specified
        visited = []
        GNode.traverse_nodes_depth_first(node, visit_method)
        visited_names = [x.name for x in visited]
        self.assertEqual(visited_names, visited_expected)

        # Traverse with will_traverse_method that allows all nodes
        visited = []
        GNode.traverse_nodes_depth_first(node, visit_method, will_traverse_method)
        visited_names = [x.name for x in visited]
        self.assertEqual(visited_names, visited_expected)
    
        # Traverse with will_traverse_method that ignores node "c"
        def will_traverse_method2(node, child, visited_nodes):
            return child.name != "c"
        visited = []
        GNode.traverse_nodes_depth_first(node, visit_method, will_traverse_method2)
        visited_names = [x.name for x in visited]
        visited_expected = ["Start", "b", "e", "d"]
        self.assertEqual(visited_names, visited_expected)


    #    S-------c---E
    #   / \     /|\
    #  b   d   / | \
    #  |      h--i  g
    #  e
    def test_traverse_breadth_first(self):
        node, all_nodes = TestGraphs.get_man_graph()
        visited_expected = ["Start", "b", "c", "d", "e", "End", "g", "h", "i"]

        def visit_method(node, visited_nodes):
            visited.append(node)

        def will_traverse_method(node, visited_nodes):
            return True

        # Traverse with no will_traverse_method specified
        visited = []
        GNode.traverse_nodes_breadth_first(node, visit_method)
        visited_names = [x.name for x in visited]
        self.assertEqual(visited_names, visited_expected)

        # Traverse with will_traverse_method that allows all nodes
        visited = []
        GNode.traverse_nodes_breadth_first(node, visit_method, will_traverse_method)
        visited_names = [x.name for x in visited]
        self.assertEqual(visited_names, visited_expected)
    
        # Traverse with will_traverse_method that ignores node "c"
        def will_traverse_method2(node, visited_nodes):
            return node.name != "c"
        visited = []
        GNode.traverse_nodes_breadth_first(node, visit_method, will_traverse_method2)
        visited_names = [x.name for x in visited]
        visited_expected = ["Start", "b", "d", "e"]
        self.assertEqual(visited_names, visited_expected)

        

    def test_find_all_nodes(self):
        a, all_nodes = TestGraphs.get_man_graph()
        nodes = GNode.find_all_nodes(a)
        self.assertEqual(set(nodes), all_nodes)

        a, all_nodes = TestGraphs.get_house_graph()
        nodes = GNode.find_all_nodes(a)
        self.assertEqual(set(nodes), all_nodes)

        a, all_nodes = TestGraphs.get_graph_b()
        nodes = GNode.find_all_nodes(a)
        self.assertEqual(set(nodes), all_nodes)

        a, all_nodes = TestGraphs.get_graph_a()
        nodes = GNode.find_all_nodes(a)
        self.assertEqual(set(nodes), all_nodes)

        a, all_nodes = TestGraphs.get_triangle_graph()
        nodes = GNode.find_all_nodes(a)
        self.assertEqual(set(nodes), all_nodes)

    def test_mutable_default_argument_bug(self):
        gnode1 = GNode("")
        gnode2 = GNode("")
        bad_node0 = GNode("BadNode0")
        gnode1.add_child_s(bad_node0)
        self.assertEqual(len(gnode2.child_s), 0)

        start1 = Start()
        start2 = Start()
        bad_node1 = GNode("BadNode1")
        start1.add_child_s(bad_node1)
        self.assertEqual(len(start2.child_s), 0)

        end1 = End()
        end2 = End()
        bad_node2 = GNode("BadNode2")
        end1.add_parent_s(bad_node2)
        self.assertEqual(len(end2.parent_s), 0)

        key1 = Key()
        key2 = Key()
        bad_node3 = GNode("BadNode3")
        key1.add_child_s(bad_node3)
        bad_node4 = GNode("BadNode4")
        key1.add_parent_s(bad_node4)
        self.assertEqual(len(key2.child_s), 0)
        self.assertEqual(len(key2.parent_s), 0)

        lock1 = Lock()
        lock2 = Lock()
        bad_node5 = GNode("BadNode5")
        lock1.add_child_s(bad_node5)
        bad_node6 = GNode("BadNode6")
        lock1.add_parent_s(bad_node6)
        self.assertEqual(len(lock2.child_s), 0)
        self.assertEqual(len(lock2.parent_s), 0)

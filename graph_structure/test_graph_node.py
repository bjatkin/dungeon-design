import unittest
from graph_structure.graph_node import Node, GNode, Start, End, Key, Lock
from graph_to_level.test_graphs import TestGraphs


class TestGraphNode(unittest.TestCase):

    def test_equality(self):
        a = GNode("a")
        b = GNode("b", a)
        self.assertEqual(a, a)
        self.assertEqual(b, b)
        self.assertNotEqual(a, b)
        pass

    def is_list_permutation_in_string(self, input_string, format_string, list_values):
        permutated_strings = []
        permutated_strings.append(format_string.format(list_values))
        list_values.reverse()
        permutated_strings.append(format_string.format(list_values))
        return input_string in permutated_strings



    def test_node_to_strings(self):
        start = Start()
        a = GNode("a")
        c = End()
        d = Key("key")
        e = Lock("e")
        start.add_child_s(a)
        start.add_child_s(d)
        d.add_lock_s(e)
        self.assertTrue(self.is_list_permutation_in_string(str(start), "Start(\'Start\', children={})", ["a", "key"]))
        c.add_parent_s([e, d])
        self.assertTrue(self.is_list_permutation_in_string(str(c), "End(\'End\', parents={})", ["e", "key"]))
        self.assertTrue(self.is_list_permutation_in_string(str(d), "Key(\'key\', parents=[\'Start\'], children={}, locks=[\'e\'])", ["e", "End"]))
        self.assertEqual(str(e), "Lock(\'e\', parents=[\'key\'], children=[\'End\'], keys=[\'key\'])")
        self.assertEqual(str(a), "GNode(\'a\', parents=[\'Start\'], children=[])")

    def test_add(self):
        n0 = GNode("0")
        n1 = GNode("1")
        n2 = GNode("2")
        n3 = GNode("3")
        n4 = GNode("4")
        n5 = GNode("5")
        Node._add(n0, [n1], lambda x: x.child_s, lambda x: x.parent_s)
        self.assertEqual(n0.child_s, {n1})
        self.assertEqual(n1.parent_s, {n0})
        Node._add(n0, [n2, n3, n4, n5], lambda x: x.child_s, lambda x: x.parent_s)
        self.assertEqual(n0.child_s, {n1, n2, n3, n4, n5})
        self.assertEqual(n1.parent_s, {n0})
        self.assertEqual(n2.parent_s, {n0})
        self.assertEqual(n3.parent_s, {n0})
        self.assertEqual(n4.parent_s, {n0})
        self.assertEqual(n5.parent_s, {n0})

    def test_remove_by_name(self):
        n1 = GNode("1")
        n2 = GNode("2")
        n3 = GNode("3")
        n4 = GNode("4")
        n5 = GNode("5")

        n0 = GNode("0")
        n0.child_s = {n1, n2, n3, n4, n5}
        n1.parent_s.add(n0)
        n2.parent_s.add(n0)
        n2.parent_s.add(n0)
        n3.parent_s.add(n0)
        n4.parent_s.add(n0)
        n5.parent_s.add(n0)
        Node._remove_by_name(n0, n2.name, lambda x: x.child_s, lambda x: x.parent_s)
        self.assertEqual(n0.child_s, {n1, n3, n4, n5})
        self.assertEqual(n1.parent_s, {n0})
        self.assertEqual(n2.parent_s, set())
        self.assertEqual(n3.parent_s, {n0})
        self.assertEqual(n4.parent_s, {n0})
        self.assertEqual(n5.parent_s, {n0})
        

    def add_remove_item_test(self, node, add_method, remove_method, get_method, get_inverse_method, constructor_method, should_remove_by_name):
        b = constructor_method("b")
        c = constructor_method("c")
        d = constructor_method("d")
        e = constructor_method("e")
        f = constructor_method("f")

        # Can't add self as a node
        add_method(node, node)
        self.assertEqual(get_method(node), set())

        # Add single
        add_method(node, b)
        self.assertEqual(get_method(node), {b})
        self.assertEqual(get_inverse_method(b), {node})
        self.assertEqual(get_inverse_method(c), set())
        self.assertEqual(get_inverse_method(d), set())
        self.assertEqual(get_inverse_method(e), set())
        self.assertEqual(get_inverse_method(f), set())
        # Add single value multiple times
        add_method(node, [c, c, c])
        add_method(node, [c])
        self.assertEqual(get_method(node), {b, c})
        self.assertEqual(get_inverse_method(b), {node})
        self.assertEqual(get_inverse_method(c), {node})
        self.assertEqual(get_inverse_method(d), set())
        self.assertEqual(get_inverse_method(e), set())
        self.assertEqual(get_inverse_method(f), set())
        # Add multiple
        add_method(node, [d, e, f])
        self.assertEqual(get_method(node), {b, c, d, e, f})
        self.assertEqual(get_inverse_method(b), {node})
        self.assertEqual(get_inverse_method(c), {node})
        self.assertEqual(get_inverse_method(d), {node})
        self.assertEqual(get_inverse_method(e), {node})
        self.assertEqual(get_inverse_method(f), {node})
        # Add empty list
        add_method(node, [])
        self.assertEqual(get_method(node), {b, c, d, e, f})

        # Remove name not in children
        if should_remove_by_name:
            remove_method(node, "g")
        else:
            g = constructor_method("g")
            remove_method(node, g)

        self.assertEqual(get_method(node), {b, c, d, e, f})
        self.assertEqual(get_inverse_method(b), {node})
        self.assertEqual(get_inverse_method(c), {node})
        self.assertEqual(get_inverse_method(d), {node})
        self.assertEqual(get_inverse_method(e), {node})
        self.assertEqual(get_inverse_method(f), {node})

        # Remove multiple, remove middle
        if should_remove_by_name:
            remove_method(node, ["c", "d"])
        else:
            remove_method(node, [c, d])

        self.assertEqual(get_method(node), {b, e, f})
        self.assertEqual(get_inverse_method(b), {node})
        self.assertEqual(get_inverse_method(c), set())
        self.assertEqual(get_inverse_method(d), set())
        self.assertEqual(get_inverse_method(e), {node})
        self.assertEqual(get_inverse_method(f), {node})

        # Remove end child
        if should_remove_by_name:
            remove_method(node, "f")
        else:
            remove_method(node, f)

        self.assertEqual(get_method(node), {b, e})
        self.assertEqual(get_inverse_method(b), {node})
        self.assertEqual(get_inverse_method(c), set())
        self.assertEqual(get_inverse_method(d), set())
        self.assertEqual(get_inverse_method(f), set())
        self.assertEqual(get_inverse_method(e), {node})

        # Remove first child, remove single in array
        if should_remove_by_name:
            remove_method(node, ["b"])
        else:
            remove_method(node, [b])

        self.assertEqual(get_method(node), {e})
        self.assertEqual(get_inverse_method(b), set())
        self.assertEqual(get_inverse_method(c), set())
        self.assertEqual(get_inverse_method(d), set())
        self.assertEqual(get_inverse_method(f), set())
        self.assertEqual(get_inverse_method(e), {node})

        # Remove final child
        if should_remove_by_name:
            remove_method(node, "e")
        else:
            remove_method(node, e)

        self.assertEqual(get_method(node), set())
        self.assertEqual(get_inverse_method(b), set())
        self.assertEqual(get_inverse_method(c), set())
        self.assertEqual(get_inverse_method(d), set())
        self.assertEqual(get_inverse_method(e), set())
        self.assertEqual(get_inverse_method(f), set())





    def test_add_remove_child(self):
        add_method = lambda n, c: n.add_child_s(c)
        remove_method_by_name = lambda n, c: n.remove_child_s_by_name(c)
        remove_method = lambda n, c: n.remove_child_s(c)
        get_method = lambda n: n.child_s
        get_inverse_method = lambda n: n.parent_s
        constructor_method = lambda x: GNode(x)
        node = GNode("node")

        self.add_remove_item_test(node, add_method, remove_method_by_name, get_method, get_inverse_method, constructor_method, True)
        self.add_remove_item_test(node, add_method, remove_method, get_method, get_inverse_method, constructor_method, False)

    def test_add_remove_parent(self):
        add_method = lambda n, c: n.add_parent_s(c)
        remove_method_by_name = lambda n, c: n.remove_parent_s_by_name(c)
        remove_method = lambda n, c: n.remove_parent_s(c)
        get_method = lambda n: n.parent_s
        get_inverse_method = lambda n: n.child_s
        constructor_method = lambda x: GNode(x)
        node = GNode("node")

        self.add_remove_item_test(node, add_method, remove_method_by_name, get_method, get_inverse_method, constructor_method, True)
        self.add_remove_item_test(node, add_method, remove_method, get_method, get_inverse_method, constructor_method, False)

    def test_add_remove_key(self):
        add_method = lambda n, c: n.add_key_s(c)
        remove_method_by_name = lambda n, c: n.remove_key_s_by_name(c)
        remove_method = lambda n, c: n.remove_key_s(c)
        get_method = lambda n: n.key_s
        get_inverse_method = lambda n: n.lock_s
        constructor_method = lambda x: Key(x)
        node = Lock("lock")

        self.add_remove_item_test(node, add_method, remove_method_by_name, get_method, get_inverse_method, constructor_method, True)
        self.add_remove_item_test(node, add_method, remove_method, get_method, get_inverse_method, constructor_method, False)

    def test_add_remove_lock(self):
        add_method = lambda n, c: n.add_lock_s(c)
        remove_method_by_name = lambda n, c: n.remove_lock_s_by_name(c)
        remove_method = lambda n, c: n.remove_lock_s(c)
        get_method = lambda n: n.lock_s
        get_inverse_method = lambda n: n.key_s
        constructor_method = lambda x: Lock(x)
        node = Key("key")

        self.add_remove_item_test(node, add_method, remove_method_by_name, get_method, get_inverse_method, constructor_method, True)
        self.add_remove_item_test(node, add_method, remove_method, get_method, get_inverse_method, constructor_method, False)


    def test_traverse_depth_first(self):
        node, all_nodes = TestGraphs.get_man_graph()
        visited_expected = ["Start", "b", "e", "c", "End", "g", "h", "i", "d"]

        def visit_method(node, visited_nodes):
            visited.append(node)

        def will_traverse_method(node, child, visited_nodes):
            return True

        # Traverse with no will_traverse_method specified
        visited = []
        Node.traverse_nodes_depth_first(node, visit_method)
        visited_names = [x.name for x in visited]
        self.assertTrue(self.assert_ordered(visited_names, [
            ("Start", ["b", "c", "d", "e", "End", "g", "h", "i"]),
            ("b", ["e"]),
            ("c", ["End", "g", "h", "i"]),
            ("d", []),
            ("h", []),
            ("g", []),
            ("e", []),
            ("End", []) ]))

        # Traverse with will_traverse_method that allows all nodes
        visited = []
        Node.traverse_nodes_depth_first(node, visit_method, will_traverse_method)
        visited_names = [x.name for x in visited]
        self.assertTrue(self.assert_ordered(visited_names, [
            ("Start", ["b", "c", "d", "e", "End", "g", "h", "i"]),
            ("b", ["e"]),
            ("c", ["End", "g", "h", "i"]),
            ("d", []),
            ("h", []),
            ("g", []),
            ("e", []),
            ("End", []) ]))
    
        # Traverse with will_traverse_method that ignores node "c"
        def will_traverse_method2(node, child, visited_nodes):
            return child.name != "c"
        visited = []
        Node.traverse_nodes_depth_first(node, visit_method, will_traverse_method2)
        visited_names = [x.name for x in visited]
        self.assertTrue(self.assert_ordered(visited_names, [
            ("Start", ["b", "d", "e"]),
            ("b", ["e"]),
            ("d", []),
            ("e", []) ]))
        self.assertFalse(self.are_values_in_list(visited_names, ["c", "g", "h", "i"]))


    def are_values_in_list(self, list_a, values_not_in_list):
        is_value_in_list = [value in list_a for value in values_not_in_list]
        return any(is_value_in_list)


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
        Node.traverse_nodes_breadth_first(node, visit_method)
        visited_names = [x.name for x in visited]
        self.assertTrue(self.assert_ordered(visited_names, [
            ("Start", ["b", "c", "d", "e", "End", "g", "h", "i"]),
            ("b", ["e", "End", "g", "h", "i"]),
            ("c", ["e", "End", "g", "h", "i"]),
            ("d", ["e", "End", "g", "h", "i"]),
            ("h", []),
            ("g", []),
            ("e", []),
            ("End", []) ]))

        # Traverse with will_traverse_method that allows all nodes
        visited = []
        Node.traverse_nodes_breadth_first(node, visit_method, will_traverse_method)
        visited_names = [x.name for x in visited]
        self.assertTrue(self.assert_ordered(visited_names, [
            ("Start", ["b", "c", "d", "e", "End", "g", "h", "i"]),
            ("b", ["e", "End", "g", "h", "i"]),
            ("c", ["e", "End", "g", "h", "i"]),
            ("d", ["e", "End", "g", "h", "i"]),
            ("h", []),
            ("g", []),
            ("e", []),
            ("End", []) ]))
    
        # Traverse with will_traverse_method that ignores node "c"
        def will_traverse_method2(node, visited_nodes):
            return node.name != "c"
        visited = []
        Node.traverse_nodes_breadth_first(node, visit_method, will_traverse_method2)
        visited_names = [x.name for x in visited]
        visited_expected = ["Start", "b", "d", "e"]
        self.assertTrue(self.assert_ordered(visited_names, [
            ("Start", ["b", "d", "e"]),
            ("b", ["e"]),
            ("d", []),
            ("e", []) ]))

        self.assertFalse(self.are_values_in_list(visited_names, ["c", "g", "h", "i"]))

        

    def test_find_all_nodes(self):
        a, all_nodes = TestGraphs.get_man_graph()
        nodes = Node.find_all_nodes(a)
        self.assertEqual(set(nodes), all_nodes)

        a, all_nodes = TestGraphs.get_house_graph()
        nodes = Node.find_all_nodes(a)
        self.assertEqual(set(nodes), all_nodes)

        a, all_nodes = TestGraphs.get_graph_b()
        nodes = Node.find_all_nodes(a)
        self.assertEqual(set(nodes), all_nodes)

        a, all_nodes = TestGraphs.get_graph_a()
        nodes = Node.find_all_nodes(a)
        self.assertEqual(set(nodes), all_nodes)

        a, all_nodes = TestGraphs.get_triangle_graph()
        nodes = Node.find_all_nodes(a)
        self.assertEqual(set(nodes), all_nodes)

    def assert_ordered(self, list_a, orderings):
        for ordering in orderings:
            if ordering[0] not in list_a:
                return False

            index = list_a.index(ordering[0])
            after_items = list_a[index + 1:]
            for item in ordering[1]:
                if item not in after_items:
                    return False
        return True
        

    def test_find_all_nodes_topological_sort(self):
        top_sort = "topological-sort"

        n0 = GNode("0")
        n1 = GNode("1")
        n2 = GNode("2")
        n3 = GNode("3")
        n4 = GNode("4")
        n5 = GNode("5")
        n5.add_child_s([n0, n2, n4])
        n2.add_child_s(n3)
        n3.add_child_s(n1)
        n4.add_child_s([n0, n1])
        nodes = Node.find_all_nodes(n5, method=top_sort)
        self.assertTrue(self.assert_ordered(nodes, [
            (n5, [n4,n3,n2,n1,n0]), 
            (n4, [n0, n1]),
            (n2, [n3, n1]),
            (n3, [n1]),
            (n0, []),
            (n1, []) ]))

        n0 = GNode("0")
        n1 = GNode("1")
        n2 = GNode("2")
        n3 = GNode("3")
        n4 = GNode("4")
        n5 = GNode("5")
        n0.add_child_s([n1, n2, n3])
        n1.add_child_s(n4)
        n2.add_child_s(n5)
        n3.add_child_s(n1)
        n4.add_child_s(n2)
        nodes = Node.find_all_nodes(n0, method=top_sort)
        self.assertTrue(self.assert_ordered(nodes, [
            (n0, [n1, n2, n3, n4, n5]),
            (n1, [n4, n2, n5]),
            (n2, [n5]),
            (n3, [n1, n4, n2, n5]),
            (n4, [n2, n5]),
            (n5, []) ]))



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


    def test_node_create_params(self):
        n0 = GNode("n0")
        n2 = GNode("n2")
        n1 = GNode("n1", n0, n2)
        n3 = GNode("n3", [n0], [n2])
        start = Start(n0)
        end = End(n2)
        key1 = Key("key1", n0, n1)
        lock1 = Lock("lock1", n2, end, key1)
        lock2 = Lock("lock1", n2, end)
        key2 = Key("key1", n0, n1, lock2)

        self.assertEqual(start.parent_s, set())
        self.assertEqual(start.child_s, {n0})
        self.assertEqual(n0.parent_s, {start})
        self.assertEqual(n0.child_s, {n1, n3, key1, key2})
        self.assertEqual(n1.parent_s, {n0, key1, key2})
        self.assertEqual(n1.child_s, {n2})
        self.assertEqual(n2.parent_s, {n1, n3})
        self.assertEqual(n2.child_s, {end, lock1, lock2})
        self.assertEqual(n3.parent_s, {n0})
        self.assertEqual(n3.child_s, {n2})
        self.assertEqual(key1.parent_s, {n0})
        self.assertEqual(key1.child_s, {n1, lock1})
        self.assertEqual(key1.lock_s, {lock1})
        self.assertEqual(lock1.parent_s, {n2, key1})
        self.assertEqual(lock1.child_s, {end})
        self.assertEqual(lock1.key_s, {key1})
        self.assertEqual(key2.parent_s, {n0})
        self.assertEqual(key2.child_s, {n1, lock2})
        self.assertEqual(key2.lock_s, {lock2})
        self.assertEqual(lock2.parent_s, {n2, key2})
        self.assertEqual(lock2.child_s, {end})
        self.assertEqual(lock2.key_s, {key2})
        self.assertEqual(end.parent_s, {n2, lock1, lock2})
        self.assertEqual(end.child_s, set())

    def test_topological_sort_bug(self):
        start = Start()
        key = Key("key")
        lock = Lock("lock")
        end = End()
        start.add_child_s(key)
        key.add_lock_s(lock)
        lock.add_child_s(end)

        nodes = Node.find_all_nodes(start, method="topological-sort")
        self.assertEqual(nodes, [start, key, lock, end])

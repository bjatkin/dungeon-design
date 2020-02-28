import numpy as np

class GNode(object):
    def __init__(self, name="", parent_s=None, child_s=None):
        self.child_s = []
        self.parent_s = []

        if child_s is not None:
            self.add_child_s(child_s)
        if parent_s is not None:
            self.add_parent_s(parent_s)

        self.name = name


    # traversal_order=['preorder','postorder']
    @staticmethod
    def traverse_nodes_depth_first(node, visit_method, will_traverse_method = lambda node, child, visited_nodes: True, traversal_order='preorder'):
        visited_nodes = set()
        GNode._traverse_nodes_depth_first(node, visit_method, will_traverse_method, visited_nodes, traversal_order)


    @staticmethod
    def _traverse_nodes_depth_first(node, visit_method, will_traverse_method, visited_nodes, traversal_order):
        visited_nodes.add(node)
        if traversal_order == 'preorder':
            visit_method(node, visited_nodes)

        for child in node.child_s:
            if child not in visited_nodes:
                will_traverse = will_traverse_method(node, child, visited_nodes)
                if will_traverse:
                    GNode._traverse_nodes_depth_first(child, visit_method, will_traverse_method, visited_nodes, traversal_order)

        if traversal_order == 'postorder':
            visit_method(node, visited_nodes)


    @staticmethod
    def traverse_nodes_breadth_first(node, visit_method, will_traverse_method = lambda node, visited_nodes: True):
        visited_nodes = set()
        queue = []
        queue.append(node)
        while (len(queue) > 0):
            node = queue.pop(0)
            if node not in visited_nodes:
                will_traverse = will_traverse_method(node, visited_nodes)
                if will_traverse:
                    visited_nodes.add(node)
                    visit_method(node, visited_nodes)
                    for child in node.child_s:
                        queue.append(child)


    # method=['depth-first','breadth-first','topological-sort']
    @staticmethod
    def find_all_nodes(node, method="depth-first"):
        visited = []


        def visit_method(node, visited_nodes):
            nonlocal visited
            visited.append(node)


        if method == "depth-first":
            GNode.traverse_nodes_depth_first(node, visit_method)
        elif method == "breadth-first":
            GNode.traverse_nodes_breadth_first(node, visit_method)
        elif method == "topological-sort":
            GNode.traverse_nodes_depth_first(node, visit_method, traversal_order='postorder')
            visited.reverse()

        return visited


    @staticmethod
    def _listify(items):
        if not isinstance(items, list):
            items = [items]
        return items


    @staticmethod
    def _add(_self, items, get_self_list_method, get_items_list_method):
        items = GNode._listify(items)
        get_self_list_method(_self).extend(items)
        for item in items:
            get_items_list_method(item).append(_self)


    @staticmethod
    def _remove(_self, item_names, get_self_list_method, get_items_list_method):
        item_names = GNode._listify(item_names)
        items = [item for item in get_self_list_method(_self) if item.name in item_names]
        get_self_list_method(_self)[:] = [item for item in get_self_list_method(_self) if item.name not in item_names]
        for item in items:
            get_items_list_method(item)[:] = [item for item in get_items_list_method(item) if item.name != _self.name]


    def add_child_s(self, child_s):
        # Instead of having the code to add a child/parent/key here, we call a static method
        # passing it the list that we want to modify.
        GNode._add(self, child_s, lambda x: x.child_s, lambda x: x.parent_s)
    

    def remove_child_s(self, child_name_s):
        GNode._remove(self, child_name_s, lambda x: x.child_s, lambda x: x.parent_s)
    

    def add_parent_s(self, parent_s):
        GNode._add(self, parent_s, lambda x: x.parent_s, lambda x: x.child_s)
    

    def remove_parent_s(self, parent_name_s):
        GNode._remove(self, parent_name_s, lambda x: x.parent_s, lambda x: x.child_s)


    def __repr__(self):
        parent_names = [n.name for n in self.parent_s]
        child_names = [n.name for n in self.child_s]
        class_name = type(self).__name__
        string = "{}(\'{}\', parents={}, children={})".format(class_name, self.name, parent_names, child_names)
        return string


    def __eq__(self, other): 
        return str(self) == str(other)


    def __hash__(self):
        return hash(str(self))



class Start(GNode):
    def __init__(self, child_s=None):
        super(Start, self).__init__("Start", [], child_s)


class Key(GNode):
    def __init__(self, name="", parent_s=None, child_s=None, lock_s=None):
        self.lock_s = []
        if lock_s is not None:
            self.add_lock_s(lock_s)

        super(Key, self).__init__(name, parent_s, child_s)
    

    def add_lock_s(self, lock_s):
        GNode._add(self, lock_s, lambda x: x.lock_s, lambda x: x.key_s)
    

    def remove_lock_s(self, lock_name_s):
        GNode._remove(self, lock_name_s, lambda x: x.lock_s, lambda x: x.key_s)
        

class Lock(GNode):
    def __init__(self, name="", parent_s=None, child_s=None, key_s=None):
        self.key_s = []
        if key_s is not None:
            self.add_key_s(key_s)

        super(Lock, self).__init__(name, parent_s, child_s)
    
    def add_key_s(self, key_s):
        GNode._add(self, key_s, lambda x: x.key_s, lambda x: x.lock_s)
    
    def remove_key_s(self, key_name_s):
        GNode._remove(self, key_name_s, lambda x: x.key_s, lambda x: x.lock_s)


class End(GNode):
    def __init__(self, parent_s=None):
        if parent_s == None:
            parent_s = []

        super(End, self).__init__("End", parent_s, [])
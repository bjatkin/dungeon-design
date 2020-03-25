import numpy as np
import uuid

class Node(object):
    def __init__(self, name=None):
        if name is None:
            self.name = str(uuid.uuid4())
        else:
            self.name = name

        self.adjacent_nodes = set()


    def add_adjacent_nodes(self, nodes):
        Node._add(self, nodes, lambda x: x.adjacent_nodes, lambda x: x.adjacent_nodes)


    def remove_adjacent_nodes(self, nodes):
        Node._remove(self, nodes, lambda x: x.adjacent_nodes, lambda x: x.adjacent_nodes)


    def _get_to_string_properties(self):
        return { 
                "adjacents": [n.name for n in self.adjacent_nodes],
            }


    def __repr__(self):
        properties = self._get_to_string_properties()
        class_name = type(self).__name__
        string = "{}(\'{}\'".format(class_name, self.name)
        for prop_name, prop_value in properties.items():
            string += ", {}={}".format(prop_name, prop_value)
        string += ")"
        return string


    def __eq__(self, other): 
        self_class_name = type(self).__name__
        other_class_name = type(other).__name__

        return (self_class_name == other_class_name and self.name == other.name)


    def __hash__(self):
        self_class_name = type(self).__name__
        if hasattr(self, 'name'):
            return hash(self.name + self_class_name)
        else:
            return hash(id(self))


    # traversal_order=['preorder','postorder']
    @staticmethod
    def traverse_nodes_depth_first(node, visit_method, will_traverse_method = lambda node, child, visited_nodes: True, traversal_order='preorder'):
        visited_nodes = set()
        Node._traverse_nodes_depth_first(node, visit_method, will_traverse_method, visited_nodes, traversal_order)


    @staticmethod
    def _traverse_nodes_depth_first(node, visit_method, will_traverse_method, visited_nodes, traversal_order):
        visited_nodes.add(node)
        if traversal_order == 'preorder':
            visit_method(node, visited_nodes)

        for child in node.adjacent_nodes:
            if child not in visited_nodes:
                will_traverse = will_traverse_method(node, child, visited_nodes)
                if will_traverse:
                    Node._traverse_nodes_depth_first(child, visit_method, will_traverse_method, visited_nodes, traversal_order)

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
                    for child in node.adjacent_nodes:
                        queue.append(child)


    # method=['depth-first','breadth-first','topological-sort']
    @staticmethod
    def find_all_nodes(node, method="depth-first"):
        visited = []

        def visit_method(node, visited_nodes):
            nonlocal visited
            visited.append(node)

        if method == "depth-first":
            Node.traverse_nodes_depth_first(node, visit_method)
        elif method == "breadth-first":
            Node.traverse_nodes_breadth_first(node, visit_method)
        elif method == "topological-sort":
            Node.traverse_nodes_depth_first(node, visit_method, traversal_order='postorder')
            visited.reverse()

        return visited


    @staticmethod
    def _setify(items):
        if isinstance(items, list):
            items = set(items)
        elif not isinstance(items, set):
            items = set([items])
        return items


    @staticmethod
    def _add(_self, items, get_self_list_method, get_items_list_method):
        items = Node._setify(items)
        if _self in items:
            items.remove(_self)
        
        get_self_list_method(_self).update(items)
        for item in items:
            get_items_list_method(item).add(_self)


    @staticmethod
    def _remove_by_name(_self, item_names, get_self_list_method, get_items_list_method):
        item_names = Node._setify(item_names)
        items = [item for item in get_self_list_method(_self) if item.name in item_names]
        Node._remove(_self, items, get_self_list_method, get_items_list_method)

    @staticmethod
    def _remove(_self, items, get_self_list_method, get_items_list_method):
        items = Node._setify(items)
        for item in items:
            items_list = get_items_list_method(item)
            if _self in items_list:
                items_list.remove(_self)

        self_list = get_self_list_method(_self)
        self_list -= items



class GNode(Node):
    def __init__(self, name=None, parent_s=None, child_s=None):
        super(GNode, self).__init__(name)
        self.child_s = self.adjacent_nodes
        self.parent_s = set()

        if child_s is not None:
            self.add_child_s(child_s)
        if parent_s is not None:
            self.add_parent_s(parent_s)


    def add_child_s(self, child_s):
        # Instead of having the code to add a child/parent/key here, we call a static method
        # passing it the list that we want to modify.
        Node._add(self, child_s, lambda x: x.child_s, lambda x: x.parent_s)
    

    def remove_child_s_by_name(self, child_name_s):
        Node._remove_by_name(self, child_name_s, lambda x: x.child_s, lambda x: x.parent_s)
    

    def remove_child_s(self, child_s):
        Node._remove(self, child_s, lambda x: x.child_s, lambda x: x.parent_s)


    def add_parent_s(self, parent_s):
        Node._add(self, parent_s, lambda x: x.parent_s, lambda x: x.child_s)
    

    def remove_parent_s_by_name(self, parent_name_s):
        Node._remove_by_name(self, parent_name_s, lambda x: x.parent_s, lambda x: x.child_s)


    def remove_parent_s(self, parent_s):
        Node._remove(self, parent_s, lambda x: x.parent_s, lambda x: x.child_s)


    def _get_to_string_properties(self):
        return { 
                "parents": [n.name for n in self.parent_s],
                "children": [n.name for n in self.child_s],
            }


class Start(GNode):
    def __init__(self, child_s=None):
        super(Start, self).__init__("Start", None, child_s)

    def _get_to_string_properties(self):
        return { 
                "children": [n.name for n in self.child_s],
            }


class Key(GNode):
    def __init__(self, name=None, parent_s=None, lock_s=None):
        super(Key, self).__init__(name, parent_s, None)

        self.lock_s = set()
        if lock_s is not None:
            self.add_lock_s(lock_s)
    

    def add_lock_s(self, lock_s):
        Node._add(self, lock_s, lambda x: x.lock_s, lambda x: x.key_s)
        self.add_child_s(lock_s)
    

    def remove_lock_s_by_name(self, lock_name_s):
        Node._remove_by_name(self, lock_name_s, lambda x: x.lock_s, lambda x: x.key_s)


    def remove_lock_s(self, lock_s):
        Node._remove(self, lock_s, lambda x: x.lock_s, lambda x: x.key_s)


    def _get_to_string_properties(self):
        return { 
                "parents": [n.name for n in self.parent_s],
                "children": [n.name for n in self.child_s],
                "locks": [n.name for n in self.lock_s],
            }
        

class Lock(GNode):
    def __init__(self, name=None, parent_s=None, child_s=None, key_s=None):
        super(Lock, self).__init__(name, parent_s, child_s)

        self.key_s = set()
        if key_s is not None:
            self.add_key_s(key_s)

    
    def add_key_s(self, key_s):
        Node._add(self, key_s, lambda x: x.key_s, lambda x: x.lock_s)
        self.add_parent_s(key_s)
    

    def remove_key_s_by_name(self, key_name_s):
        Node._remove_by_name(self, key_name_s, lambda x: x.key_s, lambda x: x.lock_s)


    def remove_key_s(self, key_s):
        Node._remove(self, key_s, lambda x: x.key_s, lambda x: x.lock_s)


    def _get_to_string_properties(self):
        return { 
                "parents": [n.name for n in self.parent_s],
                "children": [n.name for n in self.child_s],
                "keys": [n.name for n in self.key_s],
            }



class End(GNode):
    def __init__(self, parent_s=None):
        super(End, self).__init__("End", parent_s, None)

    def _get_to_string_properties(self):
        return { 
                "parents": [n.name for n in self.parent_s],
            }



class Collectable(Key):
    def __init__(self, name=None, parent_s=None):
        super(Collectable, self).__init__(name=name, parent_s=parent_s)


    def _get_to_string_properties(self):
        return { 
                "parents": [n.name for n in self.parent_s],
            }



class CollectableBarrier(Lock):
    def __init__(self, name=None, parent_s=None, child_s=None, collectables=None):
        super(CollectableBarrier, self).__init__(name, parent_s, child_s, key_s=collectables)


    def _get_to_string_properties(self):
        return { 
                "parents": [n.name for n in self.parent_s],
                "children": [n.name for n in self.child_s],
                "collectables": [n.name for n in self.key_s],
            }
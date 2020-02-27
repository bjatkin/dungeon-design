from graph_structure.graph_node import GNode, Start, Key, Lock, End
from random import randint

class Graph():
    def __init__(self, difficulty=1):
        # Generate starting and ending nodes
        start = Start()
        end = End()

        n = start
        for i in range(2):
            n = self.grow_graph(n)
        
        # a = self.grow_graph(n)
        b = self.grow_graph(n)

        n = b
        # for i in range(2):
        #     n = self.grow_graph(n, multi=False)

        n.add_child_s([end])
        # end.add_parent_s([n])
        self.start = start
    
    def grow_graph(self, start, multi=False):
        # Add a door
        n = start

        lid = self.get_lock_id()
        name = "Lock"+str(lid)
        l = Lock(parent_s=[n], child_s=[], name=name)
        n.add_child_s([l])
        for i in range(randint(0, 2)):
            if len(n.parent_s) > 0:
                n = n.parent_s[0]
    
        tmp_n = n
        keys = 1
        if multi:
            keys = randint(2, 4)
        
        for k in range(keys):
            n = tmp_n
            for i in range(randint(0, 3)):
                c_len = len(n.child_s)
                if c_len > 1:
                    new_c = n.child_s[randint(0, c_len-1)]
                    if new_c.name != name and not "Key" in new_c.name:
                        n = new_c

            kid = self.get_key_id()
            k = Key(parent_s=[n], child_s=[], name="Key{}({})".format(kid,lid), lock_s=[l])
            n.add_child_s([k])
        
        return l

    lock_id = -1
    def get_lock_id(self):
        self.lock_id += 1
        return self.lock_id
    
    key_id = -1
    def get_key_id(self):
        self.key_id += 1
        return self.key_id

    def string(self):
        return self.recurse_string(self.start)
    
    def recurse_string(self, node):
        base = node.name + "\n"
        for i, c in enumerate(node.child_s):
            base += "Child {} for {}: ".format(i, node.name)
            base += self.recurse_string(c)
        
        return base

    def convert_graph_to_mission_format(self):
        self.add_doors_as_children_to_locks()
        self.sort_key_children_first()

    def sort_key_children_first(self):
        def sort_keys_first(node):
            if isinstance(node, Key):
                return 0
            else:
                return 1

        nodes = GNode.find_all_nodes(self.start, method="breadth-first")
        for node in nodes:
            node.child_s.sort(key=sort_keys_first)
        pass


    def add_doors_as_children_to_locks(self):
        nodes = GNode.find_all_nodes(self.start, method="breadth-first")
        for key_node in nodes:
            if isinstance(key_node, Key):
                key_node.add_child_s(key_node.lock_s)


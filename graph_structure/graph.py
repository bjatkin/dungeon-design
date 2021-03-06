from graph_structure.graph_node import Node, Start, Key, Lock, End, Collectable, CollectableBarrier, Room, SokobanKey, SokobanLock
import numpy as np

class Graph():
    def __init__(self, aesthetic):
        # Generate starting and ending nodes
        start = Start()
        end = End()
        self.start = start
        self.end = end

        self.lock_id = -1
        self.key_id = -1
        self.collect_id = -1
        self.room_id = -1
        

        node_to_grow = start
        tree_depth = np.random.randint(aesthetic.min_depth, aesthetic.max_depth)
        for _ in range(tree_depth):
            branch_count = np.random.choice(range(1, len(aesthetic.branch_probability) + 1), p=aesthetic.branch_probability)
            for _ in range(branch_count):
                f = self.grow_graph(node_to_grow, aesthetic)
            node_to_grow = f
        
        node_to_grow.add_child_s(end)

        if aesthetic.max_multi_lock_count > 0:
            for _ in range(np.random.randint(aesthetic.max_multi_lock_count)):
                self.add_multi_lock(lock_count=np.random.randint(aesthetic.max_locks_per_multi_lock))

        self.insert_rooms(aesthetic)
        self.fill_rooms_with_collectables(aesthetic)
    

    def grow_graph(self, lock_parent, aesthetic, multi="None"):
        ancestor = self.get_random_ancestor(lock_parent)
        key_parent = self.get_random_descendant(ancestor)

        key = self.add_key(key_parent, aesthetic)
        lock = self.add_lock(lock_parent, key)
        return lock


    def get_random_ancestor(self, node):
        ancestors = []
        current_node = node
        while current_node is not None:
            possible_parents = [parent for parent in current_node.parent_s if not isinstance(parent, Key)]
            if len(possible_parents) > 0:
                ancestors.append(possible_parents[0])
                current_node = possible_parents[0]
            else:
                current_node = None

        if len(ancestors) > 0:
            ancestor = np.random.choice(ancestors)
        else:
            ancestor = node

        return ancestor


    def get_random_descendant(self, node):
        def is_valid_descendant(child):
            return not isinstance(child, Key) and not isinstance(child, End)

        possible_descendants = [node for node in Node.find_all_nodes(node) if is_valid_descendant(node)]
        descendant = np.random.choice(possible_descendants)
        return descendant

    
    def add_multi_lock(self, lock_count=2):
        def is_node_multilock_candidate(node):
            is_candidate = (isinstance(node, Key) and
                            len(node.lock_s) == 1 and
                            len(next(iter(node.lock_s)).key_s) == 1)
            return is_candidate

        multilock_key_candidates = [node for node in Node.find_all_nodes(self.start) if is_node_multilock_candidate(node)]
        multilock_key = np.random.choice(multilock_key_candidates)
        lock = next(iter(multilock_key.lock_s))

        for _ in range(lock_count):
            current_node = self.get_random_descendant(lock)

            child = None
            if len(current_node.child_s) > 0:
                child = np.random.choice(list(current_node.child_s))

            lock = self.add_lock(current_node, multilock_key, child)

    
    def add_key(self, key_parent, aesthetic, lock=None):
        key_id = self.get_key_id()
        name = "K{}".format(key_id)
        if np.random.random() < aesthetic.key_is_sokoban_probability:
            key = SokobanKey(name=name, parent_s=key_parent, lock_s=lock)
        else:
            key = Key(name, parent_s=key_parent, lock_s=lock)
        key.id = key_id
        return key


    def add_lock(self, lock_parent, key, lock_replace_child=None):
        lock_id = self.get_lock_id()
        if isinstance(key, SokobanKey):
            lock = SokobanLock(name="L{}".format(lock_id), parent_s=lock_parent, key_s=key)
        else:
            lock = Lock(name="L{}".format(lock_id), parent_s=lock_parent, key_s=key)
        lock.id = lock_id
        if lock_replace_child != None:
            lock.add_child_s(lock_replace_child)
            lock_parent.remove_child_s(lock_replace_child)
        return lock

    def add_collectable(self, collectable_parent):
        collectable_id = self.get_collectable_id()
        collectable = Collectable(name="C{}".format(collectable_id), parent_s=collectable_parent)
        return collectable


    def insert_rooms(self, aesthetic):
        nodes = Node.find_all_nodes(self.start, method="topological-sort")
        for node in nodes:
            keys = [n for n in node.child_s if isinstance(n, Key)]
            if len(keys) > 0 and np.random.random() < aesthetic.insert_room_probability:
                room = Room(str(self.get_room_id()), parent_s=node)
                for key in keys:
                    key.remove_parent_s(node)
                    key.add_parent_s(room)


    def fill_rooms_with_collectables(self, aesthetic):
        def can_node_contain_collectable(node):
            return isinstance(node, Start) or isinstance(node, Lock) or isinstance(node, Room)

        collectables = []
        possible_collectable_room_nodes = [node for node in Node.find_all_nodes(self.start) if can_node_contain_collectable(node)]
        collectable_rooms = [room for room in possible_collectable_room_nodes if np.random.random() < aesthetic.collectable_in_room_probability]
        for collectable_room in collectable_rooms:
            collectable = self.add_collectable(collectable_room)
            collectables.append(collectable)

        collectables.extend(self.fill_dead_ends())

        end_parent = next(iter(self.end.parent_s))
        self.end.remove_parent_s(end_parent)
        collectable_barrier = CollectableBarrier("B", end_parent, self.end, collectables)


    def fill_dead_ends(self):
        collectables = []
        def visit_method(node, visited_nodes):
            if len(node.child_s) == 0 and isinstance(node, Lock):
                collectable = self.add_collectable(node)
                collectables.append(collectable)
        
        Node.traverse_nodes_breadth_first(self.start, visit_method)
        return collectables


    def get_lock_id(self):
        self.lock_id += 1
        return self.lock_id
    

    def get_key_id(self):
        self.key_id += 1
        return self.key_id
    

    def get_collectable_id(self):
        self.collect_id += 1
        return self.collect_id

    def get_room_id(self):
        self.room_id += 1
        return self.room_id


    def string(self):
        return self.recurse_string(self.start)
    

    def recurse_string(self, node):
        base = node.name + "\n"
        for i, c in enumerate(node.child_s):
            base += "Child {} for {}: ".format(i, node.name)
            base += self.recurse_string(c)
        
        return base

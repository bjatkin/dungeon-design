from graph_structure.graph_node import Node, GNode, Start, Key, Lock, End, Collectable
from PIL import Image, ImageDraw, ImageFont
import numpy as np

class Graph():
    def __init__(self, aesthetic):
        # Generate starting and ending nodes
        start = Start()
        end = End()
        self.start = start
        self.end = end

        node_to_grow = start
        tree_depth = np.random.randint(1, aesthetic.max_depth)
        for _ in range(tree_depth):
            branch_count = np.random.choice([1, 2, 3, 4], p=aesthetic.branch_probability)
            for _ in range(branch_count):
                f = self.grow_graph(node_to_grow)
            node_to_grow = f
        
        node_to_grow.add_child_s(end)

        for i in range(aesthetic.multi_lock_types):
            self.add_multi_lock(start, lock_count=aesthetic.multi_lock_count[i])

        self.fill_dead_ends(start)
    

    def grow_graph(self, lock_parent, multi="None"):
        ancestor = self.get_random_ancestor(lock_parent)
        key_parent = self.get_random_descendant(ancestor)

        key = self.add_key(key_parent)
        lock = self.add_lock(lock_parent, key)
        return lock


    def get_random_ancestor(self, node, max_depth=3):
        go_up_count = np.random.randint(0, 3)
        ancestor = node
        for _ in range(go_up_count):
            if len(ancestor.parent_s) > 0:
                ancestor = [parent for parent in ancestor.parent_s if not isinstance(parent, Key)][0]
        return ancestor


    def get_random_descendant(self, node, max_depth=3):
        def is_valid_descendant(child):
            return not isinstance(child, Key) and not isinstance(child, End)

        go_down_count = np.random.randint(0, max_depth)
        descendant = node
        for _ in range(go_down_count):
            possible_descendant_nodes = [child for child in descendant.child_s if is_valid_descendant(child)]
            if len(possible_descendant_nodes) > 0:
                descendant = np.random.choice(possible_descendant_nodes)
        return descendant

    
    def add_multi_lock(self, start, lock_count=2):
        def is_node_multilock_candidate(node):
            is_candidate = (isinstance(node, Key) and
                            len(node.lock_s) == 1 and
                            len(next(iter(node.lock_s)).key_s) == 1)
            return is_candidate

        multilock_key_candidates = [node for node in Node.find_all_nodes(start) if is_node_multilock_candidate(node)]
        multilock_key = np.random.choice(multilock_key_candidates)
        lock = next(iter(multilock_key.lock_s))

        for _ in range(lock_count):
            current_node = self.get_random_descendant(lock)

            child = None
            if len(current_node.child_s) > 0:
                child = np.random.choice(list(current_node.child_s))

            lock = self.add_lock(current_node, multilock_key, child)

    
    def add_key(self, key_parent, lock=None):
        key_id = self.get_key_id()
        key = Key(name="K{}".format(key_id), parent_s=key_parent, lock_s=lock)
        key.id = key_id
        return key


    def add_lock(self, lock_parent, key, lock_replace_child=None):
        lock_id = self.get_lock_id()
        lock = Lock(name="L{}".format(lock_id), parent_s=lock_parent, key_s=key)
        lock.id = lock_id
        if lock_replace_child != None:
            lock.add_child_s(lock_replace_child)
            lock_parent.remove_child_s(lock_replace_child)
        return lock


    def fill_dead_ends(self, start):
        def visit_method(node, visited_nodes):
            if isinstance(node, Lock):
                print(node.name, " Child Length: ", len(node.child_s))
            if len(node.child_s) == 0 and isinstance(node, Lock):
                collectable_id = self.get_collectable_id()
                collectable = Collectable(name="C{}".format(collectable_id), parent_s=[node])
                node.add_child_s(collectable)
        
        GNode.traverse_nodes_breadth_first(self.start, visit_method)


    lock_id = -1
    def get_lock_id(self):
        self.lock_id += 1
        return self.lock_id
    

    key_id = -1
    def get_key_id(self):
        self.key_id += 1
        return self.key_id
    
    collect_id = -1
    def get_collectable_id(self):
        self.collect_id += 1
        return self.collect_id


    def string(self):
        return self.recurse_string(self.start)
    

    def recurse_string(self, node):
        base = node.name + "\n"
        for i, c in enumerate(node.child_s):
            base += "Child {} for {}: ".format(i, node.name)
            base += self.recurse_string(c)
        
        return base
    

    def draw(self):
        im = Image.new('RGB', (1500, 800), (255, 255, 255)) 
        draw = ImageDraw.Draw(im) 
        
        rows = np.full((1000, 1), 0)

        sorted_nodes = Node.find_all_nodes(self.start, method="topological-sort")

        # Draw Connections
        for node in sorted_nodes:
            if len(node.parent_s) > 0:
                parent_node = [node for node in node.parent_s if not isinstance(node, Key)][0]
                node.x = parent_node.x + 2
                # find the size of this row
                new_y = rows[node.x] + 2
                node.y = new_y
                if new_y < node.parent_s[0].y:
                    node.y = node.parent_s[0].y
                    rows[node.x] = node.parent_s[0].y - 2
                rows[node.x] += 2
                self.connect_node(draw, (parent_node.y, parent_node.x, node.y, node.x))
        
        # Draw Nodes
        for node in sorted_nodes:
            if len(node.parent_s) > 0:
                if isinstance(node, Lock):
                    self.draw_node(draw, (node.y, node.x), node.name, n_type="lock")
                elif isinstance(node, End):
                    self.draw_node(draw, (node.y, node.x), node.name, n_type="lock")
                else:
                    self.draw_node(draw, (node.y, node.x), node.name, n_type="key")
        
        GNode.traverse_nodes_breadth_first(self.start, visit_method_connect)
        GNode.traverse_nodes_breadth_first(self.start, visit_method_nodes)

        self.draw_node(draw, (0, 0), "Start", n_type="lock")

        im.save("graph.png")
        im.show()
    

    def draw_node(self, draw, xy, text, n_type="lock"):
        if n_type == "lock":
            color = (128, 128, 255)
            draw.rectangle((xy[0]*50+15, xy[1]*50+15, xy[0]*50+60, xy[1]*50+60), fill=color)
            draw.text((xy[0]*50+23, xy[1]*50+33), text, fill=(255, 255, 255))

        if n_type == "key":
            color = (128, 0, 255)
            draw.ellipse((xy[0]*50+15, xy[1]*50+15, xy[0]*50+60, xy[1]*50+60), fill=color)
            draw.text((xy[0]*50+23, xy[1]*50+33), text, fill=(255, 255, 255))
    

    def connect_node(self, draw, xy, straight=True):
        black = (0, 0, 0)
        if (xy[0] == xy[2] or xy[1] == xy[3]) or straight:
            draw.line((xy[0]*50+38, xy[1]*50+38, xy[2]*50+38, xy[3]*50+38), fill=black)
        else:
            draw.line((xy[0]*50+38, xy[1]*50+38, xy[0]*50+38, xy[3]*50-10), fill=black)
            draw.line((xy[0]*50+38, xy[3]*50-10, xy[2]*50+38, xy[3]*50-10), fill=black)
            draw.line((xy[2]*50+38, xy[3]*50-10, xy[2]*50+38, xy[3]*50+38), fill=black)

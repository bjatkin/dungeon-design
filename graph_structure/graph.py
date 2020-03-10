from graph_structure.graph_node import GNode, Start, Key, Lock, End, Collectable
from PIL import Image, ImageDraw, ImageFont
from random import randint
import numpy as np

class Graph():
    def __init__(self, max_depth=3, branch_prob=[0.8, 0.2, 0.0, 0.0], multi_door_types=1, multi_door_count=[2]):
        # Generate starting and ending nodes
        start = Start()
        end = End()
        self.start = start
        self.end = end

        n = start
        a = randint(1, max_depth)
        for i in range(a):
            b = np.random.choice([1, 2, 3, 4], p=branch_prob)
            for j in range(b):
                f = self.grow_graph(n)
            n = f
        
        n.add_child_s(end)

        for i in range(multi_door_types):
            self.add_multi_door(start, door_count=multi_door_count[i])

        self.fill_dead_ends(start)
    
    def grow_graph(self, start, multi="None"):
        # Add a door
        n = start

        lid = self.get_lock_id()
        name = "L"+str(lid)
        l = Lock(name=name)
        l.id = lid
        l.add_parent_s(n)
        r = randint(0, 3)
        for i in range(r):
            if len(n.parent_s) > 0:
                n = next(iter(n.parent_s))
    
        tmp_n = n
        r = randint(0, 3)
        for i in range(r):
            c_len = len(n.child_s)
            if c_len > 0:
                new_c = np.random.choice(n.child_s)
                if new_c.name != name and not isinstance(new_c, Key):
                    n = new_c

        kid = self.get_key_id()
        k = Key(name="K{}({})".format(kid,lid))
        k.id = kid
        k.add_parent_s(n)
        k.add_lock_s(l)
        
        return l

    def add_multi_door(self, start, door_count=2):
        search = True
        n = start
        while search:
            if len(n.child_s) == 0:
                n = start
            n = np.random.choice(n.child_s)
            if  isinstance(n, Key) and \
                len(n.lock_s) == 1 and \
                len(n.lock_s[0].key_s) == 1:
                n = n.lock_s[0]
                search = False
        
        lock = n
        kid = n.key_s[0].id
        for _ in range(door_count):
            n = lock
            r = randint(0, 3)
            for i in range(r):
                c_len = len(n.child_s)
                if c_len > 0:
                    new_n = np.random.choice(n.child_s)
                    if not isinstance(new_n, Key) and not isinstance(new_n, End):
                        n = new_n
            
            child = None
            print("Child Length:", len(n.child_s))
            if len(n.child_s) > 0:
                child = np.random.choice(n.child_s)

            lid = self.get_lock_id()
            lock = Lock(name="L{}({})".format(lid, kid))
            lock.add_parent_s(n)
            if child != None:
                lock.add_child_s(child)
                n.remove_child_s([child.name])

            print("New Child Length:", len(lock.child_s))

    def fill_dead_ends(self, start):
        def visit_method(node, visited_nodes):
            if isinstance(node, Lock):
                print(node.name, " Child Length: ", len(node.child_s))
            if len(node.child_s) == 0 and isinstance(node, Lock):
                cid = self.get_collectable_id()
                c = Collectable(name="C{}".format(cid), parent_s=[node])
                node.add_child_s(c)
        
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

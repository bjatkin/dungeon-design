from graph_structure.graph_node import GNode, Start, Key, Lock, End
from PIL import Image, ImageDraw, ImageFont
from random import randint
import numpy as np

class Graph():
    def __init__(self, mission_graph_aesthetic):
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

        n.add_child_s(end)
        self.start = start
        self.end = end
    
    def grow_graph(self, start, multi=False):
        # Add a door
        n = start

        lid = self.get_lock_id()
        name = "Lock"+str(lid)
        l = Lock(name=name)
        l.add_parent_s(n)
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
            k = Key(name="Key{}({})".format(kid,lid))
            k.add_parent_s(n)
            k.add_lock_s(l)
        
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
    
    def draw(self):
        im = Image.new('RGB', (800, 1500), (255, 255, 255)) 
        draw = ImageDraw.Draw(im) 
        
        rows = np.full((1000, 1), 0)

        sorted_nodes = Node.find_all_nodes(self.start, method="topological-sort")

        # Draw Connections
        for node in sorted_nodes:
            if len(node.parent_s) > 0:
                parent_node = [node for node in node.parent_s if not isinstance(node, Key)][0]
                node.x = parent_node.x + 2
                # find the size of this row
                node.y = rows[node.x] + 2
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
    
    def connect_node(self, draw, xy):
        black = (0, 0, 0)
        if (xy[0] == xy[2] or xy[1] == xy[3]):
            draw.line((xy[0]*50+38, xy[1]*50+38, xy[2]*50+38, xy[3]*50+38), fill=black)
        else:
            draw.line((xy[0]*50+38, xy[1]*50+38, xy[0]*50+38, xy[3]*50-10), fill=black)
            draw.line((xy[0]*50+38, xy[3]*50-10, xy[2]*50+38, xy[3]*50-10), fill=black)
            draw.line((xy[2]*50+38, xy[3]*50-10, xy[2]*50+38, xy[3]*50+38), fill=black)

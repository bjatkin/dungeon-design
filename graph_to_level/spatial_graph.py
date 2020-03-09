import numpy as np
from graph_structure.graph_node import Node

class SpatialGraph:
    def __init__(self):
        self.nodes = set()



class SpatialGraphNode(Node):
    def __init__(self, mask):
        self.mask = mask

    def add_adjacent_nodes(self, nodes):
        Node._add(self, nodes, lambda x: x.nodes, lambda x: x.nodes)


    def remove_adjacent_nodes(self, child_name_s):
        Node._remove(self, child_name_s, lambda x: x.child_s, lambda x: x.parent_s)
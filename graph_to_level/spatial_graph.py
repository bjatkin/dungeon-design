from graph_structure.graph_node import Node
from scipy.ndimage.measurements import label as label_connected_components
from skimage.morphology import binary_dilation
from dungeon_level.dungeon_tiles import Tiles
import numpy as np

class SpatialGraph:
    def __init__(self, layer):
        self.nodes = SpatialGraph.get_graph_nodes_from_layer(layer)

    
    def merge_node_b_into_a(self, node_a, node_b):
        node_a.merge_node(node_b)
        self.nodes.remove(node_b)

    @staticmethod
    def get_graph_nodes_from_layer(layer):
        nodes = [ SpatialGraphNode(name=str(i), mask=mask) for i, mask in enumerate(SpatialGraph.get_space_component_masks(layer)) ]

        SpatialGraph.connect_space_nodes(nodes)
        return nodes


    @staticmethod
    def connect_space_nodes(nodes):
        for i_a in range(len(nodes)):
            for i_b in range(i_a + 1, len(nodes)):
                node_a = nodes[i_a]
                node_b = nodes[i_b]
                shared_edge_mask = SpatialGraph.get_shared_edge_mask_between_nodes(node_a, node_b)
                if np.any(shared_edge_mask):
                    node_a.add_adjacent_nodes(node_b)

    @staticmethod
    def get_shared_edge_mask_between_nodes(node_a, node_b):
        dilation_a = binary_dilation(node_a.mask)
        dilation_b = binary_dilation(node_b.mask)
        shared_edge_mask = np.logical_and(dilation_a, dilation_b)
        return shared_edge_mask
            

    @staticmethod
    def get_space_component_masks(layer):
        masks = []
        empty_space = (layer == Tiles.empty)
        connected_components, component_count = label_connected_components(empty_space)
        for component_label in range(1, component_count + 1):
            component_mask = (connected_components == component_label).astype(int)
            masks.append(component_mask)
        return masks




class SpatialGraphNode(Node):
    def __init__(self, name=None, mask=None):
        super(SpatialGraphNode, self).__init__(name)
        self.mask = mask

    def merge_node(self, node):
        if node in self.adjacent_nodes:
            self.mask = np.logical_or(self.mask, node.mask)
            self.add_adjacent_nodes(node.adjacent_nodes)
            self.remove_adjacent_nodes([node, self])
            node.remove_adjacent_nodes(node.adjacent_nodes)
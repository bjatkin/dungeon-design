from graph_to_level.unraveler import Unraveler
import numpy as np

class SpatialGraphGenerator:
    @staticmethod
    def generate_spatial_graph(mission_graph_start_node, level_size=np.array([30,30])): # Max Tile World level is 32,32

        nodes, node_positions, adjacency_matrix = SpatialGraphGenerator.init_spatial_graph(mission_graph_start_node)

        Unraveler.unravel_spatial_graph(node_positions, adjacency_matrix)
        SpatialGraphGenerator.center_graph_in_level(node_positions, level_size)
        SpatialGraphGenerator.align_nodes_to_grid(node_positions)
        return nodes, node_positions, adjacency_matrix

    @staticmethod
    def center_graph_in_level(node_positions, level_size):
        min_position = np.min(node_positions, axis=0)
        max_position = np.max(node_positions, axis=0)
        graph_size = max_position - min_position
        
        # Center graph at 0,0
        center = np.average([max_position, min_position], axis=0)
        node_positions -= center

        # Scale graph
        ratio_of_level_filled = 0.75
        node_positions *= level_size * ratio_of_level_filled / graph_size

        # Center graph at center of level
        node_positions += level_size * 0.5


    @staticmethod
    def align_nodes_to_grid(node_positions):
        node_positions = np.round(node_positions)
        

    @staticmethod
    def init_spatial_graph(mission_graph_start_node, random_initial_positions=True):
        nodes = set()
        SpatialGraphGenerator.find_all_nodes(mission_graph_start_node, nodes)
        nodes = sorted(nodes, key=lambda x: x.name)
        if random_initial_positions:
            node_positions = np.random.random([len(nodes), 2]) * 10
        else:
            node_positions = np.transpose(np.stack([np.arange(len(nodes)), np.zeros(len(nodes))]))

        adjacency_matrix = np.zeros([len(nodes), len(nodes)])
        for i, node_start in enumerate(nodes):
            for j, node_end in enumerate(nodes):
                if node_end in node_start.child_s:
                    adjacency_matrix[(i, j)] = 1
                    adjacency_matrix[(j, i)] = 1
        return nodes, node_positions, adjacency_matrix



    @staticmethod
    def find_all_nodes(node, nodes_set):
        nodes_set.add(node)
        for child in node.child_s:
            if not child in nodes_set:
                SpatialGraphGenerator.find_all_nodes(child, nodes_set)

        
        

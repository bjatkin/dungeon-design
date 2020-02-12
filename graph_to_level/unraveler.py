import numpy as np
from graph_structure.graph import Graph
from graph_to_level.spatial_graph_visualizer import SpatialGraphVisualizer


class Unraveler:
    @staticmethod
    def unravel(mission_graph_start_node, frame_debug_method=None):
        mission_nodes, positions, adjacency_matrix = Unraveler.build_spatial_graph(mission_graph_start_node)
        velocities = np.random.random([len(mission_nodes), 2])
        time_step = 0.1
        node_mass = 1.0
        debug_info = None
        state_count = 10
        offsets_history = [float('inf')] * state_count
        stopping_epsilon = 0.000001

        while sum(offsets_history) / len(offsets_history) > stopping_epsilon:
            forces = Unraveler.accumulate_forces(positions, velocities, adjacency_matrix)
            velocities += forces / node_mass * time_step
            offsets = velocities * time_step
            positions += offsets

            if not frame_debug_method is None:
                debug_info = frame_debug_method(positions, adjacency_matrix, debug_info)

            offsets_history.pop(0)
            offsets_history.append(np.average(offsets))

    first_time = True
    @staticmethod
    def accumulate_forces(positions, velocities, adjacency_matrix):
        count, _ = positions.shape
        forces = np.zeros((count, 2))
        # Node Repulsive Forces
        for i in range(count):
            for j in range(count):
                if i != j:
                    distance = Unraveler.distance(positions[i], positions[j])
                    normal = (positions[j] - positions[i]) / distance
                    forces[i] += -normal * 1 / (distance ** 2)
        
        spring_length = 1.0
        # Edge Spring Forces
        for i in range(count):
            for j in range(count):
                if i != j and adjacency_matrix[(i, j)] == 1:
                    distance = Unraveler.distance(positions[i], positions[j])
                    normal = (positions[j] - positions[i]) / distance
                    forces[i] += normal * (distance - spring_length)
        
        # Friction Forces
        for i in range(count):
            forces -= velocities * 0.1
        
        return forces


    @staticmethod
    def distance(position_a, position_b):
        return np.linalg.norm(position_a - position_b, axis=0)

    @staticmethod
    def build_spatial_graph(mission_graph_start_node):
        nodes = set()
        Unraveler.find_all_nodes(mission_graph_start_node, nodes)
        nodes = sorted(nodes, key=lambda x: x.name)
        # node_positions = np.transpose(np.stack([np.arange(len(nodes)), np.zeros(len(nodes))]))
        node_positions = np.random.random([len(nodes), 2]) * 10
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
                Unraveler.find_all_nodes(child, nodes_set)

        
        


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
        stopping_epsilon = 0.004
        max_step_count = 400
        steps = 0

        while sum(offsets_history) / len(offsets_history) > stopping_epsilon and steps < max_step_count:
            forces = Unraveler.accumulate_forces(positions, velocities, adjacency_matrix)
            velocities += forces / node_mass * time_step
            offsets = velocities * time_step
            positions += offsets

            centroid = np.average(positions, axis=0)
            positions -= centroid

            if not frame_debug_method is None:
                debug_info = frame_debug_method(positions, adjacency_matrix, debug_info, last_frame=False)

            offsets_history.pop(0)
            offsets_history.append(np.average(np.linalg.norm(offsets, axis=1)))
            steps += 1
            print("steps {}".format(steps))

        frame_debug_method(positions, adjacency_matrix, debug_info, last_frame=True)

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
                    force = -normal * 1 / (distance ** 2)
                    forces[i] += force
        
        spring_length = 1.0
        # Edge Spring Forces
        for i in range(count):
            for j in range(count):
                if i != j and adjacency_matrix[(i, j)] == 1:
                    distance = Unraveler.distance(positions[i], positions[j])
                    normal = (positions[j] - positions[i]) / distance
                    force = normal * (distance - spring_length)
                    forces[i] += force
        
        # Friction Forces
        for i in range(count):
            forces -= velocities * 0.1

        forces += Unraveler.overlap_repulsive_force(positions, adjacency_matrix)
        
        return forces

    # http://www.cs.swan.ac.uk/~cssimon/line_intersection.html
    @staticmethod
    def find_intersection(p1, p2, p3, p4, count_endpoints=False):
        bottom = (p4[1] - p3[1]) * (p1[0] - p2[0]) - (p1[1] - p2[1]) * (p4[0] - p3[0])
        if bottom == 0:
            return None

        t = (p3[0] - p4[0]) * (p1[1] - p3[1]) + (p4[1] - p3[1]) * (p1[0] - p3[0])
        u = (p1[0] - p2[0]) * (p1[1] - p3[1]) + (p2[1] - p1[1]) * (p1[0] - p3[0])
        if bottom < 0:
            bottom = -bottom
            t = -t
            u = -u
        
        if count_endpoints:
            if t < 0 or u < 0 or t > bottom or u > bottom:
                return None
        else:
            epsilon = 0.000000001
            if t <= epsilon or u <= epsilon or t >= bottom - epsilon or u >= bottom - epsilon:
                return None


        t /= bottom
        u /= bottom
        
        intersection = p1 + t * (p2 - p1)
        return intersection


    
    @staticmethod
    def overlap_repulsive_force(positions, adjacency_matrix):
        node_count, _ = positions.shape
        forces = np.zeros((node_count, 2))

        edges = np.argwhere(adjacency_matrix)
        edge_count, _ = edges.shape
        for i in range(edge_count - 1):
            for j in range(i, edge_count):
                n1 = edges[i, 0]
                n2 = edges[i, 1]
                n3 = edges[j, 0]
                n4 = edges[j, 1]
                p1 = positions[n1]
                p2 = positions[n2]
                p3 = positions[n3]
                p4 = positions[n4]
                intersection = Unraveler.find_intersection(p1, p2, p3, p4)
                if not intersection is None:
                    distance = Unraveler.distance(intersection, p1)
                    normal = (intersection - p1) / distance
                    force = -normal
                    forces[n1] += force
                    forces[n2] += force

        
        return forces
        



    @staticmethod
    def distance(position_a, position_b):
        return np.linalg.norm(position_a - position_b, axis=0)

    @staticmethod
    def build_spatial_graph(mission_graph_start_node):
        nodes = set()
        Unraveler.find_all_nodes(mission_graph_start_node, nodes)
        nodes = sorted(nodes, key=lambda x: x.name)
        node_positions = np.transpose(np.stack([np.arange(len(nodes)), np.zeros(len(nodes))]))
        # node_positions = np.random.random([len(nodes), 2]) * 10
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

        
        


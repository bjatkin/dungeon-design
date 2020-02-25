import numpy as np
from graph_structure.graph import Graph
from graph_to_level.spatial_graph_visualizer import SpatialGraphVisualizer


class Unraveler:
    @staticmethod
    def unravel_spatial_graph(node_positions, adjacency_matrix, frame_debug_method=None):
        node_count, _  = node_positions.shape
        velocities = np.random.random([node_count, 2])
        time_step = 0.1
        node_mass = 1.0
        debug_info = None
        state_count = 10
        offsets_history = [float('inf')] * state_count
        stopping_epsilon = 0.004
        max_step_count = 400
        steps = 0


        while sum(offsets_history) / len(offsets_history) > stopping_epsilon and steps < max_step_count:

            forces = Unraveler.accumulate_forces(node_positions, velocities, adjacency_matrix)
            velocities += forces / node_mass * time_step
            offsets = velocities * time_step
            node_positions += offsets

            centroid = np.average(node_positions, axis=0)
            node_positions -= centroid

            if not frame_debug_method is None:
                debug_info = frame_debug_method(node_positions, adjacency_matrix, debug_info, last_frame=False)

            offsets_history.pop(0)
            offsets_history.append(np.average(np.linalg.norm(offsets, axis=1)))
            steps += 1
            # print("steps {}".format(steps))

        if not frame_debug_method is None:
            frame_debug_method(node_positions, adjacency_matrix, debug_info, last_frame=True)

    @staticmethod
    def add_node_repulsive_forces(positions, forces):
        count, _ = positions.shape
        max_repulsive_force = 10
        for i in range(count):
            distances = Unraveler.distance(positions[i], positions, axis=1).reshape(-1,1)
            normals = (positions - positions[i]) / distances
            repulsive_forces = np.nan_to_num(-normals / (distances ** 2))
            force = np.clip(np.sum(repulsive_forces, axis=0), -max_repulsive_force, max_repulsive_force)
            forces[i] += force

    @staticmethod
    def add_spring_forces(positions, adjacency_matrix, spring_k, forces):
        count, _ = positions.shape
        spring_length = 1.0
        for i in range(count):
            distances = Unraveler.distance(positions[i], positions, axis=1).reshape(-1, 1)
            normals = (positions - positions[i]) / distances
            spring_forces = np.nan_to_num(normals * spring_k * (distances - spring_length))
            spring_forces = spring_forces * adjacency_matrix[i].reshape(-1,1)
            force = np.sum(spring_forces, axis=0)
            forces[i] += force


    @staticmethod
    def add_friction_forces(velocities, forces):
        forces -= velocities * 0.4

    
    @staticmethod
    def add_bounding_forces(positions, forces):
        window_size = 1
        forces += -np.maximum(np.abs(positions) - window_size, 0.) * np.sign(positions)


    @staticmethod
    def accumulate_forces(positions, velocities, adjacency_matrix, spring_k=1.0):
        count, _ = positions.shape
        forces = np.zeros((count, 2))

        Unraveler.add_node_repulsive_forces(positions, forces)
        Unraveler.add_spring_forces(positions, adjacency_matrix, spring_k, forces)
        Unraveler.add_bounding_forces(positions, forces)
        Unraveler.add_friction_forces(velocities, forces)
        Unraveler.add_overlap_repulsive_force(positions, adjacency_matrix, forces)
        
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
    def add_overlap_repulsive_force(positions, adjacency_matrix, forces):
        node_count, _ = positions.shape
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
        

    @staticmethod
    def distance(position_a, position_b, axis=None):
        return np.linalg.norm(position_a - position_b, axis=axis)

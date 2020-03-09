from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
import numpy as np

class SpatialGraphVisualizer:
    @staticmethod
    def visualize_graph(node_positions, adjacency_matrix, window_min=None, window_max=None, resolution=100.0, node_radius=0.01):
        if window_min is None or window_max is None:
            window_min = np.amin(node_positions, axis=0)
            window_max = np.amax(node_positions, axis=0)

        max_dim = np.amax(window_max - window_min)
        padding = max_dim * 0.1
        window_max = window_min + max_dim + padding * 2
        window_min = window_min - padding
        max_dim = np.amax(window_max - window_min)

        node_positions = (node_positions - window_min) * resolution

        image = Image.new('RGB', (int(max_dim * resolution), int(max_dim * resolution)), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        for pos in node_positions:
            pos_min = pos - node_radius * resolution * max_dim
            pos_max = pos + node_radius * resolution * max_dim
            draw.ellipse([pos_min[1], pos_min[0], pos_max[1], pos_max[0]], fill=(0,0,0))

        count, _ = adjacency_matrix.shape
        for i in range(count):
            for j in range(count):
                if adjacency_matrix[(i, j)] == 1:
                    node_positions[i]
                    draw.line([node_positions[i][1], node_positions[i][0], node_positions[j][1], node_positions[j][0]], fill=(0,0,0), width=int(resolution * max_dim * node_radius * 0.5))
        return image

from graph_to_level.legacy.spatial_graph_visualizer import SpatialGraphVisualizer
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import time

def debug_method(node_positions, adjacency_matrix, debug_info, last_frame):
    if debug_info == None:
        im = plt.imshow(Image.new('RGB', (1,1)))
        now = time.time()
        plt.draw()
    else:
        im = debug_info[0]
        now = debug_info[1]

    img = SpatialGraphVisualizer.visualize_graph(node_positions, adjacency_matrix, resolution=25, window_min=np.array([-8, -8]), window_max=np.array([8,8]))
    im.set_data(img)
    plt.draw()
    plt.pause(0.0001)
    # print(time.time() - now)
    now = time.time()
    if last_frame:
        plt.pause(1.0)
    return im, now
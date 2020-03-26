import numpy as np
from PIL import Image, ImageDraw, ImageFont
from graph_structure.graph_node import Node, GNode, Start, Key, Lock, End, Collectable
from collections import defaultdict
from graph_structure.graph import Graph

class GraphVisualizer:
    node_spacing = 90
    node_size = 45
    padding = np.array([15, 15])
    connection_color = (0, 0, 0)
    key_connection_color = (255, 0, 0)
    text_color = (255, 255, 255)
    background_color = (255, 255, 255)
    key_color = (128, 0, 255)
    lock_color = (128, 128, 255)


    @staticmethod
    def show_graph(start_node, draw_straight_lines=True, draw_key_connections=True):
        sorted_nodes = Node.find_all_nodes(start_node, method="topological-sort")
        node_positions = GraphVisualizer.get_node_layout(start_node)

        im = Image.new('RGB', GraphVisualizer.get_image_size(node_positions), GraphVisualizer.background_color) 
        draw = ImageDraw.Draw(im) 

        # Draw Connections
        for node in sorted_nodes:
            parent_node = GraphVisualizer.get_not_key_parent(node)
            if parent_node is not None:
                GraphVisualizer.draw_connection(draw, node_positions[parent_node], node_positions[node], straight=draw_straight_lines, is_key_connection=False)
            if isinstance(node, Key):
                for lock in node.lock_s:
                    GraphVisualizer.draw_connection(draw, node_positions[node], node_positions[lock], straight=True, is_key_connection=True)
        
        # Draw Nodes
        for node in sorted_nodes:
            if isinstance(node, Key):
                node_type = "key"
            else:
                node_type = "lock"
            GraphVisualizer.draw_node(draw, node_positions[node], node.name, n_type=node_type)
        
        im.show()
    

    @staticmethod
    def get_image_size(node_positions):
        positions = np.vstack(list(node_positions.values()))
        max_positions = np.amax(positions, axis=0)
        image_size = GraphVisualizer.padding * 2 + GraphVisualizer.node_size + GraphVisualizer.node_spacing * max_positions
        return tuple(image_size)


    @staticmethod
    def get_not_key_parent(node):
        parents = [parent for parent in node.parent_s if not isinstance(parent, Key)]
        if len(parents) > 0:
            return parents[0]
        else:
            return None

    
    @staticmethod
    def get_node_depth(node):
        node_depth = 0
        parent = GraphVisualizer.get_not_key_parent(node)
        while parent is not None:
            node_depth += 1
            node = parent
            parent = GraphVisualizer.get_not_key_parent(node)

        return node_depth


    @staticmethod
    def get_max_width_below_row(rows, row):
        rows_below = {k:v for k,v in rows.items() if k >= row}
        if len(rows_below) > 0:
            return max(rows_below.values())
        else:
            return rows.default_factory()


    # Layouts out the nodes from left to right so that:
    # * Each node is only as far left as its parent
    # * Each node is spaced apart from its neighbors so that all of its children can fit beside each other below the node.
    # * Nodes are not considered children of Keys/Collectables
    # * Keys/Collectables come last in a each node's children
    @staticmethod
    def get_node_layout(start_node):
        def only_visit_children_of_non_keys(node, child, visited_nodes):
            return not isinstance(node, Key)
        def sort_keys_last(node):
            if isinstance(node, Collectable):
                return 2
            elif isinstance(node, Key):
                return 1
            else:
                return 0

        nodes = Node.find_all_nodes(
            node=start_node, 
            method="depth-first", 
            will_traverse_method=only_visit_children_of_non_keys,
            child_sort_method=sort_keys_last)
        node_positions = dict()
        rows = defaultdict(lambda: -1)
        for node in nodes:
            node_depth = GraphVisualizer.get_node_depth(node)
            if not isinstance(node, Key):
                row_width = GraphVisualizer.get_max_width_below_row(rows, node_depth) 
            else:
                row_width = rows[node_depth]

            node_width = np.maximum(row_width + 1, rows[node_depth - 1])

            rows[node_depth] = node_width
            node_positions[node] = np.array([node_width, node_depth])

        return node_positions


    @staticmethod
    def get_node_position(xy, is_center=False):
        node_xy = xy * GraphVisualizer.node_spacing + GraphVisualizer.padding
        if is_center:
            node_xy += GraphVisualizer.node_size // 2
        return node_xy
    

    @staticmethod
    def draw_node(draw, xy, text, n_type="lock"):
        node_xy = GraphVisualizer.get_node_position(xy)
        node_shape_extents = np.concatenate([node_xy, node_xy + GraphVisualizer.node_size])
        if n_type == "lock":
            draw.rectangle(tuple(node_shape_extents), fill=GraphVisualizer.lock_color)
        elif n_type == "key":
            draw.ellipse(tuple(node_shape_extents), fill=GraphVisualizer.key_color)

        text_w, text_h = draw.textsize(text)
        text_xy = GraphVisualizer.get_node_position(xy, True) - np.array([text_w // 2, text_h // 2])
        draw.text(tuple(text_xy), text, fill=GraphVisualizer.text_color)
    

    @staticmethod
    def draw_connection(draw, xy1, xy2, straight=True, is_key_connection=False):
        center1 = GraphVisualizer.get_node_position(xy1, True)
        center2 = GraphVisualizer.get_node_position(xy2, True)

        if is_key_connection:
            color = GraphVisualizer.key_connection_color
        else:
            color = GraphVisualizer.connection_color

        if (xy1[0] == xy2[0] or xy1[1] == xy2[1]) or straight:
            line = np.concatenate([center1, center2])
            draw.line(tuple(line), fill=color)
        else:
            d = -(GraphVisualizer.node_size + GraphVisualizer.node_spacing) // 2
            draw.line((center1[0], center1[1],     center1[0], center2[1] + d), fill=color)
            draw.line((center1[0], center2[1] + d, center2[0], center2[1] + d), fill=color)
            draw.line((center2[0], center2[1] + d, center2[0], center2[1]    ), fill=color)
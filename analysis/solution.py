import numpy as np
from graph_structure.graph_node import SokobanKey, Start

class Solution:
    def __init__(self, start_position):
        self.start_position = start_position
        self.steps = []


    def add_step(self, node, moves, sokoban_moves=None):
        if not isinstance(node, SokobanKey) and not isinstance(node, Start):
            if sokoban_moves is not None:
                step = (node, sokoban_moves)
            else:
                step = (node, moves)
            self.steps.append(step)


    def get_flattened_moves(self):
        flattened_moves = []
        for step in self.steps:
            node, moves = step
            flattened_moves.extend(moves)
        return flattened_moves


    def get_final_solution_position(self):
        flattened_moves = self.get_flattened_moves()
        offset = np.sum(np.array(flattened_moves, dtype=int), axis=0)
        final_position = offset + self.start_position
        return final_position


    def get_steps_of_type(self, step_types):
        if not isinstance(step_types, list):
            step_types = [step_types]

        steps_of_type = []
        for step in self.steps:
            if any([isinstance(step, step_type) for step_type in step_types]):
                steps_of_type.append(step)
        return steps_of_type
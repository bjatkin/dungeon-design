import numpy as numpy
import copy
from dungeon_level.solution import Solution
from graph_structure.graph_node import Node, SokobanLock

class LevelAnalyzer:
    @staticmethod
    def get_level_quality(level):
        quality_metrics = {
            (1, LevelAnalyzer._get_mission_length_score),
            (1, LevelAnalyzer._get_moves_length_score),
            (1, LevelAnalyzer._get_sokoban_score) }

        level_quality = LevelAnalyzer._get_value_from_metrics(level, quality_metrics)
        return level_quality


    @staticmethod
    def get_level_difficulty(level):
        difficulty_metrics = {
            (1, LevelAnalyzer._get_mission_length_score) }

        level_difficulty = LevelAnalyzer._get_value_from_metrics(level, difficulty_metrics)
        return level_difficulty


    @staticmethod
    def _get_value_from_metrics(level, metrics):
        metric_values = [weight * metric(level) for weight, metric in metrics]
        level_value = sum(metric_values)
        return level_value
        

    @staticmethod
    def _get_moves_length_score(level):
        moves = level.solution.get_flattened_moves()
        moves_length = len(moves)
        return moves_length


    @staticmethod
    def _get_mission_length_score(level):
        nodes = Node.find_all_nodes(level.mission)
        mission_length = len(nodes)
        return mission_length


    @staticmethod
    def _get_sokoban_score(level):
        sokoban_steps = level.solution.get_steps_of_type(SokobanLock)
        total_step_turns = 0
        for sokoban_step in sokoban_steps:
            moves = copy.deepcopy(sokoban_step[1])
            step_turns = 0
            for i in range(1, len(moves)):
                if not np.array_equal(moves[i - 1], moves[i]):
                    turns += 1
            total_step_turns += step_turns

        return total_step_turns
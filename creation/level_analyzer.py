import numpy as np
import copy
from dungeon_level.level import Level
from dungeon_level.dungeon_tiles import Tiles
from dungeon_level.solution import Solution
from validation.path_finder import PathFinder
from validation.player_traverser import PlayerTraverser
from graph_structure.graph_node import Node, SokobanLock, Key, SokobanKey, CollectableBarrier, Collectable, Start, Lock

class LevelAnalyzer:
    @staticmethod
    def get_score_from_metrics(level, metrics, return_type="total", raw_scores=False):
        if raw_scores:
            metric_scores = [metric(level) for weight, normalizer, metric in metrics]
        else:
            metric_scores = [weight * normalizer * metric(level) for weight, normalizer, metric in metrics]
        if return_type == "total":
            level_score = sum(metric_scores)
            return level_score
        else:
            return metric_scores


    @staticmethod
    def _get_turns(steps):
        step_turns = []
        for step in steps:
            _, moves = step
            turn_count = 0
            for i in range(1, len(moves)):
                if tuple(moves[i - 1]) != tuple(moves[i]):
                    turn_count += 1
            step_turns.append(turn_count)
        return step_turns
        

    @staticmethod
    def _get_moves_length_score(level):
        moves = level.solution.get_flattened_moves()
        moves_length = len(moves)
        return moves_length


    @staticmethod
    def _get_average_length_of_step_score(level):
        moves_length = LevelAnalyzer._get_moves_length_score(level)
        mission_length = LevelAnalyzer._get_mission_length_score(level)
        average_length_of_step = float(moves_length) / mission_length
        return average_length_of_step


    @staticmethod
    def _get_mission_length_score(level):
        mission_length = len(level.solution.steps)
        return mission_length


    @staticmethod
    def _get_sokoban_turn_score(level):
        sokoban_steps = level.solution.get_steps_of_type(SokobanLock)
        step_turns = LevelAnalyzer._get_turns(sokoban_steps)
        total_step_turns = sum(step_turns)
        return total_step_turns


    @staticmethod
    def _get_sokoban_count_score(level):
        sokoban_steps = level.solution.get_steps_of_type(SokobanLock)
        sokoban_step_count = len(sokoban_steps)
        return sokoban_step_count


    @staticmethod
    def _get_average_distance_between_locks_and_keys_score(level):
        key_steps = level.solution.get_steps_of_type(step_types=Key, not_of_step_types=[Collectable, SokobanKey])
        single_lock_key_steps = [step for step in key_steps if len(step[0].lock_s) == 1]
        distances_between_locks_and_keys = []
        for step in single_lock_key_steps:
            key_position = level.get_node_position(step[0])
            lock_position = level.get_node_position(next(iter(step[0].lock_s)))
            walls = np.full(level.upper_layer.shape, Tiles.empty)
            walls[level.upper_layer == Tiles.wall] = Tiles.wall
            key_to_lock_moves = PathFinder.find_path(walls, key_position, lock_position, PlayerTraverser.can_traverse, return_type="moves")
            distances_between_locks_and_keys.append(len(key_to_lock_moves))
        
        if len(distances_between_locks_and_keys) > 0:
            average_distance_between_locks_and_keys = float(sum(distances_between_locks_and_keys)) / len(distances_between_locks_and_keys)
        else:
            average_distance_between_locks_and_keys = 0

        return average_distance_between_locks_and_keys


    @staticmethod
    def _get_decision_count_score(level, return_type="total"):
        steps_with_decisions = level.solution.get_steps_of_type([Start, Lock], CollectableBarrier)
        decisions_per_step = [len(node.child_s) for node,_ in steps_with_decisions]
        if return_type == "total":
            return sum(decisions_per_step)
        else:
            return decisions_per_step


    @staticmethod
    def _get_average_decisions_per_step_score(level):
        decisions_per_step = LevelAnalyzer._get_decision_count_score(level, return_type="individual")
        if len(decisions_per_step) > 0:
            average_decisions_per_step = float(sum(decisions_per_step)) / len(decisions_per_step)
        else:
            average_decisions_per_step = 0

        return average_decisions_per_step


LevelAnalyzer.quality_metrics = [
    (8.0,  20.0, LevelAnalyzer._get_mission_length_score),
    (-2.0,  1.0, LevelAnalyzer._get_moves_length_score),
    (6.0,  8.0, LevelAnalyzer._get_sokoban_turn_score),
    (5.0, 80.0, LevelAnalyzer._get_sokoban_count_score),
    (-2.0,  6.0, LevelAnalyzer._get_average_length_of_step_score),
    (1.0, 10.0, LevelAnalyzer._get_decision_count_score),
    (1.0, 40.0, LevelAnalyzer._get_average_decisions_per_step_score),
    (3.0, 5.0, LevelAnalyzer._get_average_distance_between_locks_and_keys_score) ]

LevelAnalyzer.difficulty_metrics = LevelAnalyzer.quality_metrics
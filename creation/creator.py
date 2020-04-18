import numpy as np
import string
import operator
from creation.level_analyzer import LevelAnalyzer
from generation.generator import Generator
from dungeon_level.level_set import LevelSet

class Creator:
    @staticmethod
    def create_level_set(level_type, aesthetic_settings, generate_level_count=10, keep_level_count=5, draw_graph=False, return_quality_scores=False):
        generated_levels = Creator._generate_levels(level_type, aesthetic_settings, generate_level_count, draw_graph)
        best_levels = Creator._pick_best_k_levels(generated_levels, k=keep_level_count)
        level_set = Creator._create_level_set_from_levels(best_levels)

        if return_quality_scores:
            level_quality_scores = [quality_score for quality_score,level in Creator._rate_levels(level_set.levels, LevelAnalyzer.quality_metrics, return_type="individual", raw_scores=True)]
            return level_set, level_quality_scores
        else:
            return level_set


    @staticmethod
    def _generate_levels(level_type, aesthetic_settings, generate_level_count, draw_graph):
        generated_levels = []
        size = (30,30)

        for i in range(generate_level_count):
            was_successful, level = Generator.generate(level_type, size, aesthetic_settings, draw_graph=draw_graph)
            print("({}/{}) Was Generator Successful: {}".format(i + 1, generate_level_count, was_successful))
            if was_successful:
                generated_levels.append(level)
        
        return generated_levels


    # sort_order=["ascending", "descending"]
    @staticmethod
    def _sort_levels_by_metric(levels, metrics, sort_order="ascending"):
        should_reverse = (sort_order == "descending")
        level_scores = Creator._rate_levels(levels, metrics)
        level_scores = sorted(level_scores, key=operator.itemgetter(0), reverse=should_reverse)
        levels = [level for score, level in level_scores]
        return levels


    @staticmethod
    def _rate_levels(levels, metrics, return_type="total", raw_scores=False):
        level_scores = [(LevelAnalyzer.get_score_from_metrics(level, metrics, return_type=return_type, raw_scores=raw_scores),level) for level in levels]
        return level_scores


    @staticmethod
    def _pick_best_k_levels(levels,k=5):
        levels = Creator._sort_levels_by_metric(levels, LevelAnalyzer.quality_metrics, sort_order="descending")
        if k >= len(levels):
            return levels
        else:
            return levels[:k]

    
    @staticmethod
    def _create_level_set_from_levels(levels):
        level_set = LevelSet()
        # levels = Creator._sort_levels_by_metric(levels, LevelAnalyzer.difficulty_metrics, sort_order="ascending")
        for i, level in enumerate(levels):
            level.map_title = "Level {}".format(i + 1)
        level_set.levels = levels
        return level_set
import numpy as np
from dungeon_level.dungeon_tiles import Tiles

class AestheticSettings:
    class LevelSpaceAesthetic:
        def __init__(self):
            self.rectangle_count = 40
            self.rectangle_min = 4
            self.rectangle_max = 15
            self.noise_percentage = 0.15
            self.noise_empty_percentage = 0.5

    class MissionAesthetic:
        def __init__(self):
            self.hazard_spread_probability = {Tiles.water: 0.8, Tiles.fire: 0.3}
            self.single_lock_is_hazard_probability = 0.1

    class TweakerAesthetic:
        def __init__(self):
            self.should_fill_unused_space = True

    class MissionGraphAesthetic:
        def __init__(self):
            self.max_depth = 5
            self.min_depth = 1
            self.branch_probability = [0.8, 0.2]
            self.max_multi_lock_count = 2
            self.max_locks_per_multi_lock = 4
            self.collectable_in_room_probability = 0.75
            

    def __init__(self):
        self.level_space_aesthetic = AestheticSettings.LevelSpaceAesthetic()
        self.mission_aesthetic = AestheticSettings.MissionAesthetic()
        self.tweaker_aesthetic = AestheticSettings.TweakerAesthetic()
        self.mission_graph_aesthetic = AestheticSettings.MissionGraphAesthetic()

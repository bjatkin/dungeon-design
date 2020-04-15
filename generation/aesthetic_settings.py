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
        
        def from_config_data(self, config):
            self.rectangle_count = config['rectangle_count']
            self.rectangle_min = config['rectangle_min']
            self.rectangle_max = config['rectangle_max']
            self.noise_percentage = config['noise_percentage']
            self.noise_empty_percentage = config['noise_empty_percentage']
            self.x_mirror = config['x_mirror']
            self.y_mirror = config['y_mirror']

    class MissionAesthetic:
        def __init__(self):
            self.hazard_spread_probability = {Tiles.water: 0.8, Tiles.fire: 0.3}
            self.single_lock_is_hazard_probability = 0.1
            self.single_lock_is_sokoban_probability = 0.3
        
        def from_config_data(self, config):
            self.hazard_spread_probability = {
                Tiles.water: config['hazard_spread_probability']['water'],
                Tiles.fire: config['hazard_spread_probability']['fire']
            }
            self.single_lock_is_hazard_probability = config['single_lock_is_hazard_probability']


    class TweakerAesthetic:
        def __init__(self):
            self.should_fill_unused_space = True

        def from_config_data(self, config):
            self.should_fill_unused_space = config['should_fill_unused_space']

    class MissionGraphAesthetic:
        def __init__(self):
            self.max_depth = 5
            self.min_depth = 1
            self.branch_probability = [0.8, 0.2]
            self.max_multi_lock_count = 2
            self.max_locks_per_multi_lock = 4
            self.collectable_in_room_probability = 0.75
            
        
        def from_config_data(self, config):
            self.max_depth = config['max_depth']
            self.min_depth = config['min_depth']
            self.branch_probability = config['branch_probability']
            self.max_multi_lock_count = config['max_multi_lock_count']
            self.max_locks_per_multi_lock = config['max_locks_per_multi_lock']
            self.collectable_in_room_probability = config['collectable_in_room_probability']

    def __init__(self):
        self.level_space_aesthetic = AestheticSettings.LevelSpaceAesthetic()
        self.mission_aesthetic = AestheticSettings.MissionAesthetic()
        self.tweaker_aesthetic = AestheticSettings.TweakerAesthetic()
        self.mission_graph_aesthetic = AestheticSettings.MissionGraphAesthetic()
    
    def from_config_data(self, config):
        self.level_space_aesthetic.from_config_data(config['level_space_aesthetic'])
        self.mission_aesthetic.from_config_data(config['mission_aesthetic'])
        self.tweaker_aesthetic.from_config_data(config['tweaker_aesthetic'])
        self.mission_graph_aesthetic.from_config_data(config['mission_graph_aesthetic'])
    
    def from_csv_data(self, csv_data):
        d = csv_data.split(",")
        self.LevelSpaceAesthetic.rectangle_count = int(d[2])
        self.LevelSpaceAesthetic.rectangle_max = int(d[3])
        self.LevelSpaceAesthetic.rectangle_max = int(d[4])
        self.LevelSpaceAesthetic.noise_percentage = int(d[5])
        self.LevelSpaceAesthetic.noise_empty_percentage = float(d[6])
        self.LevelSpaceAesthetic.x_mirror = float(d[7])
        self.LevelSpaceAesthetic.y_mirror = float(d[8])
        self.MissionAesthetic.hazard_spread_probability[Tiles.fire] = float(d[9])
        self.MissionAesthetic.hazard_spread_probability[Tiles.water] = float(d[10])
        self.MissionAesthetic.single_lock_is_hazard_probability = float(d[11])
        self.TweakerAesthetic.should_fill_unused_space = bool(d[12])
        self.MissionGraphAesthetic.max_depth = int(d[13])
        self.MissionGraphAesthetic.min_depth = int(d[14])

        branch_str = d[15].split(":")
        branch_arr = [float(branch_str[0][1:]), float(branch_str[1], float(branch_str[2][:-1]))]
        self.MissionGraphAesthetic.branch_probability = branch_arr

        self.MissionGraphAesthetic.max_multi_lock_count = int(d[16])
        self.MissionGraphAesthetic.max_locks_per_multi_lock = int(d[17])

    @staticmethod
    def csv_header():
        return "rectangle_count,"+\
            "rectangle_min,"+\
            "rectangle_max,"+\
            "noise_percentage,"+\
            "noise_empty_percentage,"+\
            "x_mirror,"+\
            "y_mirror,"+\
            "hazard_spread_probability_water,"+\
            "hazard_spread_probability_fire,"+\
            "single_lock_is_hazard_probability,"+\
            "should_fill_unused_space,"+\
            "max_depth,"+\
            "min_depth,"+\
            "branch_probability,"+\
            "max_multi_lock_count,"+\
            "max_locks_per_multi_lock,"
    
    def csv_data(self):
        return ",".join([
            str(self.level_space_aesthetic.rectangle_count),
            str(self.level_space_aesthetic.rectangle_min),
            str(self.level_space_aesthetic.rectangle_max),
            str(self.level_space_aesthetic.noise_percentage),
            str(self.level_space_aesthetic.noise_empty_percentage),
            str(self.level_space_aesthetic.x_mirror),
            str(self.level_space_aesthetic.y_mirror),
            str(self.mission_aesthetic.hazard_spread_probability[Tiles.water]),
            str(self.mission_aesthetic.hazard_spread_probability[Tiles.fire]),
            str(self.mission_aesthetic.single_lock_is_hazard_probability),
            str(self.tweaker_aesthetic.should_fill_unused_space),
            str(self.mission_graph_aesthetic.max_depth),
            str(self.mission_graph_aesthetic.min_depth),
            "["+str(self.mission_graph_aesthetic.branch_probability[0])+":"+\
            str(self.mission_graph_aesthetic.branch_probability[1])+":"+\
            str(self.mission_graph_aesthetic.branch_probability[2])+":"+\
            str(self.mission_graph_aesthetic.branch_probability[3])+"]",
            str(self.mission_graph_aesthetic.max_multi_lock_count),
            str(self.mission_graph_aesthetic.max_locks_per_multi_lock),
        ])

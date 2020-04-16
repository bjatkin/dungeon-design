import numpy as np
import re
from dungeon_level.dungeon_tiles import Tiles

class AestheticBase:
    def from_config_data(self, config):
        for setting in self.__dict__:
            if setting not in config:
                aesthetic_name = re.sub("(?!^)([A-Z]+)", r"_\1", type(self).__name__).lower()
                raise LookupError("You are missing 'aesthetic.{}.{}' in your config file!".format(aesthetic_name, setting))

            self.__dict__[setting] = config[setting]


class AestheticSettings:
    class LevelSpaceAesthetic(AestheticBase):
        def __init__(self):
            self.rectangle_count = 40
            self.rectangle_min = 4
            self.rectangle_max = 15
            self.noise_percentage = 0.15
            self.noise_empty_percentage = 0.5
            self.x_mirror_probability = 0.5
            self.y_mirror_probability = 0.5
        

    class MissionAesthetic(AestheticBase):
        def __init__(self):
            self.hazard_spread_probability = {Tiles.water: 0.8, Tiles.fire: 0.3}
            self.single_lock_is_hazard_probability = 0.1
        
        def from_config_data(self, config):
            super(AestheticSettings.MissionAesthetic, self).from_config_data(config)
            KEY_MAP = {'water': Tiles.water, 'fire': Tiles.fire}
            self.hazard_spread_probability = { KEY_MAP[key]:value for key,value in self.hazard_spread_probability.items() }


    class TweakerAesthetic(AestheticBase):
        def __init__(self):
            self.should_fill_unused_space = True


    class MissionGraphAesthetic(AestheticBase):
        def __init__(self):
            self.max_depth = 5
            self.min_depth = 1
            self.branch_probability = [0.8, 0.2]
            self.max_multi_lock_count = 2
            self.max_locks_per_multi_lock = 4
            self.collectable_in_room_probability = 0.75
            self.insert_room_probability = 0.4
            self.key_is_sokoban_probability = 0.3
            
        
    def __init__(self):
        self.level_space_aesthetic = AestheticSettings.LevelSpaceAesthetic()
        self.mission_aesthetic = AestheticSettings.MissionAesthetic()
        self.tweaker_aesthetic = AestheticSettings.TweakerAesthetic()
        self.mission_graph_aesthetic = AestheticSettings.MissionGraphAesthetic()
    

    def from_config_data(self, config):
        for aesthetic in self.__dict__:
            self.__dict__[aesthetic].from_config_data(config[aesthetic])


    def from_csv_data(self, csv_data):
        default_settings = AestheticSettings()
        data_paths = AestheticSettings.get_csv_data_paths()
        for data_path, value in zip(data_paths, csv_data):
            aesthetic, setting = data_path
            default_value = default_settings.__dict__[aesthetic].__dict__[setting]
            default_type = type(default_value)

            if default_type is list:
                values = value[1:-1].split(", ")
                converted_value = [type(default_value[0])(x) for x in values]
            elif default_type is dict:
                values = value[1:-1].split(", ")
                converted_value = [type(list(default_value.values())[0])(x) for x in values]
                converted_value = dict(zip(default_value.keys(), converted_value))
            else:
                converted_value = default_type(value)

            self.__dict__[aesthetic].__dict__[setting] = converted_value


    @staticmethod
    def get_csv_data_paths():
        aesthetic_settings = AestheticSettings()
        data_paths = []
        for aesthetic in sorted(aesthetic_settings.__dict__):
            for setting in sorted(aesthetic_settings.__dict__[aesthetic].__dict__):
                data_path = (aesthetic, setting)
                data_paths.append(data_path)
        return data_paths


    @staticmethod
    def get_csv_header():
        data_paths = AestheticSettings.get_csv_data_paths()
        data_paths = ["{}.{}".format(aesthetic, setting) for aesthetic, setting in data_paths]
        return data_paths

    
    def to_csv_data(self):
        data_paths = AestheticSettings.get_csv_data_paths()
        # It is easier to deal with lists than dictionaries for csv data, so we temporarily convert it
        temp = self.mission_aesthetic.hazard_spread_probability
        self.mission_aesthetic.hazard_spread_probability = list(self.mission_aesthetic.hazard_spread_probability.values())
        settings = [str(self.__dict__[aesthetic].__dict__[setting]) for aesthetic, setting in data_paths]
        self.mission_aesthetic.hazard_spread_probability = temp
        return settings
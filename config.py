from generation.aesthetic_settings import AestheticSettings
import json

class ConfigReader():
    def __init__(self, config_file):
            self.super_cc_loc = None
            self.tile_world_loc = None
            self.super_cc_save_file = None
            self.tile_world_save_file = None
            self.puzzle_script_save_file = None
            self.engine = None
            self.level_count = None
            self.play_or_generate = None
            self.ask_for_rating = None
            self.name = None
            self.ratings_file = None
            self.draw_graph = None
            self.aesthetic = None
            self.generate_level_count = None
            self.keep_level_count = None

            with open(config_file) as f:
                config = json.load(f)
                self.from_config_data(config)

                self.aesthetic = AestheticSettings()
                self.aesthetic.from_config_data(config['aesthetic'])


    def from_config_data(self, config):
            for setting in self.__dict__:
                if setting not in config:
                    raise LookupError("You are missing '{}' in your config file!".format(setting))
                self.__dict__[setting] = config[setting]
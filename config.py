import json

class ConfigReader():
    def __init__(self, config_file):
        with open(config_file) as f:
            data = json.load(f)
            self.super_cc_loc = data['super_cc_loc']
            self.tile_world_loc = data['tile_world_loc']
            self.super_cc_save_file = data['super_cc_save_file']
            self.tile_world_save_file = data['tile_world_save_file']
            self.puzzle_script_save_file = data['puzzle_script_save_file']
            self.engine = data['engine']
            self.level_count = data['level_count']
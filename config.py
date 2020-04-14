from generation.aesthetic_settings import AestheticSettings
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
            self.play_or_generate = data['play_or_generate']
            self.ask_for_rating = data['ask_for_rating']
            self.name = data['name']
            self.ratings_file = data['ratings_file']
            self.draw_graph = data['draw_graph']

            self.aesthetic = AestheticSettings()
            self.aesthetic.from_config_data(data['aesthetic'])
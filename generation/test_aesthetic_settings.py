import unittest
import numpy as np
from generation.aesthetic_settings import AestheticBase, AestheticSettings
from dungeon_level.dungeon_tiles import Tiles

class TestAestheticSettings(unittest.TestCase):
    def test_csv_roundtrip(self):
        aesthetic_settings = AestheticSettings()
        paths = AestheticSettings.get_csv_data_paths()
        for i, path in enumerate(paths):
            aesthetic, setting = path
            aesthetic_settings.__dict__[aesthetic].__dict__[setting] = i
        aesthetic_settings.mission_aesthetic.hazard_spread_probability = { Tiles.water: 1, Tiles.fire: 2 }
        aesthetic_settings.mission_graph_aesthetic.branch_probability = [0, 1, 2, 3]
        csv_data = aesthetic_settings.to_csv_data()
        expected_csv_data = ["0", "1", "2", "3", "4", "5", "6", "[1, 2]", "8", "9", "10", "[0, 1, 2, 3]", "12", "13", "14", "15", "16", "17", "18", "19"]

        self.assertEqual(expected_csv_data, csv_data)
        
        aesthetic_settings2 = AestheticSettings()
        aesthetic_settings2.from_csv_data(csv_data)

        expected_values = [0.0, 1.0, 2, 3, 4, 5.0, 6.0, {Tiles.water: 1.0, Tiles.fire: 2.0}, 8, 9, 10.0, [0.0, 1.0, 2.0, 3.0], 12.0, 13.0, 14.0, 15, 16, 17, 18, 19.0 ]
        for path, expected_value in zip(paths, expected_values):
            aesthetic, setting = path
            value = aesthetic_settings2.__dict__[aesthetic].__dict__[setting]
            self.assertEqual(value, expected_value)


    def test_get_csv_header(self):
        header = AestheticSettings.get_csv_header()

        expected_header = [
            "level_space_aesthetic.noise_empty_percentage",
            "level_space_aesthetic.noise_percentage",
            "level_space_aesthetic.rectangle_count",
            "level_space_aesthetic.rectangle_max",
            "level_space_aesthetic.rectangle_min",
            "level_space_aesthetic.x_mirror_probability",
            "level_space_aesthetic.y_mirror_probability",
            "mission_aesthetic.hazard_spread_probability",
            "mission_aesthetic.max_seconds_per_move",
            "mission_aesthetic.min_seconds_per_move",
            "mission_aesthetic.single_lock_is_hazard_probability",
            "mission_graph_aesthetic.branch_probability",
            "mission_graph_aesthetic.collectable_in_room_probability",
            "mission_graph_aesthetic.insert_room_probability",
            "mission_graph_aesthetic.key_is_sokoban_probability",
            "mission_graph_aesthetic.max_depth",
            "mission_graph_aesthetic.max_locks_per_multi_lock",
            "mission_graph_aesthetic.max_multi_lock_count",
            "mission_graph_aesthetic.min_depth",
            "tweaker_aesthetic.should_fill_unused_space"]

        self.assertEqual(header, expected_header)


    def test_get_csv_data_paths(self):
        l = "level_space_aesthetic"
        m = "mission_aesthetic"
        g = "mission_graph_aesthetic"
        t = "tweaker_aesthetic"
        data_paths = AestheticSettings.get_csv_data_paths()
        expected_data_paths = [
                (l, "noise_empty_percentage"),
                (l, "noise_percentage"),
                (l, "rectangle_count"),
                (l, "rectangle_max"),
                (l, "rectangle_min"),
                (l, "x_mirror_probability"),
                (l, "y_mirror_probability"),
                (m, "hazard_spread_probability"),
                (m, "max_seconds_per_move"),
                (m, "min_seconds_per_move"),
                (m, "single_lock_is_hazard_probability"),
                (g, "branch_probability"),
                (g, "collectable_in_room_probability"),
                (g, "insert_room_probability"),
                (g, "key_is_sokoban_probability"),
                (g, "max_depth"),
                (g, "max_locks_per_multi_lock"),
                (g, "max_multi_lock_count"),
                (g, "min_depth"),
                (t, "should_fill_unused_space") ]
        self.assertEqual(expected_data_paths, data_paths)


    def test_from_config_data(self):
        config = {
            "level_space_aesthetic":
            {
                "rectangle_count": 1,
                "rectangle_min": 2,
                "rectangle_max": 3,
                "noise_percentage": 0.4,
                "noise_empty_percentage": 0.6,
                "x_mirror_probability": 0.7,
                "y_mirror_probability": 0.8
            },
            "mission_graph_aesthetic": 
            {
                "max_depth": 1,
                "min_depth": 2,
                "branch_probability": [0.3, 0.4],
                "max_multi_lock_count": 5,
                "max_locks_per_multi_lock": 6,
                "collectable_in_room_probability": 0.7,
                "insert_room_probability": 0.8,
                "key_is_sokoban_probability": 0.9
            },
            "tweaker_aesthetic":
            {
                "should_fill_unused_space": 0.5
            },
            "mission_aesthetic":
            {
                "hazard_spread_probability": 
                {
                    "water": 0.1,
                    "fire": 0.2
                },
                "single_lock_is_hazard_probability": 0.3,
                "max_seconds_per_move": 4,
                "min_seconds_per_move": 5
            }
        }

        aesthetic = AestheticSettings()
        aesthetic.from_config_data(config)
        self.assertEqual(aesthetic.level_space_aesthetic.rectangle_count, 1)
        self.assertEqual(aesthetic.level_space_aesthetic.rectangle_min, 2)
        self.assertEqual(aesthetic.level_space_aesthetic.rectangle_max, 3)
        self.assertEqual(aesthetic.level_space_aesthetic.noise_percentage, 0.4)
        self.assertEqual(aesthetic.level_space_aesthetic.noise_empty_percentage, 0.6)
        self.assertEqual(aesthetic.level_space_aesthetic.x_mirror_probability, 0.7)
        self.assertEqual(aesthetic.level_space_aesthetic.y_mirror_probability, 0.8)

        self.assertEqual(aesthetic.mission_graph_aesthetic.max_depth, 1)
        self.assertEqual(aesthetic.mission_graph_aesthetic.min_depth, 2)
        self.assertEqual(aesthetic.mission_graph_aesthetic.branch_probability, [0.3, 0.4])
        self.assertEqual(aesthetic.mission_graph_aesthetic.max_multi_lock_count, 5)
        self.assertEqual(aesthetic.mission_graph_aesthetic.max_locks_per_multi_lock, 6)
        self.assertEqual(aesthetic.mission_graph_aesthetic.collectable_in_room_probability, 0.7)
        self.assertEqual(aesthetic.mission_graph_aesthetic.insert_room_probability, 0.8)
        self.assertEqual(aesthetic.mission_graph_aesthetic.key_is_sokoban_probability, 0.9)

        self.assertEqual(aesthetic.tweaker_aesthetic.should_fill_unused_space, 0.5)

        self.assertEqual(aesthetic.mission_aesthetic.hazard_spread_probability[Tiles.water], 0.1)
        self.assertEqual(aesthetic.mission_aesthetic.hazard_spread_probability[Tiles.fire], 0.2)
        self.assertEqual(aesthetic.mission_aesthetic.single_lock_is_hazard_probability, 0.3)
        self.assertEqual(aesthetic.mission_aesthetic.max_seconds_per_move, 4)
        self.assertEqual(aesthetic.mission_aesthetic.min_seconds_per_move, 5)
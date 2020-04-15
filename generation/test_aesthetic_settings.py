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
        expected_csv_data = (""
            + "0\t1\t2\t3\t4\t5\t6\t[1, 2]\t8\t9\t[0, 1, 2, 3]\t11\t12\t13\t14\t15\t16\t17")
        
        aesthetic_settings2 = AestheticSettings()
        aesthetic_settings2.from_csv_data(csv_data)

        expected_values = [0.0, 1.0, 2, 3, 4, True, True, {Tiles.water: 1.0, Tiles.fire: 2.0}, 8.0, 9.0, [0.0, 1.0, 2.0, 3.0], 11.0, 12, 13, 14, 15, True ]
        for path, expected_value in zip(paths, expected_values):
            aesthetic, setting = path
            value = aesthetic_settings2.__dict__[aesthetic].__dict__[setting]
            self.assertEqual(value, expected_value)


    def test_get_csv_header(self):
        header = AestheticSettings.get_csv_header()

        expected_header = (""
            + "level_space_aesthetic.noise_empty_percentage\t"
            + "level_space_aesthetic.noise_percentage\t"
            + "level_space_aesthetic.rectangle_count\t"
            + "level_space_aesthetic.rectangle_max\t"
            + "level_space_aesthetic.rectangle_min\t"
            + "level_space_aesthetic.x_mirror\t"
            + "level_space_aesthetic.y_mirror\t"
            + "mission_aesthetic.hazard_spread_probability\t"
            + "mission_aesthetic.single_lock_is_hazard_probability\t"
            + "mission_aesthetic.single_lock_is_sokoban_probability\t"
            + "mission_graph_aesthetic.branch_probability\t"
            + "mission_graph_aesthetic.collectable_in_room_probability\t"
            + "mission_graph_aesthetic.max_depth\t"
            + "mission_graph_aesthetic.max_locks_per_multi_lock\t"
            + "mission_graph_aesthetic.max_multi_lock_count\t"
            + "mission_graph_aesthetic.min_depth\t"
            + "tweaker_aesthetic.should_fill_unused_space")

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
                (l, "x_mirror"),
                (l, "y_mirror"),
                (m, 'hazard_spread_probability'),
                (m, 'single_lock_is_hazard_probability'),
                (m, 'single_lock_is_sokoban_probability'),
                (g, 'branch_probability'),
                (g, 'collectable_in_room_probability'),
                (g, 'max_depth'),
                (g, 'max_locks_per_multi_lock'),
                (g, 'max_multi_lock_count'),
                (g, 'min_depth'),
                (t, 'should_fill_unused_space') ]
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
                "x_mirror": False,
                "y_mirror": True
            },
            "mission_graph_aesthetic": 
            {
                'max_depth': 1,
                'min_depth': 2,
                'branch_probability': [0.3, 0.4],
                'max_multi_lock_count': 5,
                'max_locks_per_multi_lock': 6,
                'collectable_in_room_probability': 0.7
            },
            "tweaker_aesthetic":
            {
                'should_fill_unused_space': False
            },
            "mission_aesthetic":
            {
                'hazard_spread_probability': 
                {
                    'water': 0.1,
                    'fire': 0.2
                },
                'single_lock_is_hazard_probability': 0.3,
                'single_lock_is_sokoban_probability': 0.4
            }
        }

        aesthetic = AestheticSettings()
        aesthetic.from_config_data(config)
        self.assertEqual(aesthetic.level_space_aesthetic.rectangle_count, 1)
        self.assertEqual(aesthetic.level_space_aesthetic.rectangle_min, 2)
        self.assertEqual(aesthetic.level_space_aesthetic.rectangle_max, 3)
        self.assertEqual(aesthetic.level_space_aesthetic.noise_percentage, 0.4)
        self.assertEqual(aesthetic.level_space_aesthetic.noise_empty_percentage, 0.6)
        self.assertEqual(aesthetic.level_space_aesthetic.x_mirror, False)
        self.assertEqual(aesthetic.level_space_aesthetic.y_mirror, True)

        self.assertEqual(aesthetic.mission_graph_aesthetic.max_depth, 1)
        self.assertEqual(aesthetic.mission_graph_aesthetic.min_depth, 2)
        self.assertEqual(aesthetic.mission_graph_aesthetic.branch_probability, [0.3, 0.4])
        self.assertEqual(aesthetic.mission_graph_aesthetic.max_multi_lock_count, 5)
        self.assertEqual(aesthetic.mission_graph_aesthetic.max_locks_per_multi_lock, 6)
        self.assertEqual(aesthetic.mission_graph_aesthetic.collectable_in_room_probability, 0.7)

        self.assertEqual(aesthetic.tweaker_aesthetic.should_fill_unused_space, False)

        self.assertEqual(aesthetic.mission_aesthetic.hazard_spread_probability[Tiles.water], 0.1)
        self.assertEqual(aesthetic.mission_aesthetic.hazard_spread_probability[Tiles.fire], 0.2)
        self.assertEqual(aesthetic.mission_aesthetic.single_lock_is_hazard_probability, 0.3)
        self.assertEqual(aesthetic.mission_aesthetic.single_lock_is_sokoban_probability, 0.4)
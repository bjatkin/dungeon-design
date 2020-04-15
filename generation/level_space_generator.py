from dungeon_level.dungeon_tiles import Tiles, key_to_lock, key_tiles
from generation.drawing import Drawing
import numpy as np

import pdb

class LevelSpaceGenerator:
    @staticmethod
    def generate(level, size, level_space_aesthetic):
        level.upper_layer = np.full(size, Tiles.empty)
        level.lower_layer = np.full(size, Tiles.empty)

        LevelSpaceGenerator.add_random_rectangles(level, size, level_space_aesthetic)
        LevelSpaceGenerator.add_random_noise(level, size, level_space_aesthetic)

        Drawing.draw_rectangle(level.upper_layer, (0,0), size - 1, Tiles.wall)
        LevelSpaceGenerator.mirror_level(level, level_space_aesthetic.x_mirror_probability, level_space_aesthetic.y_mirror_probability)


    @staticmethod
    def add_random_rectangles(level, size, level_space_aesthetic):
        for _ in range(level_space_aesthetic.rectangle_count):
            p0 = LevelSpaceGenerator.get_random_positions(size, 1)[0]
            rect_max = level_space_aesthetic.rectangle_max - level_space_aesthetic.rectangle_min
            p1 = p0 + LevelSpaceGenerator.get_random_positions(np.array([rect_max, rect_max]), 1)[0] + level_space_aesthetic.rectangle_min

            Drawing.fill_rectangle(level.upper_layer, p0 + 1, p1 - 1, Tiles.empty)
            Drawing.draw_rectangle(level.upper_layer, p0, p1, Tiles.wall)

    
    @staticmethod
    def add_random_noise(level, size, level_space_aesthetic):
        random_positions = LevelSpaceGenerator.get_random_positions(size)
        percentage_index = int(level_space_aesthetic.noise_percentage * random_positions.shape[0])
        random_positions = random_positions[:percentage_index]
        for position in random_positions:
            if np.random.random() < level_space_aesthetic.noise_empty_percentage:
                level.upper_layer[tuple(position)] = Tiles.empty
            else:
                level.upper_layer[tuple(position)] = Tiles.wall


    @staticmethod
    def get_random_positions(size, count=None):
        BORDER = 2
        max_index = np.prod(size - BORDER)
        if count == None:
            count = max_index
        random_indices = np.random.choice(max_index, count, replace=False)
        y_vals = random_indices // (size[1] - BORDER)
        x_vals = random_indices - y_vals * (size[1] - BORDER)
        random_positions = np.stack([y_vals, x_vals], axis=1)
        random_positions += BORDER // 2
        return random_positions
    
    @staticmethod
    def mirror_level(level, x_mirror_probability, y_mirror_probability):
        x_mirror = np.random.random() < x_mirror_probability
        y_mirror = np.random.random() < y_mirror_probability

        level_size = np.array(level.upper_layer.shape)
        midpoint = level_size // 2

        if x_mirror:
            flipped_level = np.flip(level.upper_layer, 0)
            level.upper_layer[midpoint[0]:, :] = flipped_level[midpoint[0]:, :]

        if y_mirror:
            flipped_level = np.flip(level.upper_layer, 1)
            level.upper_layer[:, midpoint[1]:] = flipped_level[:, midpoint[1]:]

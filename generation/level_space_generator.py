from dungeon_level.dungeon_tiles import Tiles, key_to_lock, key_tiles
from generation.drawing import Drawing
import numpy as np

class LevelSpaceGenerator:
    @staticmethod
    def generate_level_space(level, size):
        level.upper_layer = np.full(size, Tiles.empty)
        level.lower_layer = np.full(size, Tiles.empty)

        LevelSpaceGenerator.add_random_rectangles(level, size)
        LevelSpaceGenerator.add_random_noise(level, size)

        Drawing.draw_rectangle(level.upper_layer, (0,0), size - 1, Tiles.wall)


    @staticmethod
    def add_random_rectangles(level, size):
        for _ in range(20):
            p0 = LevelSpaceGenerator.get_random_positions(size, 1)[0]
            p1 = p0 + LevelSpaceGenerator.get_random_positions(np.array([10, 10]), 1)[0] + 4

            Drawing.fill_rectangle(level.upper_layer, p0 + 1, p1 - 1, Tiles.empty)
            Drawing.draw_rectangle(level.upper_layer, p0, p1, Tiles.wall)

    
    @staticmethod
    def add_random_noise(level, size):
        random_positions = LevelSpaceGenerator.get_random_positions(size)
        percentage = 0.3
        percentage_index = int(percentage * random_positions.shape[0])
        random_positions = random_positions[:percentage_index]
        for position in random_positions:
            if np.random.randint(4) == 0:
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
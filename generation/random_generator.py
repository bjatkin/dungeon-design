from dungeon_level.dungeon_tiles import Tiles
import random
import numpy as np


class RandomGenerator:
    @staticmethod
    def generate(level, size):
        level.upper_layer = np.full(size, Tiles.empty)
        level.upper_layer = np.pad(level.upper_layer, 1, mode='constant', constant_values=Tiles.wall)

        for y in range(size[0]):
            for x in range(size[1]):
                level.upper_layer[y + 1, x + 1] = RandomGenerator.random_tile()

        player_position = RandomGenerator.get_random_position_in_level(size)
        level.upper_layer[player_position] = Tiles.player

        finish_position = RandomGenerator.get_random_position_in_level(size)
        while finish_position == player_position:
            finish_position = RandomGenerator.get_random_position_in_level(size)
        level.upper_layer[finish_position] = Tiles.finish

        level.required_collectable_count = np.count_nonzero(level.upper_layer == Tiles.collectable)



    @staticmethod
    def get_random_position_in_level(size):
        return random.randint(1, size[0]), random.randint(1, size[1])

    @staticmethod
    def random_tile():
        return random.choices(list(Tiles), [
            0.60, # empty
            0.20, # wall
            0.0,  # player
            0.0,  # finish
            0.05, # movable_block
            0.05, # collectable
            0.0,  # required_collectable_barrier
            0.1   # water
            ])[0]
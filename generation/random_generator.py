from dungeon_level.dungeon_tiles import Tiles
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

        finish_offsets = [np.array([-1, 0]), np.array([1, 0]), np.array([0, -1]), np.array([0, 1]), np.array([0, 0])]
        finish_tiles = [Tiles.wall, Tiles.required_collectable_barrier, Tiles.wall, Tiles.wall, Tiles.finish]
        RandomGenerator.place_feature(level, size, finish_tiles, finish_offsets)

        RandomGenerator.place_feature(level, size, [Tiles.flippers], np.array([0, 0]))

        # RandomGenerator.place_feature(level, size, [Tiles.monster], np.array([0,0]))


        level.required_collectable_count = np.count_nonzero(level.upper_layer == Tiles.collectable)

    @staticmethod
    def place_feature(level, size, feature_tiles, feature_offsets, feature_position=None):
        if feature_position is None:
            feature_position = RandomGenerator.get_random_position_in_level(size)
            while not RandomGenerator.is_free_space(level, feature_position, feature_offsets):
                feature_position = RandomGenerator.get_random_position_in_level(size)

        for tile, neighbor in zip(feature_tiles, feature_offsets):
            level.upper_layer[tuple(neighbor + feature_position)] = tile


    @staticmethod
    def is_free_space(level, position, offsets):
        not_free_tiles = {Tiles.player, Tiles.finish, Tiles.flippers}
        for offset in offsets:
            if level.upper_layer[tuple(position + offset)] in not_free_tiles:
                return False
        return True


    @staticmethod
    def get_random_position_in_level(size):
        return np.random.randint(1, size[0]), np.random.randint(1, size[1])

    @staticmethod
    def random_tile():
        tiles = list(Tiles)
        return np.random.choice(tiles, p= [
            0.60,  # empty
            0.20,  # wall
            0.0,   # player
            0.0,   # finish
            0.05,  # movable_block
            0.03,  # collectable
            0.0,   # required_collectable_barrier
            0.1,   # water
            0.0,   # flippers
            0.02,  # monster
            0.0,   # key_red
            0.0    # lock_red
            ])
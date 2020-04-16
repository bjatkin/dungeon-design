from dungeon_level.dungeon_tiles import Tiles, lock_tiles, key_tiles, item_tiles, hazard_tiles
from dungeon_level.level import Level
import numpy as np

class PlayerStatus:
    def __init__(self, required_collectable_count):
        self.key_counts = [0] * len(key_tiles)
        self.item_counts = [0] * len(item_tiles)
        self.collectable_count = 0
        self.required_collectable_count = required_collectable_count
        self.player_position = np.array([0,0])


    @staticmethod
    def _index_of_tile(tile, tile_list, inverse_tile_list):
        if tile in tile_list:
            index = tile_list.index(tile)
        elif tile in inverse_tile_list:
            index = inverse_tile_list.index(tile)
        else:
            index = None
        return index

    @staticmethod
    def _perform_indexed_operation(tile, tile_list, inverse_tile_list, operation):
        index = PlayerStatus._index_of_tile(tile, tile_list, inverse_tile_list)
        if index is not None:
            return operation(index)
        return None


    def get_key_count(self, tile):
        def op(index):
            return self.key_counts[index]
        return PlayerStatus._perform_indexed_operation(tile, key_tiles, lock_tiles, op)


    def add_to_key_count(self, tile, add_count=1):
        def op(index):
            self.key_counts[index] += add_count
        return PlayerStatus._perform_indexed_operation(tile, key_tiles, lock_tiles, op)


    def remove_from_key_count(self, tile, remove_count=1):
        def op(index):
            self.key_counts[index] -= remove_count
        return PlayerStatus._perform_indexed_operation(tile, key_tiles, lock_tiles, op)

    
    def get_item_count(self, tile):
        def op(index):
            return self.item_counts[index]
        return PlayerStatus._perform_indexed_operation(tile, item_tiles, hazard_tiles, op)


    def add_to_item_count(self, tile, add_count=1):
        def op(index):
            self.item_counts[index] += add_count
        return PlayerStatus._perform_indexed_operation(tile, item_tiles, hazard_tiles, op)


    def remove_from_item_count(self, tile, remove_count=1):
        def op(index):
            self.item_counts[index] -= remove_count
        return PlayerStatus._perform_indexed_operation(tile, item_tiles, hazard_tiles, op)


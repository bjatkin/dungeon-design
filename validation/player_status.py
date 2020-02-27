from dungeon_level.dungeon_tiles import Tiles, lock_tiles, key_tiles
import numpy as np

class PlayerStatus:
    def __init__(self, required_collectable_count):
        self.can_swim = False
        self.key_counts = [0] * len(lock_tiles)
        self.collectable_count = 0
        self.required_collectable_count = required_collectable_count
        self.player_position = np.array([0,0])


    @staticmethod
    def _key_index_of_tile(tile):
        if tile in key_tiles:
            index = key_tiles.index(tile)
        elif tile in lock_tiles:
            index = lock_tiles.index(tile)
        else:
            index = None
        return index

    def get_key_count(self, tile):
        index = PlayerStatus._key_index_of_tile(tile)
        if index is not None:
            return self.key_counts[index]
        return None

    def add_to_key_count(self, tile, add_count=1):
        index = PlayerStatus._key_index_of_tile(tile)
        if index is not None:
            self.key_counts[index] += add_count

    def remove_from_key_count(self, tile, remove_count=1):
        index = PlayerStatus._key_index_of_tile(tile)
        if index is not None:
            self.key_counts[index] -= remove_count

    
    def can_traverse(self, layer, current_position, neighbor_position, is_final_step):
        h, w = layer.shape
        is_within_bounds = neighbor_position[0] >= 0 and neighbor_position[1] >= 0 and neighbor_position[0] < h and neighbor_position[1] < w
        if not is_within_bounds:
            return False
        
        current_tile = layer[tuple(current_position)]
        neighbor_tile = layer[tuple(neighbor_position)]

        if neighbor_tile == Tiles.wall: # We can never walk through walls
            return False

        if current_tile == Tiles.finish: # We can walk to the finish, but we can't walk through it since the level will have completed.
            return False

        if neighbor_tile == Tiles.water and not self.can_swim: # You can only go on water tiles if you can swim.
            return False

        if neighbor_tile == Tiles.required_collectable_barrier and self.collectable_count < self.required_collectable_count: # To pass through the collectable barrier, you need to have all the collectables first.
            return False

        if neighbor_tile == Tiles.movable_block: # TODO: We can't path find with blocks yet.
            return False

        for lock_tile in lock_tiles:
            key_count = self.get_key_count(lock_tile)
            if (neighbor_tile == lock_tile and key_count == 0) or (neighbor_tile == lock_tile and not is_final_step): # We can only step on a lock if we have a key for it and it is destination. If we don't impose the destination rule, then A* becomes much more complicated as we have to try the key with every potential door.
                return False

        return True
from dungeon_level.dungeon_tiles import Tiles, lock_tiles, key_tiles, item_tiles, hazard_tiles
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


    def can_traverse(self, layer, current_position, neighbor_position):
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

        if neighbor_tile == Tiles.required_collectable_barrier and self.collectable_count < self.required_collectable_count: # To pass through the collectable barrier, you need to have all the collectables first.
            return False

        if neighbor_tile == Tiles.movable_block: # TODO: We can't path find with blocks yet.
            return False

        # We can't have the player go past a lock because we can't have the level change as we
        # are performing A* and if we go past a lock, then we have to change our key count and
        # that changes which locks we could open.
        # However, we can see if we end up on a lock to tell if it is reachable.
        for lock_tile in lock_tiles:
            if current_tile == lock_tile:
                return False

        # Similarly, we want to see if hazards are reachable without making them passable.
        # So we allow the player to traverse onto a hazard but not off of it.
        # The player can only traverse off of a hazard if they have the item to do so.
        for hazard_tile in hazard_tiles:
            if current_tile == hazard_tile and neighbor_tile != hazard_tile: # and self.get_item_count(hazard_tile) == 0:
                return False

        return True
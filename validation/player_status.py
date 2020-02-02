from dungeon_level.dungeon_tiles import Tiles

class PlayerStatus:
    def __init__(self):
        self.has_all_collectables = False
        self.can_swim = False

    
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

        if neighbor_tile == Tiles.water and not self.can_swim: # You can only go on water tiles if you can swim.
            return False

        if neighbor_tile == Tiles.required_collectable_barrier and not self.has_all_collectables: # To pass through the collectable barrier, you need to have all the collectables first.
            return False

        if neighbor_tile == Tiles.movable_block: # TODO: We can't path find with blocks yet.
            return False

        return True
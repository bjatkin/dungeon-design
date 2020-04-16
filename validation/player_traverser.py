from dungeon_level.dungeon_tiles import Tiles, lock_tiles, key_tiles, item_tiles, hazard_tiles
from dungeon_level.level import Level
import numpy as np

class PlayerTraverser:
    @staticmethod
    def can_traverse(layer, previous_position, current_position, next_position):
        if not Level.is_position_within_layer_bounds(layer, next_position):
            return False

        current_tile = layer[tuple(current_position)]
        next_tile = layer[tuple(next_position)]

        if next_tile == Tiles.wall: # We can never walk through walls
            return False

        if current_tile in [Tiles.finish, Tiles.required_collectable_barrier, Tiles.sokoban_block]:
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
            if current_tile == hazard_tile and next_tile != hazard_tile:
                return False

        return True
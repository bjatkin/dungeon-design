import unittest
import numpy as np
from validation.player_status import PlayerStatus
from dungeon_level.dungeon_tiles import Tiles, key_tiles, lock_tiles, item_tiles, hazard_tiles

class TestPlayerStatus(unittest.TestCase):
    def test_keys(self):
        get_method = lambda ps, tile: ps.get_key_count(tile)
        add_method = lambda ps, tile, count: ps.add_to_key_count(tile, count)
        remove_method = lambda ps, tile, count: ps.remove_from_key_count(tile, count)

        self.indexed_tests(key_tiles, lock_tiles, get_method, add_method, remove_method)


    def test_items(self):
        get_method = lambda ps, tile: ps.get_item_count(tile)
        add_method = lambda ps, tile, count: ps.add_to_item_count(tile, count)
        remove_method = lambda ps, tile, count: ps.remove_from_item_count(tile, count)

        self.indexed_tests(item_tiles, hazard_tiles, get_method, add_method, remove_method)


    def indexed_tests(self, tiles1, tiles2, get_method, add_method, remove_method):
        player_status = PlayerStatus(4)

        add_values = [3, 7, 9, 11]
        remove_values = [2, 4, 6, 8]
        for i, tile in enumerate(tiles1):
            self.assertEqual(0, get_method(player_status, tile))

            add_method(player_status, tile, add_values[i])
            self.assertEqual(add_values[i], get_method(player_status, tile))

            remove_method(player_status, tile, remove_values[i])
            self.assertEqual(add_values[i] - remove_values[i], get_method(player_status, tile))

        for i, tile in enumerate(tiles2):
            self.assertEqual(add_values[i] - remove_values[i], get_method(player_status, tile))

            add_method(player_status, tile, add_values[i])
            self.assertEqual(2 * add_values[i] - remove_values[i], get_method(player_status, tile))

            remove_method(player_status, tile, remove_values[i])
            self.assertEqual(2 * add_values[i] - 2 * remove_values[i], get_method(player_status, tile))

    def test_can_traverse(self):
        e = Tiles.empty
        lB = Tiles.lock_blue
        lR = Tiles.lock_red
        lG = Tiles.lock_green
        lY = Tiles.lock_yellow
        W = Tiles.water
        w = Tiles.wall
        F = Tiles.fire
        f = Tiles.finish
        b = Tiles.movable_block
        kB = Tiles.key_blue
        kR = Tiles.key_red
        kG = Tiles.key_green
        kY = Tiles.key_yellow

        layer = np.array([
            [e, e, w, e, e],
            [e, e, f, W, W],
            [e, e,kR,kY, e],
            [e, b,kB,kG, e],
            [F, F, e, e, e],
            [e, e, e, e, e],
            [lB,lR,lG,lY,e]], dtype=object)
        player_status = PlayerStatus(4)
        h, w = layer.shape

        # Entering and exiting locks
        # You should always be able to enter and never be able to exit a lock, no matter the key counts.
        # Whether a lock is passable is handled by the solver by checking the respective key count and
        # changing the opened lock to an empty tile and decrementing the key count.
        for j in range(2):
            for i, key_tile in enumerate(key_tiles):
                player_status = PlayerStatus(4)
                self.assertEqual(True, player_status.can_traverse(layer, (5,i), (6,i)))
                self.assertEqual(False, player_status.can_traverse(layer, (6,i), (5,i)))

                player_status.key_counts[i - 1] += 1
                self.assertEqual(True, player_status.can_traverse(layer, (5,i), (6,i)))
                self.assertEqual(False, player_status.can_traverse(layer, (6,i), (5,i)))

                player_status.key_counts[i] += 1
                self.assertEqual(True, player_status.can_traverse(layer, (5,i), (6,i)))
                self.assertEqual(False, player_status.can_traverse(layer, (6,i), (5,i)))

        # Empty North
        self.assertEqual(True, player_status.can_traverse(layer, (1,0), (0,0)))
        # Empty South
        self.assertEqual(True, player_status.can_traverse(layer, (0,0), (1,0)))
        # Empty West
        self.assertEqual(True, player_status.can_traverse(layer, (1,1), (1,0)))
        # Empty East
        self.assertEqual(True, player_status.can_traverse(layer, (1,0), (1,1)))
        # Out of Bounds North
        self.assertEqual(False, player_status.can_traverse(layer, (0,0), (-1,0)))
        # Out of Bounds South
        self.assertEqual(False, player_status.can_traverse(layer, (h - 1,0), (h,0)))
        # Out of Bounds West
        self.assertEqual(False, player_status.can_traverse(layer, (0,0), (0,-1)))
        # Out of Bounds East
        self.assertEqual(False, player_status.can_traverse(layer, (0,w - 1), (0,w)))
        # wall
        self.assertEqual(False, player_status.can_traverse(layer, (0,1), (0,2)))
        # finish
        self.assertEqual(True, player_status.can_traverse(layer, (1,1), (1,2)))
        # key red
        self.assertEqual(True, player_status.can_traverse(layer, (2,1), (2,2)))
        # key blue
        self.assertEqual(True, player_status.can_traverse(layer, (4,2), (3,2)))
        # key green
        self.assertEqual(True, player_status.can_traverse(layer, (3,2), (3,3)))
        # key yellow
        self.assertEqual(True, player_status.can_traverse(layer, (2,2), (2,3)))
        # block
        # self.assertEqual(False, player_status.can_traverse(layer, (3,1), (3,0)))

        # Just like locks, hazards are always enterable, but never exitable
        # However, the player may move around in the hazard (so that the player
        # can reach the lock node). Exiting a hazard is handled by the solver
        # by replacing all hazard tiles with empty tiles.

        item_counts = np.array([
            [0, 0],
            [1, 0],
            [0, 1],
            [1, 1]])
        for item_count in item_counts:
            player_status.item_counts = item_count
            # water
            self.assertEqual(False, player_status.can_traverse(layer, (1,3), (0,3)))
            self.assertEqual(True, player_status.can_traverse(layer, (1,3), (1,4)))
            # fire
            self.assertEqual(False, player_status.can_traverse(layer, (4,0), (3,0)))
            self.assertEqual(True, player_status.can_traverse(layer, (4,0), (4,1)))
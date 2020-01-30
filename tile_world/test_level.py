import unittest
from tile_world.tile_world_writer.level_writer import LevelWriter
from tile_world.tiles import Tiles

class TestTileWorldLevel(unittest.TestCase):
    def test_uncompress(self):
        layer = ([Tiles.finish, Tiles.fire, Tiles.rle, 0x03, Tiles.tank_button, 
                Tiles.finish, Tiles.rle, 0x05, Tiles.socket, Tiles.rle, 0x04, Tiles.red_door])

        expected = ([Tiles.finish, Tiles.fire, Tiles.tank_button, Tiles.tank_button, 
                     Tiles.tank_button, Tiles.finish, Tiles.socket, Tiles.socket, 
                     Tiles.socket, Tiles.socket, Tiles.socket, Tiles.red_door, 
                     Tiles.red_door, Tiles.red_door, Tiles.red_door])

        uncompressed_layer = LevelWriter.uncompress_layer(layer)
        self.assertEqual(uncompressed_layer, expected)

    def test_compress(self):
        layer = ([Tiles.finish, Tiles.fire, Tiles.tank_button, Tiles.tank_button, 
                  Tiles.tank_button, Tiles.finish, Tiles.socket, Tiles.socket, 
                  Tiles.socket, Tiles.socket, Tiles.socket, Tiles.red_door, 
                  Tiles.red_door, Tiles.red_door, Tiles.red_door])
        layer.extend( [ Tiles.blue_door ] * 540)

        expected = ([Tiles.finish, Tiles.fire, Tiles.tank_button, Tiles.tank_button, 
                     Tiles.tank_button, Tiles.finish, Tiles.rle, 0x05, Tiles.socket, 
                     Tiles.rle, 0x04, Tiles.red_door, Tiles.rle, 0xFF, Tiles.blue_door,
                     Tiles.rle, 0xFF, Tiles.blue_door, Tiles.rle, 0x1E, Tiles.blue_door])
        
        compressed_layer = LevelWriter.compress_layer(layer)
        self.assertEqual(compressed_layer, expected)


    def test_standardize_layer(self):
        layer = [Tiles.empty, Tiles.empty, Tiles.empty, Tiles.rle, 0x03, 
                 Tiles.empty, Tiles.wall, Tiles.rle, 0x03, Tiles.socket, 
                 Tiles.red_door, Tiles.red_door, Tiles.suction_boots, 
                 Tiles.rle, 0xFF, Tiles.teleport, Tiles.rle, 0xAA, Tiles.teleport]
        expected = [Tiles.rle, 0x06, Tiles.empty, Tiles.wall, 
                    Tiles.socket, Tiles.socket, Tiles.socket,
                    Tiles.red_door, Tiles.red_door, Tiles.suction_boots,
                    Tiles.rle, 0xFF, Tiles.teleport, Tiles.rle,
                    0xAA, Tiles.teleport, Tiles.rle, 0xFF, Tiles.empty,
                    Tiles.rle, 0xFF, Tiles.empty, Tiles.rle, 0x4C, Tiles.empty]

        standardized_layer = LevelWriter.standardize_layer(layer)
        self.assertEqual(standardized_layer, expected)


    def test_standardize_layer_empty(self):
        layer = []
        expected = [Tiles.rle, 0xFF, Tiles.empty, Tiles.rle, 0xFF, 
                    Tiles.empty, Tiles.rle, 0xFF, Tiles.empty, Tiles.rle, 
                    0xFF, Tiles.empty, Tiles.rle, 0x04, Tiles.empty]

        standardized_layer = LevelWriter.standardize_layer(layer)
        self.assertEqual(standardized_layer, expected)

unittest.main()
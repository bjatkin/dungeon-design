from tile_world.tile_world_level import TileWorldLevel
from tile_world.tile_world_writer.level_writer import LevelWriter
from tile_world.tile_world_writer.file_helpers import *

class LevelSetWriter:
    @staticmethod
    def write(level_set, filename):
        f = open(filename, "wb")
        data = bytearray([])

        header_magic_number = 0x0002AAAC
        wb(data, header_magic_number, LONG_SIZE)
        wb(data, len(level_set.levels), WORD_SIZE)

        for i, level in enumerate(level_set.levels):
            LevelWriter.write(data, level, i + 1)

        f.write(data)
        f.close()
from itertools import groupby

from puzzle_script.puzzle_script_level import PuzzleScriptLevel
from puzzle_script.puzzle_script_tiles import Tiles
from puzzle_script.puzzle_world_writer.layer_converter import LayerConverter

class LevelWriter:
    @staticmethod
    def write(level, level_number):
        data = ""
        data += "\nLevel: {}\n".format(level_number)
        converted_upper_layer = LayerConverter.convert_layer(level.upper_layer)
        converted_lower_layer = LayerConverter.convert_layer(level.lower_layer)
        print(converted_lower_layer)
        for i, tile in enumerate(converted_upper_layer):
            data += tile.value
            if (i+1) % level.LAYER_WIDTH == 0:
                data += "\n"

        return data
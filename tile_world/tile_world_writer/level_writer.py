from itertools import groupby

from tile_world.tile_world_writer.file_helpers import *
from tile_world.tile_world_level import TileWorldLevel
from tile_world.tile_world_writer.fields_writer import *
from tile_world.tile_world_tiles import Tiles
from tile_world.tile_world_writer.layer_converter import LayerConverter

class LevelWriter:
    @staticmethod
    def write(data, level, level_number):
        converted_upper_layer = LayerConverter.convert_layer(level.upper_layer)
        converted_lower_layer = LayerConverter.convert_layer(level.lower_layer)
        fields = LevelWriter.init_fields(level, converted_upper_layer, converted_lower_layer)

        next_record_offset_placeholder = placeholder(data, WORD_SIZE)
        wb(data, level_number, WORD_SIZE)
        wb(data, level.time_limit, WORD_SIZE)
        wb(data, level.required_collectable_count, WORD_SIZE)

        wb(data, 1, WORD_SIZE) # magic number 1

        upper_layer_size_placeholder = placeholder(data, WORD_SIZE)
        LevelWriter.write_layer(data, converted_upper_layer)
        fill_placeholder(data, upper_layer_size_placeholder)

        lower_layer_size_placeholder = placeholder(data, WORD_SIZE)
        LevelWriter.write_layer(data, converted_lower_layer)
        fill_placeholder(data, lower_layer_size_placeholder)

        fields_size_placeholder = placeholder(data, WORD_SIZE)

        for field in fields:
            field.write(data)
        
        fill_placeholder(data, fields_size_placeholder)
        fill_placeholder(data, next_record_offset_placeholder)


    @staticmethod
    def write_layer(data, layer):
        standardized_layer = LevelWriter.standardize_layer(layer)

        for tile in standardized_layer:
            if isinstance(tile, Tiles):
                wb(data, tile.value, BYTE_SIZE)
            else:
                wb(data, tile, BYTE_SIZE)


    @staticmethod
    def init_fields(level, upper_layer, lower_layer):
        fields = [TitleField(level.map_title), PasswordField(level.map_password), HintField(level.map_hint)]
        if len(level.trap_positions) > 0:
            fields.append(TrapsField(level.trap_positions))
        if len(level.cloner_positions) > 0:
            fields.append(ClonersField(level.cloner_positions))

        monsters_field = MonstersField(upper_layer, lower_layer)
        if len(monsters_field.monster_positions) > 0:
            fields.append(monsters_field)
        
        return fields

    
    @staticmethod
    def standardize_layer(layer):
        standardized_layer = layer.copy()
        standardized_layer = LevelWriter.uncompress_layer(standardized_layer)
        standardized_layer.extend([Tiles.empty] * (TileWorldLevel.TILES_PER_LAYER_COUNT - len(standardized_layer)))
        standardized_layer = LevelWriter.compress_layer(standardized_layer)
        return standardized_layer


    @staticmethod
    def uncompress_layer(layer):
        i = 0
        while i < len(layer):
            if layer[i] == Tiles.rle:
                count = layer[i + 1]
                tile_type = layer[i + 2]
                del layer[i:i+3]
                layer[i:i] = [tile_type] * count

            i += 1
        return layer


    @staticmethod
    def compress_layer(layer):
        counts = []
        for x in groupby(layer): # Count the number of same tiles consecutively
            counts.append( ( x[0], len(list(x[1])) ) )
        
        compressed_layer = []
        for x in counts:
            if x[1] <= 3:
                compressed_layer.extend( [ x[0] ] * x[1])
            else:
                rle_count = x[1]
                while rle_count > 0: # We can only do rle encoding up to 255 in length, so spit out chunks of 255 till we do all of the tile.
                    rle_chunk_count = min(0xFF, rle_count)
                    compressed_layer.extend( [ Tiles.rle, rle_chunk_count, x[0] ])
                    rle_count -= rle_chunk_count
        return compressed_layer
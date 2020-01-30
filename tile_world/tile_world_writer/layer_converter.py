from tile_world.tile_world_tiles import Tiles as TWTiles
from tile_world.tile_world_level import TileWorldLevel
from dungeon_level.dungeon_tiles import Tiles as DungeonTiles

class LayerConverter:
    to_tile_world_tile = {
        DungeonTiles.empty          : TWTiles.empty,
        DungeonTiles.wall           : TWTiles.wall,
        DungeonTiles.player         : TWTiles.player,
        DungeonTiles.finish         : TWTiles.finish,
        DungeonTiles.movable_block  : TWTiles.movable_block,
        DungeonTiles.collectable    : TWTiles.chip
    }

    @staticmethod
    def convert_layer(layer):
        converted_layer = []
        for row in layer:
            for tile in row:
                converted_layer.append(LayerConverter.to_tile_world_tile[tile])
            converted_layer.extend([TWTiles.empty] * (TileWorldLevel.LAYER_WIDTH - len(row)))
        return converted_layer
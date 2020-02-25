from tile_world.tile_world_tiles import Tiles as TWTiles
from tile_world.tile_world_level import TileWorldLevel
from dungeon_level.dungeon_tiles import Tiles as DungeonTiles

class LayerConverter:
    to_tile_world_tile = {
        DungeonTiles.empty                          : TWTiles.empty,
        DungeonTiles.wall                           : TWTiles.wall,
        DungeonTiles.player                         : TWTiles.player,
        DungeonTiles.finish                         : TWTiles.finish,
        DungeonTiles.movable_block                  : TWTiles.movable_block,
        DungeonTiles.collectable                    : TWTiles.chip,
        DungeonTiles.required_collectable_barrier   : TWTiles.socket,
        DungeonTiles.water                          : TWTiles.water,
        DungeonTiles.flippers                       : TWTiles.flippers,
        DungeonTiles.monster                        : TWTiles.ghost_n,
        DungeonTiles.key_red                        : TWTiles.red_key,
        DungeonTiles.lock_red                       : TWTiles.red_door,
    }

    @staticmethod
    def convert_layer(layer):
        converted_layer = []
        for row in layer:
            for tile in row:
                converted_layer.append(LayerConverter.to_tile_world_tile[tile])
            converted_layer.extend([TWTiles.empty] * (TileWorldLevel.LAYER_WIDTH - len(row)))
        return converted_layer
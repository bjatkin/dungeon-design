from tile_world.tile_world_tiles import Tiles as TWTiles
from tile_world.tile_world_level import TileWorldLevel
from dungeon_level.dungeon_tiles import Tiles as DungeonTiles

class LayerConverter:
    to_tile_world_tile = {
        DungeonTiles.empty                          : TWTiles.empty,
        DungeonTiles.wall                           : TWTiles.wall,
        DungeonTiles.player                         : TWTiles.player,
        DungeonTiles.finish                         : TWTiles.finish,
        DungeonTiles.sokoban_block                  : TWTiles.movable_block,
        DungeonTiles.sokoban_goal                   : TWTiles.water,
        DungeonTiles.collectable                    : TWTiles.chip,
        DungeonTiles.required_collectable_barrier   : TWTiles.socket,
        DungeonTiles.water                          : TWTiles.water,
        DungeonTiles.flippers                       : TWTiles.flippers,
        DungeonTiles.fire                           : TWTiles.fire,
        DungeonTiles.fire_boots                     : TWTiles.fire_boots,
        DungeonTiles.monster                        : TWTiles.ghost_n,
        DungeonTiles.key_blue                       : TWTiles.blue_key,
        DungeonTiles.lock_blue                      : TWTiles.blue_door,
        DungeonTiles.key_red                        : TWTiles.red_key,
        DungeonTiles.lock_red                       : TWTiles.red_door,
        DungeonTiles.key_green                      : TWTiles.green_key,
        DungeonTiles.lock_green                     : TWTiles.green_door,
        DungeonTiles.key_yellow                     : TWTiles.yellow_key,
        DungeonTiles.lock_yellow                    : TWTiles.yellow_door,
    }

    @staticmethod
    def convert_layer(layer):
        converted_layer = []
        for row in layer:
            for tile in row:
                converted_layer.append(LayerConverter.to_tile_world_tile[tile])
            converted_layer.extend([TWTiles.empty] * (TileWorldLevel.LAYER_WIDTH - len(row)))
        return converted_layer
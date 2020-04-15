from puzzle_script.puzzle_script_tiles import Tiles as PWTiles
from puzzle_script.puzzle_script_level import PuzzleScriptLevel
from dungeon_level.dungeon_tiles import Tiles as DungeonTiles

class LayerConverter:
    to_puzzle_world_tile = {
        DungeonTiles.empty                          : PWTiles.empty,
        DungeonTiles.wall                           : PWTiles.wall,
        DungeonTiles.player                         : PWTiles.player,
        DungeonTiles.finish                         : PWTiles.finish,
        DungeonTiles.sokoban_block                  : PWTiles.movable_block,
        DungeonTiles.sokoban_goal                   : PWTiles.empty,   # PW doesn't have a sokoban goal yet
        DungeonTiles.collectable                    : PWTiles.chip,
        DungeonTiles.required_collectable_barrier   : PWTiles.socket,
        DungeonTiles.water                          : PWTiles.water,
        DungeonTiles.flippers                       : PWTiles.flippers,
        DungeonTiles.fire                           : PWTiles.empty,    # PW doesn't have fire/fireboots yet
        DungeonTiles.fire_boots                     : PWTiles.empty,    # PW doesn't have fire/fireboots yet
        DungeonTiles.monster                        : PWTiles.empty,
        DungeonTiles.key_blue                       : PWTiles.blue_key,
        DungeonTiles.lock_blue                      : PWTiles.blue_door,
        DungeonTiles.key_red                        : PWTiles.red_key,
        DungeonTiles.lock_red                       : PWTiles.red_door,
        DungeonTiles.key_yellow                     : PWTiles.yellow_key,
        DungeonTiles.lock_yellow                    : PWTiles.yellow_door,
        DungeonTiles.key_green                      : PWTiles.empty,    # PW doesn't have a green key or door yet
        DungeonTiles.lock_green                     : PWTiles.empty,    # PW doesn't have a green key or door yet

    }

    @staticmethod
    def convert_layer(layer):
        converted_layer = []
        for row in layer:
            for tile in row:
                converted_layer.append(LayerConverter.to_puzzle_world_tile[tile])
            converted_layer.extend([PWTiles.empty] * (PuzzleScriptLevel.LAYER_WIDTH - len(row)))
        return converted_layer
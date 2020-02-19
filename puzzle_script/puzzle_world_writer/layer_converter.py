from puzzle_script.puzzle_script_tiles import Tiles as PWTiles
from puzzle_script.puzzle_script_level import PuzzleScriptLevel
from dungeon_level.dungeon_tiles import Tiles as DungeonTiles

class LayerConverter:
    to_puzzle_world_tile = {
        DungeonTiles.empty                          : PWTiles.empty,
        DungeonTiles.wall                           : PWTiles.wall,
        DungeonTiles.player                         : PWTiles.player,
        DungeonTiles.finish                         : PWTiles.finish,
        DungeonTiles.movable_block                  : PWTiles.movable_block,
        DungeonTiles.collectable                    : PWTiles.chip,
        DungeonTiles.required_collectable_barrier   : PWTiles.socket,
        DungeonTiles.water                          : PWTiles.water,
        DungeonTiles.flippers                       : PWTiles.flippers,
        DungeonTiles.monster                        : PWTiles.empty
    }

    @staticmethod
    def convert_layer(layer):
        converted_layer = []
        for row in layer:
            for tile in row:
                converted_layer.append(LayerConverter.to_puzzle_world_tile[tile])
            converted_layer.extend([PWTiles.empty] * (PuzzleScriptLevel.LAYER_WIDTH - len(row)))
        return converted_layer
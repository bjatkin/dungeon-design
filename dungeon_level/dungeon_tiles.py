from enum import Enum, unique

@unique
class Tiles(Enum):
    empty                           = 0x00
    wall                            = 0x01
    player                          = 0x02
    finish                          = 0x03
    sokoban_block                   = 0x04
    sokoban_goal                    = 0x05
    collectable                     = 0x06
    required_collectable_barrier    = 0x07
    water                           = 0x08
    flippers                        = 0x09
    fire                            = 0x0A
    fire_boots                      = 0x0B
    monster                         = 0x0C
    key_blue                        = 0x0D
    lock_blue                       = 0x0E
    key_red                         = 0x0F
    lock_red                        = 0x10
    key_green                       = 0x11
    lock_green                      = 0x12
    key_yellow                      = 0x13
    lock_yellow                     = 0x14

    
    def get_tile_type(self):
        if self in key_tiles or self in lock_tiles:
            return TileTypes.key_lock
        elif self in item_tiles or self in hazard_tiles:
            return TileTypes.item_hazard
        elif self in monster_tiles:
            return TileTypes.monster
        else:
            return TileTypes.other

@unique
class TileTypes(Enum):
    key_lock                        = 0x00
    item_hazard                     = 0x01
    monster                         = 0x02
    other                           = 0x03

key_tiles = [Tiles.key_blue, Tiles.key_red, Tiles.key_green, Tiles.key_yellow, Tiles.sokoban_block]
lock_tiles = [Tiles.lock_blue, Tiles.lock_red, Tiles.lock_green, Tiles.lock_yellow, Tiles.sokoban_goal]
key_to_lock = {Tiles.key_blue: Tiles.lock_blue, Tiles.key_red: Tiles.lock_red, Tiles.key_green: Tiles.lock_green, Tiles.key_yellow: Tiles.lock_yellow, Tiles.sokoban_block: Tiles.sokoban_goal}
lock_to_key = {Tiles.lock_blue: Tiles.key_blue, Tiles.lock_red: Tiles.key_red, Tiles.lock_green: Tiles.key_green, Tiles.lock_yellow: Tiles.key_yellow, Tiles.sokoban_goal: Tiles.sokoban_block}

item_tiles = [Tiles.flippers, Tiles.fire_boots]
hazard_tiles = [Tiles.water, Tiles.fire]
item_to_hazard = {Tiles.flippers: Tiles.water, Tiles.fire_boots: Tiles.fire}
hazard_to_item = {Tiles.water: Tiles.flippers, Tiles.fire: Tiles.fire_boots}

monster_tiles = [Tiles.monster]

mission_tiles = [Tiles.key_blue, Tiles.key_red, Tiles.key_green, Tiles.key_yellow, 
                 Tiles.lock_blue, Tiles.lock_red, Tiles.lock_green, Tiles.lock_yellow,
                 Tiles.water, Tiles.flippers, Tiles.fire, Tiles.fire_boots,
                 Tiles.sokoban_block, Tiles.sokoban_goal,
                 Tiles.player, Tiles.finish, Tiles.collectable]
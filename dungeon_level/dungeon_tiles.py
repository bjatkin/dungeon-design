from enum import Enum, unique

@unique
class Tiles(Enum):
    empty                           = 0x00
    wall                            = 0x01
    player                          = 0x02
    finish                          = 0x03
    movable_block                   = 0x04
    collectable                     = 0x05
    required_collectable_barrier    = 0x06
    water                           = 0x07
    flippers                        = 0x08
    fire                            = 0x09
    fire_boots                      = 0x0A
    monster                         = 0x0B
    key_blue                        = 0x0C
    lock_blue                       = 0x0D
    key_red                         = 0x0E
    lock_red                        = 0x0F
    key_green                       = 0x10
    lock_green                      = 0x11
    key_yellow                      = 0x12
    lock_yellow                     = 0x13

    
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

key_tiles = [Tiles.key_blue, Tiles.key_red, Tiles.key_green, Tiles.key_yellow]
lock_tiles = [Tiles.lock_blue, Tiles.lock_red, Tiles.lock_green, Tiles.lock_yellow]
key_to_lock = {Tiles.key_blue: Tiles.lock_blue, Tiles.key_red: Tiles.lock_red, Tiles.key_green: Tiles.lock_green, Tiles.key_yellow: Tiles.lock_yellow}
lock_to_key = {Tiles.lock_blue: Tiles.key_blue, Tiles.lock_red: Tiles.key_red, Tiles.lock_green: Tiles.key_green, Tiles.lock_yellow: Tiles.key_yellow}

item_tiles = [Tiles.flippers, Tiles.fire_boots]
hazard_tiles = [Tiles.water, Tiles.fire]
item_to_hazard = {Tiles.flippers: Tiles.water, Tiles.fire_boots: Tiles.fire}
hazard_to_item = {Tiles.water: Tiles.flippers, Tiles.fire: Tiles.fire_boots}

monster_tiles = [Tiles.monster]

mission_tiles = [Tiles.key_blue, Tiles.key_red, Tiles.key_green, Tiles.key_yellow, 
                 Tiles.lock_blue, Tiles.lock_red, Tiles.lock_green, Tiles.lock_yellow,
                 Tiles.water, Tiles.flippers, Tiles.fire, Tiles.fire_boots,
                 Tiles.player, Tiles.finish, Tiles.collectable]
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
    monster                         = 0x09
    key_blue                        = 0x0A
    lock_blue                       = 0x0B
    key_red                         = 0x0C
    lock_red                        = 0x0D
    key_green                       = 0x0E
    lock_green                      = 0x0F
    key_yellow                      = 0x10
    lock_yellow                     = 0x11

key_tiles = [Tiles.key_blue, Tiles.key_red, Tiles.key_green, Tiles.key_yellow]
lock_tiles = [Tiles.lock_blue, Tiles.lock_red, Tiles.lock_green, Tiles.lock_yellow]
key_to_lock = {Tiles.key_blue: Tiles.lock_blue, Tiles.key_red: Tiles.lock_red, Tiles.key_green: Tiles.lock_green, Tiles.key_yellow: Tiles.lock_yellow}
lock_to_key = {Tiles.lock_blue: Tiles.key_blue, Tiles.lock_red: Tiles.key_red, Tiles.lock_green: Tiles.key_green, Tiles.lock_yellow: Tiles.key_yellow}
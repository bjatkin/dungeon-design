from enum import Enum

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
    key_red                         = 0x0A
    lock_red                        = 0x0B
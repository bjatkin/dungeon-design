from enum import Enum

class Tiles(Enum):
    empty                   = 0x00
    wall                    = 0x01
    player                  = 0x02
    finish                  = 0x03
    movable_block           = 0x04
    collectable             = 0x05
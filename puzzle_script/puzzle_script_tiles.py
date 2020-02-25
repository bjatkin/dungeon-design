from enum import Enum

class Tiles(Enum):
    empty                       = '.'
    wall                        = 'i'
    chip                        = '*'
    water                       = 'c'
    fire                        = 'm'
    movable_block               = 'q'
    dirt                        = 'z'
    finish                      = '*'
    blue_door                   = 'k'
    red_door                    = 'm'
    yellow_door                 = 'l'
    socket                      = '*'
    blue_key                    = 'o'
    red_key                     = 'n'
    yellow_key                  = 'p'
    flippers                    = '+'
    player                      = 'f'
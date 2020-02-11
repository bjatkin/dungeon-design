from enum import Enum

class Tiles(Enum):
    empty                       = 'g'
    wall                        = 'i'
    chip                        = '*'
    water                       = 'c'
    fire                        = 'm'
    # invisible_wall_wont_appear  = 0x05
    # blocked_n                   = 0x06
    # blocked_w                   = 0x07
    # blocked_s                   = 0x08
    # blocked_e                   = 0x09
    movable_block               = 'q'
    dirt                        = 'z'
    # ice                         = 0x0C
    # force_s                     = 0x0D
    # cloneable_block_n           = 0x0E
    # cloneable_block_w           = 0x0F
    # cloneable_block_s           = 0x10
    # cloneable_block_e           = 0x11
    # force_n                     = 0x12
    # force_e                     = 0x13
    # force_w                     = 0x14
    finish                      = '*'
    blue_door                   = 'k'
    red_door                    = 'm'
    # green_door                  = 0x18
    yellow_door                 = 'l'
    # ice_slide_ne                = 0x1A
    # ice_slide_nw                = 0x1B
    # ice_slide_sw                = 0x1C
    # ice_slide_se                = 0x1D
    # blue_empty                  = 0x1E
    # blue_wall                   = 0x1F
    # thief                       = 0x21
    # socket                      = 0x22
    # toggle_button               = 0x23
    # cloner_button               = 0x24
    # toggle_closed               = 0x25
    # toggle_open                 = 0x26
    # trap_button                 = 0x27
    # tank_button                 = 0x28
    # teleport                    = 0x29
    # bomb                        = 0x2A
    # trap                        = 0x2B
    # invisible_wall_will_appear  = 0x2C
    # gravel                      = 0x2D
    # pass_once                   = 0x2E
    # hint                        = 0x2F
    # wall_se                     = 0x30
    # cloner                      = 0x31
    # force_random                = 0x32

    # bug_n                       = 0x40
    # bug_w                       = 0x41
    # bug_s                       = 0x42
    # bug_e                       = 0x43
    # fireball_n                  = 0x44
    # fireball_w                  = 0x45
    # fireball_s                  = 0x46
    # fireball_e                  = 0x47
    # ball_n                      = 0x48
    # ball_w                      = 0x49
    # ball_s                      = 0x4A
    # ball_e                      = 0x4B
    # tank_n                      = 0x4C
    # tank_w                      = 0x4D
    # tank_s                      = 0x4E
    # tank_e                      = 0x4F
    # ghost_n                     = 0x50
    # ghost_w                     = 0x51
    # ghost_s                     = 0x52
    # ghost_e                     = 0x53
    # frog_n                      = 0x54
    # frog_w                      = 0x55
    # frog_s                      = 0x56
    # frog_e                      = 0x57
    # dumbell_n                   = 0x58
    # dumbell_w                   = 0x59
    # dumbell_s                   = 0x5A
    # dumbell_e                   = 0x5B
    # blob_n                      = 0x5C
    # blob_w                      = 0x5D
    # blob_s                      = 0x5E
    # blob_e                      = 0x5F
    # centipede_n                 = 0x60
    # centipede_w                 = 0x61
    # centipede_s                 = 0x62
    # centipede_e                 = 0x63
    blue_key                    = 'o'
    red_key                     = 'n'
    # green_key                   = 0x66
    yellow_key                  = 'p'
    flippers                    = '+'
    # fire_boots                  = 0x69
    # ice_skates                  = 0x6A
    # suction_boots               = 0x6B

    player                      = 'f'
    # rle                         = 0xFF


# monster_tiles = {
#     Tiles.bug_e, Tiles.bug_n, Tiles.bug_s, Tiles.bug_w,
#     Tiles.fireball_e, Tiles.fireball_n, Tiles.fireball_s, Tiles.fireball_w,
#     Tiles.ball_e, Tiles.ball_n, Tiles.ball_s, Tiles.ball_w,
#     Tiles.blob_e, Tiles.blob_n, Tiles.blob_s, Tiles.blob_w,
#     Tiles.centipede_e, Tiles.centipede_n, Tiles.centipede_s, Tiles.centipede_w,
#     Tiles.frog_e, Tiles.frog_n, Tiles.frog_s, Tiles.frog_w,
#     Tiles.ghost_e, Tiles.ghost_n, Tiles.ghost_s, Tiles.ghost_w,
#     Tiles.dumbell_e, Tiles.dumbell_n, Tiles.dumbell_s, Tiles.dumbell_w
# }
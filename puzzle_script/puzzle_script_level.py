from dungeon_level.level import Level


class PuzzleScriptLevel(Level):
    LAYER_WIDTH = 32
    TILES_PER_LAYER_COUNT = LAYER_WIDTH * LAYER_WIDTH

    def __init__(self):
        Level.__init__(self)
        self.map_password = "    "
        self.map_hint = ""
        self.trap_positions = []
        self.cloner_positions = []
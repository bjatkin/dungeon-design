from dungeon_level.dungeon_tiles import Tiles
from scipy.ndimage.measurements import label as label_connected_components
import numpy as np

class LevelTweaker:
    @staticmethod
    def tweak_level(level, tweaker_aesthetic):
        if tweaker_aesthetic.should_fill_unused_space:
            LevelTweaker.fill_unused_space(level)

    @staticmethod
    def fill_unused_space(level):
        start_position = np.argwhere(level.upper_layer == Tiles.player)[0]
        non_wall_mask = (level.upper_layer != Tiles.wall).astype(int)
        connected_components, component_count = label_connected_components(non_wall_mask)
        used_space_component = connected_components[tuple(start_position)]
        level.upper_layer[connected_components != used_space_component] = Tiles.wall
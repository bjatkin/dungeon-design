from dungeon_level.level_set import LevelSet
from dungeon_level.position import Position

from tile_world.tile_world_level import TileWorldLevel
from dungeon_level.dungeon_tiles import Tiles
from tile_world.tile_world_writer.level_set_writer import LevelSetWriter
import subprocess

level_set = LevelSet()

level2 = TileWorldLevel()
level2.map_title = "Ryan's Level"
level2.map_password = "    "
level2.time_limit = 100
level2.required_collectable_count = 1
square_size = 10

E = Tiles.empty
W = Tiles.wall
C = Tiles.collectable
P = Tiles.player
F = Tiles.finish
B = Tiles.movable_block

level2.upper_layer = (
   [[E, E, E, E, E, E, E, E, E, E, E, E],
    [E, W, W, W, W, W, W, W, W, W, W, W],
    [E, W, E, E, E, E, C, E, E, E, F, W],
    [E, W, P, E, E, E, E, E, E, E, E, W],
    [E, W, E, E, E, E, E, E, E, E, E, W],
    [E, W, E, E, E, E, E, E, E, E, E, W],
    [E, W, E, E, E, E, E, E, E, B, E, W],
    [E, W, E, C, E, E, E, E, E, W, W, W],
    [E, W, E, E, E, E, E, E, E, E, F, W],
    [E, W, W, W, W, W, W, W, W, W, W, W]])




level_set.levels.append(level2)

working_dir = "C:/Program Files/Tile World"
save_file = "test.dat"


LevelSetWriter.write(level_set, "{}/sets/{}".format(working_dir, save_file))
subprocess.run("{}/tworld.exe {} --read-only".format(working_dir, save_file), cwd=working_dir)
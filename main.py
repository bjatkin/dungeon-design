from dungeon_level.level_set import LevelSet
from dungeon_level.position import Position

from tile_world.tile_world_level import TileWorldLevel
from dungeon_level.dungeon_tiles import Tiles
from tile_world.tile_world_writer.level_set_writer import LevelSetWriter
import random
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
P = Tiles.player
F = Tiles.finish
B = Tiles.movable_block
C = Tiles.collectable
R = Tiles.required_collectable_barrier
w = Tiles.water

def r():
    return random.choices(list(Tiles), [0.65, 0.15, 0.0, 0.0, 0.05, 0.05, 0.0, 0.1])

def populate_layer(layer):
    for y in range(len(layer)):
        for x in range(len(layer[y])):
            if layer[y][x] == E:
                layer[y][x] = r()[0]
    return layer

level2.upper_layer = (
   [[E, E, E, E, E, E, E, E, E, E, E, E],
    [E, W, W, W, W, W, W, W, W, W, W, W],
    [E, W, E, E, E, E, E, E, E, E, E, W],
    [E, W, E, E, P, E, E, E, E, E, E, W],
    [E, W, E, E, E, E, E, E, E, E, E, W],
    [E, W, E, E, E, E, E, E, E, E, E, W],
    [E, W, E, E, E, E, E, E, E, E, E, W],
    [E, W, E, E, E, E, E, E, E, W, W, W],
    [E, W, E, E, E, E, E, E, E, R, F, W],
    [E, W, W, W, W, W, W, W, W, W, W, W]])

level2.upper_layer = populate_layer(level2.upper_layer)



level_set.levels.append(level2)

working_dir = "C:/Program Files/Tile World"
save_file = "test.dat"


LevelSetWriter.write(level_set, "{}/sets/{}".format(working_dir, save_file))
subprocess.run("{}/tworld.exe {} --read-only".format(working_dir, save_file), cwd=working_dir)
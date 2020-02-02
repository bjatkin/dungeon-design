from dungeon_level.level_set import LevelSet
from dungeon_level.dungeon_tiles import Tiles
from generation.random_generator import RandomGenerator
from tile_world.tile_world_level import TileWorldLevel
from tile_world.tile_world_writer.level_set_writer import LevelSetWriter
from validation.solver import Solver

import numpy as np
import subprocess




level = TileWorldLevel()
level.map_title = "Ryan's Level"
level.map_password = "    "
level.time_limit = 100

size = (20, 20)

RandomGenerator.generate(level, size)
while not Solver.is_solvable(level):
    RandomGenerator.generate(level, size)
    




level_set = LevelSet()
level_set.levels.append(level)

working_dir = "C:/Program Files/Tile World"
save_file = "test.dat"


LevelSetWriter.write(level_set, "{}/sets/{}".format(working_dir, save_file))
subprocess.run("{}/tworld.exe {} --read-only".format(working_dir, save_file), cwd=working_dir)
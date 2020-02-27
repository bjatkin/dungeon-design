from dungeon_level.level_set import LevelSet
from dungeon_level.dungeon_tiles import Tiles
from generation.random_generator import RandomGenerator
from generation.random_mission_generator import RandomMissionGenerator
from tile_world.tile_world_level import TileWorldLevel
# from puzzle_script.puzzle_world_writer.level_set_writer import LevelSetWriter
from tile_world.tile_world_writer.level_set_writer import LevelSetWriter
from validation.solver import Solver

import numpy as np
import random
import subprocess

seed = 3
random.seed(seed)
np.random.seed(seed)


level = TileWorldLevel()
# level = PuzzleScriptLevel()
level.map_title = "Brandon's Level"
level.map_password = "    "
level.time_limit = 100

size = (30, 30)

RandomMissionGenerator.generate(level, size)
    




level_set = LevelSet()
level_set.levels.append(level)

def run_supercc():
    wd = "C:/Users/Ryan/Drive/BYU/2020_Winter/cs_673/supercc/"
    subprocess.run("java -jar {}supercc.jar \"C:\\Program Files\\Tile World\\sets\\test.dat\"".format(wd), cwd=wd)

def run_tworld(save_file):
    wd = "C:/Program Files/Tile World"
    subprocess.run("{}/tworld.exe {} --read-only".format(wd, save_file), cwd=wd)



working_dir = "C:/Program Files/Tile World"
save_file = "test.dat"
LevelSetWriter.write(level_set, "{}/sets/{}".format(working_dir, save_file))

run_supercc()

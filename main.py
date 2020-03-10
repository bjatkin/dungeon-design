from dungeon_level.level_set import LevelSet
from dungeon_level.dungeon_tiles import Tiles
from generation.generator import Generator
from tile_world.tile_world_level import TileWorldLevel
# from puzzle_script.puzzle_world_writer.level_set_writer import LevelSetWriter
from tile_world.tile_world_writer.level_set_writer import LevelSetWriter
from validation.solver import Solver
from generation.aesthetic_settings import AestheticSettings
from log import Log

import numpy as np
import random
import subprocess

Log.verbose = True
# We randomly choose our random seed.... why?
# So that if we want to reproduce the level, we know what seed to use,
# and so that we don't have to change the seed each time we run the program.
seed = np.random.randint(1e5)
# seed = 1377
print("Level seed: {}".format(seed))
random.seed(seed)
np.random.seed(seed)


level_count = 1
size = (30, 30)
level_set = LevelSet()
aesthetic_settings = AestheticSettings()
aesthetic_settings.level_space_aesthetic.noise_percentage = 0
aesthetic_settings.mission_aesthetic.single_lock_is_hazard_probability = 0.1
aesthetic_settings.tweaker_aesthetic.should_fill_unused_space = False

for i in range(level_count):
    level = TileWorldLevel()
    # level = PuzzleScriptLevel()
    level.map_title = "Level {}".format(i + 1)
    level.map_password = "    "
    level.time_limit = 100

    was_successful = Generator.generate(level, size, aesthetic_settings)
    print("Was Generator Successful: {}".format(was_successful))
    level_set.levels.append(level)
    
print("Level seed: {}".format(seed))




# TODO: change the wd's to be pulled from a local config file
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

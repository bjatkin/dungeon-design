from dungeon_level.level_set import LevelSet
from dungeon_level.dungeon_tiles import Tiles
from generation.generator import Generator
from tile_world.tile_world_level import TileWorldLevel
from puzzle_script.puzzle_script_level import PuzzleScriptLevel
from puzzle_script.puzzle_world_writer.level_set_writer import LevelSetWriter as PSLevelSetWriter
from tile_world.tile_world_writer.level_set_writer import LevelSetWriter as TWLeveSetWriter
from validation.solver import Solver
from generation.aesthetic_settings import AestheticSettings
from log import Log
from config import ConfigReader

import numpy as np
import random
import subprocess
import pdb

config = ConfigReader('config.json')

Log.verbose = True
# We randomly choose our random seed.... why?
# So that if we want to reproduce the level, we know what seed to use,
# and so that we don't have to change the seed each time we run the program.
seed = np.random.randint(1e5)
# seed = 1377
print("Level seed: {}".format(seed))
random.seed(seed)
np.random.seed(seed)


level_count = config.level_count
size = (30, 30)
level_set = LevelSet()
aesthetic_settings = AestheticSettings()
aesthetic_settings.level_space_aesthetic.noise_percentage = 0
aesthetic_settings.mission_aesthetic.single_lock_is_hazard_probability = 0.1
aesthetic_settings.tweaker_aesthetic.should_fill_unused_space = False

for i in range(level_count):
    level = TileWorldLevel()
    if config.engine == 'PS':
        level = PuzzleScriptLevel()

    level.map_title = "Level {}".format(i + 1)
    level.map_password = "    "
    level.time_limit = 100

    was_successful = Generator.generate(level, size, aesthetic_settings)
    print("Was Generator Successful: {}".format(was_successful))

    level_set.levels.append(level)
    
print("Level seed: {}".format(seed))

if config.engine == 'TW':
    TWLeveSetWriter.write(level_set, config.tile_world_save_file)

    # Run TWorld
    wd = config.tile_world_loc
    subprocess.run("{}/tworld.exe {} --read-only".format(wd, config.tile_world_save_file), cwd=wd)
elif config.engine == 'CC':
    TWLeveSetWriter.write(level_set, config.tile_world_save_file)

    # Run SuperCC
    wd = config.super_cc_loc
    subprocess.run("java -jar {}supercc.jar \"{}\"".format(wd, config.super_cc_save_file), cwd=wd)
else:
    PSLevelSetWriter.write(level_set, config.puzzle_script_save_file)

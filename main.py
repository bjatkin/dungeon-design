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
from ratings.ratings import Ratings

import numpy as np
import random
import subprocess
import pdb

config = ConfigReader('config.json')

Log.verbose = True

ratings = Ratings(config.ratings_file)

level_count = config.level_count
if config.play_or_generate == "play":
    level_count = ratings.level_count()

size = (30, 30)
level_set = LevelSet()
aesthetic_settings = AestheticSettings()
aesthetic_settings.level_space_aesthetic.noise_percentage = config.aesthetic.noise
aesthetic_settings.mission_aesthetic.single_lock_is_hazard_probability = config.aesthetic.single_lock_is_hazard
aesthetic_settings.tweaker_aesthetic.should_fill_unused_space = config.aesthetic.fill_space

seeds = []
for i in range(level_count):
    # We randomly choose our random seed.... why?
    # So that if we want to reproduce the level, we know what seed to use,
    # and so that we don't have to change the seed each time we run the program.
    seed = np.random.randint(1e5)
    if config.play_or_generate == "play":
        seed = ratings.level_seed(i)

    seeds.append(seed)
    print("Level seed: {}".format(seed))
    random.seed(seed)
    np.random.seed(seed)

    level = TileWorldLevel()
    if config.engine == 'PS':
        level = PuzzleScriptLevel()

    level.map_title = "Level {}".format(i + 1)
    level.map_password = "    "
    level.time_limit = 100

    was_successful = Generator.generate(level, size, aesthetic_settings)
    print("Was Generator Successful: {}".format(was_successful))

    level_set.levels.append(level)

    if config.play_or_generate == "generate":
        ratings.add_level(seed)
    
ratings.save()

def rate_levels(ratings, name, seeds, level_count):
    for i in range(level_count):
        r = input("What is your rating for level "+str(i)+"? (0 - 10): ")
        if r == "":
            r = 0
        ratings.add_rating(name, seeds[i], r)
        ratings.save()

    ratings.save()

if config.engine == 'TW':
    TWLeveSetWriter.write(level_set, config.tile_world_save_file)

    # Run TWorld
    wd = config.tile_world_loc
    subprocess.Popen("{}/tworld.exe {} --read-only".format(wd, config.tile_world_save_file), cwd=wd, shell=True)
    rate_levels(ratings, config.name, seeds, level_count)

elif config.engine == 'CC':
    TWLeveSetWriter.write(level_set, config.tile_world_save_file)

    # Run SuperCC
    wd = config.super_cc_loc
    subprocess.Popen("java -jar {}/SuperCC.jar \"{}\"".format(wd, config.super_cc_save_file), cwd=wd, shell=True)
    rate_levels(ratings, config.name, seeds, level_count)

else:
    PSLevelSetWriter.write(level_set, config.puzzle_script_save_file)
    rate_levels(ratings, config.name, seeds, level_count)

from dungeon_level.dungeon_tiles import Tiles
from generation.generator import Generator
from tile_world.tile_world_level import TileWorldLevel
from puzzle_script.puzzle_script_level import PuzzleScriptLevel
from puzzle_script.puzzle_world_writer.level_set_writer import LevelSetWriter as PSLevelSetWriter
from tile_world.tile_world_writer.level_set_writer import LevelSetWriter as TWLeveSetWriter
from tile_world.tile_world_writer.tile_world_solution_writer import TileWorldSolutionWriter
from validation.solver import Solver
from generation.aesthetic_settings import AestheticSettings
from creation.creator import Creator
from log import Log
from config import ConfigReader
from ratings.ratings import Ratings

import csv
import numpy as np
import random
import subprocess

config = ConfigReader('config.json')

Log.verbose = True

ratings = Ratings(config.ratings_file)

level_count = config.level_count
if config.play_or_generate == "replay":
    level_count = ratings.level_count()

if level_count == 0:
    print("You must generate at least one level, level_count =", level_count)
    exit()

aesthetic_settings = config.aesthetic

seeds = []
for i in range(level_count):
    # We randomly choose our random seed.... why?
    # So that if we want to reproduce the level, we know what seed to use,
    # and so that we don't have to change the seed each time we run the program.
    seed = np.random.randint(1e5)
    if config.play_or_generate == "replay":
        seed = ratings.level_seed(i)
        aesthetic_settings = ratings.level_aesthetic(i)

    seeds.append(seed)

    print("Level seed: {}".format(seed))
    random.seed(seed)
    np.random.seed(seed)

    if config.engine == "PS":
        level_type = PuzzleScriptLevel
    else:
        level_type = TileWorldLevel

    level_set, quality_scores = Creator.create_level_set(level_type, aesthetic_settings, generate_level_count=config.generate_level_count, keep_level_count=config.keep_level_count, draw_graph=config.draw_graph, return_quality_scores=True)

    if config.play_or_generate == "generate":
        ratings.add_level(i, seed)

def save_tile_world_solutions(level_set, folder):
    for level in level_set.levels:
        filename = "{}\\solutions\\{}.json".format(folder, level.map_title)
        TileWorldSolutionWriter.write(filename, level.solution)


def save_quality_scores(quality_scores, folder):
    with open(folder + ".csv", "w") as file:
        csv_writer = csv.writer(file, delimiter=",")
        for quality_score in quality_scores:
            csv_writer.writerow(quality_score)
    

def rate_levels(ratings, name, seeds, aesthetic_settings, level_count):
    for i in range(level_count):
        r = input("What is your rating for level "+str(i+1)+"? (0 - 10): ")
        if r == "":
            r = 0
        ratings.add_rating(i, name, int(seeds[i]), aesthetic_settings, r)
        ratings.save()

    ratings.save()

if config.engine == 'TW':
    TWLeveSetWriter.write(level_set, config.tile_world_save_file)

    # Run TWorld
    wd = config.tile_world_loc
    subprocess.Popen("{}/tworld.exe {} --read-only".format(wd, config.tile_world_save_file), cwd=wd, shell=True)
    rate_levels(ratings, config.name, seeds, aesthetic_settings, level_count)

elif config.engine == 'CC':
    TWLeveSetWriter.write(level_set, config.tile_world_save_file)
    save_tile_world_solutions(level_set, config.super_cc_loc)
    save_quality_scores(quality_scores, config.super_cc_save_file)

    # Run SuperCC
    wd = config.super_cc_loc
    subprocess.Popen("java -jar {}/SuperCC.jar \"{}\"".format(wd, config.super_cc_save_file), cwd=wd, shell=True)

else:
    PSLevelSetWriter.write(level_set, config.puzzle_script_save_file)
    subprocess.Popen(config.puzzle_script_save_file, shell=True)

if config.ask_for_rating:
    rate_levels(ratings, config.name, seeds, level_count)

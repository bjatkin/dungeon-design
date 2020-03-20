import os
from puzzle_script.puzzle_script_level import PuzzleScriptLevel
from puzzle_script.puzzle_world_writer.level_writer import LevelWriter

# https://www.puzzlescript.net/
class LevelSetWriter:
    @staticmethod
    def write(level_set, filename):
        template = open("{}/puzzle_script/puzzle_world_writer/TileWorldBase.html".format(os.getcwd()), "r")
        tmp = template.read()

        f = open(filename, "w")

        data = ""
        for i, level in enumerate(level_set.levels):
            data = LevelWriter.write(level, i + i)

        print(data)
        tmp = tmp.replace("{{Levels}}", data)
        f.write(tmp)
        f.close()
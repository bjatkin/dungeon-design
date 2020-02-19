from puzzle_script.puzzle_script_level import PuzzleScriptLevel
from puzzle_script.puzzle_world_writer.level_writer import LevelWriter

# https://www.devdungeon.com/content/working-binary-data-python
# http://www.seasip.info/ccfile.html
class LevelSetWriter:
    @staticmethod
    def write(level_set, filename):
        f = open(filename, "w")

        data = ""
        for i, level in enumerate(level_set.levels):
            data = LevelWriter.write(level, i + i)

        print(data)
        f.write(data)
        f.close()
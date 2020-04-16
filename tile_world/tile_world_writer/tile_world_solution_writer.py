import numpy as np
import json

class TileWorldSolutionWriter:
    @staticmethod
    def convert_solution_to_json(solution):
        moves = []
        for step in solution:
            step = tuple(step)
            if step == (1,0):
                move = "d"
            elif step == (-1,0):
                move = "u"
            elif step == (0,1):
                move = "r"
            elif step == (0,-1):
                move = "l"
            moves.append(move)
        moves = "-".join(moves)

        data = {
            "Moves":moves,
            "Seed":"0",
            "Step":"EVEN"
        }
        json_data = json.dumps(data)
        return json_data

    @staticmethod
    def write(filename, solution):
        json_data = TileWorldSolutionWriter.convert_solution_to_json(solution)
        with open(filename, "w") as file:
            file.write(json_data)
        
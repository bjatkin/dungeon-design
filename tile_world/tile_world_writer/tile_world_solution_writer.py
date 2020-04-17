import numpy as np
import json

class TileWorldSolutionWriter:
    @staticmethod
    def convert_solution_to_json(solution):
        direction_to_move = { (1,0):"d", (-1,0):"u", (0,1):"r", (0,-1):"l" }
        moves = []
        for direction in solution.get_flattened_moves():
            move = direction_to_move[tuple(direction)]
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
        
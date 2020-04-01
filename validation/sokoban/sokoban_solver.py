import numpy as np
from validation.sokoban.sokomap import SokoMap, SokobanTiles
from dungeon_level.dungeon_tiles import Tiles, lock_tiles
from validation.sokoban.sokomap_hashtable import HashTable

# Sokoban Solver comes from the following repo:
# https://github.com/lrei/willy
# I just wrapped it minimally to be compatible with the rest of our code.
class SokobanSolver:
    @staticmethod
    def is_sokoban_solvable(level, player_position, sokoban_key, sokoban_lock, get_solution=False):
        sokomap = SokobanSolver.convert_level_to_sokomap(level, player_position, sokoban_lock)
        sokomap.static_deadlock()
        solution = SokobanSolver.IDAstar(sokomap, SokobanSolver.heuristic)
        is_solvable = (not solution is None)

        if get_solution:
            return is_solvable, solution.move_list
        else:
            return is_solvable
    

    @staticmethod
    def convert_level_to_sokomap(level, player_position, sokoban_lock):
        sokomap_level = np.full(level.upper_layer.shape, SokobanTiles.TILE_SPACE)
        sokomap_level[level.upper_layer == Tiles.wall] = SokobanTiles.TILE_WALL
        sokomap_level[level.upper_layer == Tiles.finish] = SokobanTiles.TILE_WALL
        for lock in lock_tiles:
            sokomap_level[level.upper_layer == lock] = SokobanTiles.TILE_WALL
        sokomap_level[level.upper_layer == Tiles.movable_block] = SokobanTiles.TILE_BLOCK

        sokomap_level[tuple(player_position)] = SokobanTiles.TILE_PLAYER
        sokomap_level[tuple(sokoban_lock)] = SokobanTiles.TILE_GOAL

        sokomap = SokoMap()
        sokomap.set_map(sokomap_level.tolist(), tuple(player_position))
        return sokomap


    @staticmethod
    def manhattan_distance(a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])


    @staticmethod
    def heuristic(sokomap):
        # generate all possible combinations of goals for each block
        solutions = []
        for block in sokomap.get_blocks():
            solution = []
            for goal in sokomap.get_goals():
                sol = ( block, goal, SokobanSolver.manhattan_distance(block, goal) )
                solution.append(sol)
            solutions.append(solution)

        # Select the best
        best = float('inf')
        for s in solutions[0]:
            used_goal = []
            used_block = []
            solution = []

            used_goal.append(s[1])
            used_block.append(s[0])
            solution.append(s)
            h = s[2]
            for lin in solutions:
                for col in lin:
                    if col[1] not in used_goal and col[0] not in used_block:
                        solution.append(col)
                        used_goal.append(col[1])
                        used_block.append(col[0])
                        h = h + col[2]
                        break
            if h < best:
                best = h
                result = solution

        w = sokomap.get_player()
        d = float('inf')
        v = (-1,-1)
        for x in sokomap.get_unplaced_blocks():
            if SokobanSolver.manhattan_distance(w, x) < d:
                d = SokobanSolver.manhattan_distance(w, x)
                v = x
        if v != (-1,-1):
            best = best + d

        return best


    @staticmethod
    def is_closed(closed_set, x):
        for y in closed_set:
            if x == y:
                return True
        return False


    @staticmethod
    def IDAstar(sokomap, h):
        open_set = []
        closed_set = []
        visit_set = []
        path_limit = h(sokomap) - 1
        sucess = False
        it = 0

        while True:
            path_limit = path_limit + 1
            sokomap.set_g(0)
            open_set.insert(0, sokomap)
            hashtable = HashTable()
            nodes = 0

            while len(open_set) > 0:
                current_state = open_set.pop(0)

                nodes = nodes + 1
                if current_state.is_solution():
                    return current_state # SOLUTION FOUND!!!

                if current_state.get_f() <= path_limit:
                    closed_set.insert(0, current_state)
                    # get the sucessors of the current state
                    for x in current_state.children():
                        # test if node has been "closed"
                        if SokobanSolver.is_closed(closed_set,x):
                            continue

                        # check if this has already been generated
                        if hashtable.check_add(x):
                            continue

                        # compute G for each
                        x.set_g(current_state.get_g() + 1)
                        x.set_f(x.get_g()+ h(x))
                        #x.setParent(current_state)
                        open_set.insert(0, x) # push
                else:
                    visit_set.insert(0, current_state)

            it = it + 1
            if len(visit_set) == 0:
                return None

            # set a new cut-off value (path_limit)
            low = visit_set[0].get_f()
            for x in visit_set:
                if x.get_f() < low:
                    low = x.get_f()
            path_limit = low

            # move nodes from VISIT to OPEN and reset closed_set
            open_set.extend(visit_set)
            visit_set = []
            closed_set = []


    @staticmethod
    def depth_first_search__scan(sokomap, h):
        open_set = [sokomap]
        hashtable = HashTable()
        hashtable.check_add(sokomap)
        nodes = 0

        while len(open_set) > 0:
            current_state = open_set.pop()

            nodes += 1
            if current_state.is_solution():
                return current_state # SOLUTION FOUND!!!

            for x in current_state.children():
                # check if this has already been generated
                if hashtable.check_add(x):
                    continue

                open_set.append(x)
        return None
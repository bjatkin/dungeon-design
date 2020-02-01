import numpy as np
from dungeon_level.dungeon_tiles import Tiles
from dungeon_level.level import Level
from hashlib import sha1
from numpy import ndarray, uint8, array


class HashableNdarray(ndarray):
    def __hash__(self):
        if not hasattr(hasattr, '__hash'):
            self.__hash = int(sha1(self.view(uint8)).hexdigest(), 16)
        return self.__hash

    def __eq__(self, other):
        if not isinstance(other, HashableNdarray):
            return super(HashableNdarray, self).__eq__(other)
        return super(HashableNdarray, self).__eq__(super(HashableNdarray, other)).all()




class PathFinder:
    diagonal_neighbor_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    neighbor_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]


    @staticmethod
    def a_star(layer, position_a, position_b, allow_diagonal=False):
        if allow_diagonal:
            offsets = PathFinder.diagonal_neighbor_offsets
            distance = PathFinder.diagonal_manhattan_distance
        else:
            offsets = PathFinder.neighbor_offsets
            distance = PathFinder.manhattan_distance


        position_a = position_a.view(HashableNdarray)
        position_b = position_b.view(HashableNdarray)

        f_costs = np.full(layer.shape, np.inf)
        g_costs = np.full(layer.shape, 0)
        h_costs = np.full(layer.shape, 0)
        parents = np.full(layer.shape, None, dtype=object)
        open_tiles = {position_a}
        closed_tiles = set()
        while True:
            if len(open_tiles) == 0: # We've searched everywhere and there is no path from a to b
                return f_costs, None

            current_position = PathFinder.find_lowest_f_cost_position(f_costs, open_tiles)
            open_tiles.remove(current_position)
            closed_tiles.add(current_position)

            if current_position == position_b: # We found a path from a to b
                return f_costs, parents

            current_g_cost = g_costs[current_position[1], current_position[0]]
            for neighbor_offset in offsets:
                neighbor_position = current_position + neighbor_offset

                if (neighbor_position in closed_tiles or
                    not PathFinder.is_traversable(layer, current_position, neighbor_position)):
                    continue

                old_f = f_costs[neighbor_position[1], neighbor_position[0]]
                f, g, h = PathFinder.calculate_costs(current_g_cost, current_position, neighbor_position, position_b, distance)


                if not neighbor_position in open_tiles or f < old_f:
                    PathFinder.update_costs(f_costs, g_costs, h_costs, f, g, h, neighbor_position)
                    parents[neighbor_position[1], neighbor_position[0]] = np.negative(neighbor_offset)
                    if not neighbor_position in open_tiles:
                        open_tiles.add(neighbor_position)


    @staticmethod
    def calculate_costs(current_g_cost, current_position, neighbor_position, position_b, distance):
        g = current_g_cost + distance(current_position, neighbor_position)
        h = distance(neighbor_position, position_b)
        f = g + h
        return f, g, h


    @staticmethod
    def update_costs(f_costs, g_costs, h_costs, f, g, h, position):
        f_costs[position[1], position[0]] = f
        g_costs[position[1], position[0]] = g
        h_costs[position[1], position[0]] = h


    @staticmethod
    def find_lowest_f_cost_position(f_cost, open_tiles):
        open_f_costs = [ ( t, f_cost[t[1], t[0]] ) for t in open_tiles]
        min_f_cost_position = min(open_f_costs, key=lambda t: t[1])[0]
        return min_f_cost_position


    nontraversable_tiles = {Tiles.movable_block, Tiles.wall, Tiles.water}
    @staticmethod
    def is_traversable(layer, current_position, neighbor_position):
        h, w = layer.shape
        is_within_bounds = neighbor_position[0] >= 0 and neighbor_position[1] >= 0 and neighbor_position[0] < w and neighbor_position[1] < h
        if not is_within_bounds:
            return False
        return layer[neighbor_position[1], neighbor_position[0]] not in PathFinder.nontraversable_tiles


    @staticmethod
    def manhattan_distance(position_a, position_b):
        return np.sum(np.abs(position_a - position_b))

    
    @staticmethod
    def diagonal_manhattan_distance(position_a, position_b):
        offset = np.abs(position_a - position_b)
        min_offset = np.min(offset)
        max_offset = np.max(offset)
        distance = min_offset * 14 + (max_offset - min_offset) * 10
        return distance
from copy import deepcopy
from enum import Enum, unique
import numpy as np

class SokobanTiles(Enum):
    TILE_BLOCK = 'B '
    TILE_GOAL = 'G '
    TILE_PLAYER = 'P '
    TILE_SPACE = '. '
    TILE_WALL = '# '
    TILE_BLOCK_ON_GOAL = 'BG'
    TILE_PLAYER_ON_GOAL = 'PG'
    TILE_DEADLOCK = 'x '
    TILE_PLAYER_ON_DEADLOCK = 'Px'


class SokoMap:
    TILES_BLOCKY = frozenset([SokobanTiles.TILE_BLOCK, SokobanTiles.TILE_BLOCK_ON_GOAL])
    TILES_WRONG_FOR_BLOCK = frozenset([SokobanTiles.TILE_BLOCK, SokobanTiles.TILE_WALL, SokobanTiles.TILE_BLOCK_ON_GOAL, SokobanTiles.TILE_DEADLOCK])
    TILES_WRONG_FOR_2x2 = frozenset([SokobanTiles.TILE_BLOCK, SokobanTiles.TILE_WALL, SokobanTiles.TILE_BLOCK_ON_GOAL])
    TILES_SPACEY = frozenset([SokobanTiles.TILE_SPACE, SokobanTiles.TILE_DEADLOCK])
    NEIGHBORS_4 = np.array([(1, 0), (-1, 0), (0, 1), (0, -1)])


    def __init__(self):
        self.sokomap = None

        self.g_val = 0
        self.f_val = 0

        self.parent = None
        self.move_list = []


    def __eq__(self, other):
        if isinstance(other, SokoMap):
            return np.all([np.array_equal(self.sokomap, other.sokomap), np.array_equal(self.player, other.player)])
        return NotImplemented


    def set_map(self, sokomap, player_position):
        self.sokomap = sokomap
        self.player = player_position


    def set_g(self, val):
        self.g_val = val


    def get_g(self):
        return self.g_val


    def set_f(self, val):
        self.f_val = val


    def get_f(self):
        return self.f_val


    def set_parent(self, parent):
        self.parent = parent


    def get_map(self):
        return self.sokomap


    def print_map(self):
        for line in self.sokomap:
            converted_line = "".join([x.value for x in line])
            print(converted_line)
        print()


    def get_something(self, something):
        return np.argwhere(self.sokomap == something)


    def _get_several_things(self, somethings):
        return np.vstack([self.get_something(x) for x in somethings])


    def get_goals(self):
        return self._get_several_things([SokobanTiles.TILE_GOAL, SokobanTiles.TILE_BLOCK_ON_GOAL])


    def get_blocks(self):
        return self._get_several_things([SokobanTiles.TILE_BLOCK, SokobanTiles.TILE_BLOCK_ON_GOAL])


    def get_unplaced_blocks(self):
        return self.get_something(SokobanTiles.TILE_BLOCK)


    def get_player(self):
        return self.player


    def get_walls(self):
        return self.get_something(SokobanTiles.TILE_WALL)


    def get_deadlocks(self):
        return self.get_something(SokobanTiles.TILE_DEADLOCK)

    
    @staticmethod
    def is_legal_position(sokomap, position):
        return not np.any(np.logical_or(position < 0, position >= sokomap.shape))


    def is_legal(self, new_player_position):
        player_position = self.get_player()

        if not self.is_legal_position(self.sokomap, new_player_position):
            return False

        if self.sokomap[tuple(new_player_position)] == SokobanTiles.TILE_WALL:
            return False # cant move into a wall

        if self.sokomap[tuple(new_player_position)] in self.TILES_BLOCKY:
            # is trying to push a block
            # the only way this works is if the space after the block is free
            # or a goal so we calculate where the block is going to be pushed
            # into and see if it's "open"

            player_diff = new_player_position - player_position

            block_position = new_player_position + player_diff

            if not SokoMap.is_legal_position(self.sokomap, block_position) or self.sokomap[tuple(block_position)] in self.TILES_WRONG_FOR_BLOCK:
                return False

            min_n_off = tuple(-player_diff)

            # Check for a segment of 2*2 adjacent blocks or walls. Like:
            #
            #      $$    #$     #$   $$
            #      ##    #$     $$   $$
            #
            def _my_check(d1, d2):
                filtered = [SokobanTiles.TILE_BLOCK_ON_GOAL if self.sokomap[tuple(block_position)] == SokobanTiles.TILE_GOAL \
                                             else SokobanTiles.TILE_BLOCK]
                for d in [d1, d2, d1 + d2]:
                    if SokoMap.is_legal_position(self.sokomap, block_position + d):
                        x = self.sokomap[tuple(block_position + d)]
                        if x in self.TILES_WRONG_FOR_2x2:
                            filtered.append(x)
                # There are 4 in total
                return (len(filtered) == 4 and (SokobanTiles.TILE_BLOCK in filtered))

            for y_offset in [(-1,0),(1,0)]:
                if ((y_offset != min_n_off) and (not (y_offset == (-1,0) and block_position[0] == 0 ))):
                    for x_offset in [(0,-1),(0,1)]:
                        if ((x_offset != min_n_off) and (not (x_offset == -1 and block_position[1] == 0 ))):
                            for dir_offsets in np.array([[x_offset,y_offset],[y_offset,x_offset]]):
                                if (_my_check(dir_offsets[0], dir_offsets[1])):
                                    return False

        # everything is OK
        return True

    
    @staticmethod
    def value_at(sokomap, position):
        if SokoMap.is_legal_position(sokomap, position):
            return sokomap[tuple(position)]
        else:
            return None



    def is_solution(self):
        unplaced_blocks = self.get_unplaced_blocks()
        return len(unplaced_blocks) == 0


    def is_block_in_tunnel(self, sokomap, block_position, push_direction):
        side = np.flip(push_direction)
        sides = np.vstack([side, -side])
        is_wall_beside_block = [SokoMap.value_at(sokomap, block_position + side) in [None, SokobanTiles.TILE_WALL] for side in sides]
        return np.all(is_wall_beside_block)


    def tunnel_macro(self, nMap, block_position, push_direction):
        original_block_position = np.array(block_position)

        while self.is_block_in_tunnel(nMap, block_position, push_direction) and SokoMap.value_at(nMap, block_position + push_direction) == SokobanTiles.TILE_SPACE:
            block_position += push_direction
        
        if not np.array_equal(block_position, original_block_position):
            # Some puzzles have multiple tunnels and require a block to pushed
            # into the tunnel and then the player to travel through another
            # tunnel and push it out of the tunnel again - credit: AJ
            # To solve that, the macro will not push the block out of the tunnel
            # but rather leave it on the edge
            block_position -= push_direction

            return block_position

        return None


    def add_move(self, m):
        self.move_list.append(m)


    def set_move_list(self, l):
        self.move_list = deepcopy(l)


    def get_move_list(self):
        return self.move_list


    def move(self, new_player_position):
        player_position = self.get_player().copy()
        new_map = self.sokomap.copy()
        block = None

        # transform the new location of the player
        player_tile = new_map[tuple(player_position)]
        if player_tile == SokobanTiles.TILE_PLAYER:
            new_map[tuple(player_position)] = SokobanTiles.TILE_SPACE
        elif player_tile == SokobanTiles.TILE_PLAYER_ON_DEADLOCK:
            new_map[tuple(player_position)] = SokobanTiles.TILE_DEADLOCK
        elif player_tile == SokobanTiles.TILE_PLAYER_ON_GOAL:
            new_map[tuple(player_position)] = SokobanTiles.TILE_GOAL

        offset = new_player_position - player_position
        carry = False
        new_player_tile = new_map[tuple(new_player_position)]
        if new_player_tile == SokobanTiles.TILE_BLOCK:
            carry = True
            new_map[tuple(new_player_position)] = SokobanTiles.TILE_SPACE
        elif new_player_tile == SokobanTiles.TILE_BLOCK_ON_GOAL:
            carry = True
            new_map[tuple(new_player_position)] = SokobanTiles.TILE_GOAL

        # push a block into a new space if necessary
        if carry:
            block_position = new_player_position + offset

            new_block_position = self.tunnel_macro(new_map, block_position, offset)
            if new_block_position is not None:
                new_player_position = new_block_position - offset
                new_map[tuple(new_player_position)] = SokobanTiles.TILE_SPACE

            # Place the block

            block_tile = new_map[tuple(block_position)]
            if block_tile == SokobanTiles.TILE_SPACE:
                new_map[tuple(block_position)] = SokobanTiles.TILE_BLOCK
            elif block_tile == SokobanTiles.TILE_GOAL:
                new_map[tuple(block_position)] = SokobanTiles.TILE_BLOCK_ON_GOAL
            else:
                pass

        new_player_tile = new_map[tuple(new_player_position)]
        if new_player_tile == SokobanTiles.TILE_SPACE:
            new_map[tuple(new_player_position)] = SokobanTiles.TILE_PLAYER
        elif new_player_tile == SokobanTiles.TILE_DEADLOCK:
            new_map[tuple(new_player_position)] = SokobanTiles.TILE_PLAYER_ON_DEADLOCK
        elif new_player_tile == SokobanTiles.TILE_GOAL:
            new_map[tuple(new_player_position)] = SokobanTiles.TILE_PLAYER_ON_GOAL

        new_sokomap = SokoMap()
        new_sokomap.set_map(new_map, new_player_position)
        new_sokomap.set_move_list(self.get_move_list())
        new_sokomap.add_move(offset)

        return new_sokomap


    def _filter_neighbors(self, position, offsets, filter):
        indices = offsets + position
        for index in indices:
            if filter(index):
                yield index


    def children(self):
        filtered_neighbors = list(self._filter_neighbors(self.get_player(), SokoMap.NEIGHBORS_4, self.is_legal))
        child_nodes = [self.move(neighbor) for neighbor in filtered_neighbors]
        return child_nodes


    def get_neighbors(self, node):
        def filter(position):
            return self.value_at(self.sokomap, position) not in {None, SokobanTiles.TILE_WALL}
        
        return self._filter_neighbors(node, SokoMap.NEIGHBORS_4, filter)


    def shortest_path(self, source, target):
        """Dijkstra's algorithm from the pseudocode in wikipedia"""
        dist = {}
        prev = {}
        q = []
        h, w = self.sokomap.shape
        for y in range(h):
            for x in range(w):
                position = (y,x)
                dist[position] = float('inf')
                prev[position] = None
                q.append(position)

        dist[source] = 0

        while len(q) != 0:
            # find the node with minimum value (u)
            d = deepcopy(dist)
            while True:
                b = dict(map(lambda item: (item[1],item[0]), d.items()))
                u = b[min(b.keys())]
                if u not in q:
                    d.pop(u)
                else:
                    break

            if dist[u] == float('inf'): # remaining nodes are inaccessible
                break

            q.remove(u)


            if u == target: # target found
                break

            for v in self.get_neighbors(u):
                alt = dist[u] + 1
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u

        s = []
        u = target
        while prev[u] is not None:
            s.append(u)
            u = prev[u]
        s.reverse()

        return s


    def build_influence_table(self):
        self.influence_table = {}

        h, w = self.sokomap.shape
        for sy in range(h):
            for sx in range(w):
                inf = {}
                if self.sokomap[sy, sx] == SokobanTiles.TILE_WALL:
                    break
                for ty in range(h):
                    for tx in range(w):
                        if self.sokomap[ty, tx] == SokobanTiles.TILE_WALL:
                            break
                        path = self.shortest_path((sy, sx), (ty, tx))
                        score = 0.0
                        for s in path:
                            (y, x) = s
                            sscore = 0.0
                            # Alternatives
                            for n in self.get_neighbors(s):
                                if n not in path:
                                    (ny, nx) = n
                                    px = nx - x
                                    py = ny - y
                                    hx = x - px
                                    hy = y - py
                                    if self.sokomap[ny, nx] == SokobanTiles.TILE_WALL:
                                        sscore = 0
                                    elif self.sokomap[hy, hx] != SokobanTiles.TILE_WALL:
                                        # "pushability" test
                                        # this tests if we can push a block from
                                        # s to n. It's an inacurate test
                                        # i.e. it's not always possible with
                                        # this condition but it will do
                                        sscore = 2
                                    else:
                                        sscore = 1
                            # Goal-Skew
                            for g in self.get_goals():
                                gpath = self.shortest_path((sy,sx), g)
                                if s in gpath:
                                    sscore /= 2
                                    break

                            # Connection
                            si = path.index(s)
                            if len(path) < si+1:
                                n = path[si+1]
                                (ny, nx) = n
                                px = nx - x
                                py = ny - y
                                hx = x - px
                                hy = y - py
                                # Same poor test for "pushability" as before
                                if self.sokomap[hy, hx] != SokobanTiles.TILE_WALL:
                                    sscore += 2
                                else:
                                    sscore += 1

                            # Tunnel
                            if si > 0:
                                (my, mx) = path[si-1]
                                px = x - mx
                                py = y - my

                                if px != 0: # horizontal push
                                    if self.sokomap[my+1, mx] == SokobanTiles.TILE_WALL and \
                                       self.sokomap[my-1, mx] == SokobanTiles.TILE_WALL:
                                        sscore = 0
                                else:   # vertical push
                                    if self.sokomap[my, mx+1] == SokobanTiles.TILE_WALL and \
                                       self.sokomap[my, mx-1] == SokobanTiles.TILE_WALL:
                                        sscore = 0

                            score += sscore
                        inf[(ty, tx)] = score
                self.influence_table[(sy, sx)] = deepcopy(inf)

        average = 0.0
        count = 0

        for k,v in self.influence_table:
            for kk, vv in v:
                count += 1
                average += vv

        average /= count
        if average < 6:
            self.influence_thresh = 6
        else:
            self.influence_thresh = average

        self.influence_history = 10




    class DirectView:
        def __init__(self, sokomap):
            self.sokomap = sokomap


        def get(self, y, x):
            return self.sokomap[y, x]


        def set(self, y, x, val):
            self.sokomap[y, x] = val
            return


        def y_len(self):
            return self.sokomap.shape[0]


        def x_len(self):
            return self.sokomap.shape[1]



    class Swap_XY_View:
        def __init__(self, sokomap):
            self.sokomap = sokomap


        def get(self, y, x):
            return self.sokomap[x, y]


        def set(self, y, x, val):
            self.sokomap[x, y] = val
            return


        def y_len(self):
            return self.sokomap.shape[1]


        def x_len(self):
            return self.sokomap.shape[0]



    def static_deadlock(self):
        """Detects fixed deadlocks (very basic, not perfect"""

        def _place_deadlock(y,x,delta_y,delta_x):
            if (self.value_at(self.sokomap, np.array([y + delta_y, x])) == SokobanTiles.TILE_WALL and
                    self.value_at(self.sokomap, np.array([y, x + delta_x])) == SokobanTiles.TILE_WALL):
                self.sokomap[y, x] = SokobanTiles.TILE_DEADLOCK
                return True
            else:
                return False

        # Place _deadlock Markers in corners (without goals)
        h, w = self.sokomap.shape
        for y in range(h):
            for x in range(w):
                if x == 0 or x == (len(self.sokomap[0])-1) or \
                   y == 0 or (y == len(self.sokomap)-1):
                    continue
                if self.sokomap[y, x] == SokobanTiles.TILE_SPACE:
                    _place_deadlock(y,x,-1,-1) or \
                    _place_deadlock(y,x,-1,1) or \
                    _place_deadlock(y,x,1,-1) or \
                    _place_deadlock(y,x,1,1)


        # Connect _deadlock Markers if they next to a contin. wall w/o goals
        def connect_markers(dy,dx, view):
            up = True
            down = True
            found = False
            x = dx

            while x > 1:
                x -= 1
                try:
                    if view.get(dy,x) == SokobanTiles.TILE_DEADLOCK:
                        found = True
                        break
                except IndexError:
                    break

            if found:
                sx = x
                while x != dx:
                    x += 1
                    try:
                        if view.get(dy+1,x) != SokobanTiles.TILE_WALL and down:
                            down = False
                    except IndexError:
                        down = False
                    try:
                        if view.get(dy-1,x) != SokobanTiles.TILE_WALL and up:
                            up = False
                    except IndexError:
                        up = False
                    try:
                        if not view.get(dy,x) in self.TILES_SPACEY:
                            up = down = False
                    except IndexError:
                        down = up = False

                if up or down:
                    x = sx
                    while x != dx:
                        val = view.get(dy,x)
                        if val == SokobanTiles.TILE_SPACE:
                            view.set(dy,x, SokobanTiles.TILE_DEADLOCK)
                        x += 1

        xy_v = self.DirectView(self.sokomap)
        yx_v = self.Swap_XY_View(self.sokomap)
        for dead in self.get_deadlocks():
            (dy,dx) = dead
            connect_markers(dy, dx, xy_v)
            connect_markers(dx, dy, yx_v)
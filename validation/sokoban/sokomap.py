from copy import deepcopy
from enum import Enum, unique

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


    def __init__(self):
        self.sokomap = []

        self.g_val = 0
        self.f_val = 0

        self.parent = None
        self.move_list = []


    def __eq__(self, other):
        if isinstance(other, SokoMap):
            return (self.sokomap == other.sokomap and self.player == other.player)
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
        return self.g_val


    def set_parent(self, parent):
        self.parent = parent


    def read_map(self, filename):
        # read from txt map file
        map_file = open(filename, 'r')
        temp = map_file.readlines()
        sokomap = [] # in memory map representation: list of lists of chars
        y = 0
        player = None
        for line in temp:
            base_l = list(line)[0:-1] # removes newline
            l = []
            for x in range(0,len(base_l)):
                c = base_l[x]
                if c == SokobanTiles.TILE_PLAYER:
                    c = SokobanTiles.TILE_SPACE
                    player = (x,y)
                elif c == SokobanTiles.TILE_PLAYER_ON_GOAL:
                    c = SokobanTiles.TILE_GOAL
                    player = (x,y)
                elif c == SokobanTiles.TILE_PLAYER_ON_DEADLOCK:
                    c = SokobanTiles.TILE_DEADLOCK
                    player = (x,y)
                l.append(c)
            sokomap.append(l)
            y += 1

        while sokomap[-1] == ['\n'] or sokomap[-1] == []:
             # remove last "line" (empty, original only had a newline)
            sokomap.pop()

        self.set_map(sokomap, player)


    def get_map(self):
        return self.sokomap


    def print_map(self):
        for line in self.sokomap:
            converted_line = "".join([x.value for x in line])
            print(converted_line)


    def get_something(self, something):
        result = []
        y = 0
        for l in self.sokomap:
            x = 0
            for i in l:
                if i == something:
                    result.append((x,y))
                x += 1
            y += 1

        return result


    def _get_several_things(self, somethings):
        total = []
        for thing in somethings:
            total.extend(self.get_something(thing))
        return total


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


    def is_legal(self, nplayer):
        (nx, ny) = nplayer
        (x, y) = self.get_player()

        if nx < 0 or ny < 0 or ny >= len(self.sokomap) or nx >= len(self.sokomap[ny]):
            return False

        if self.sokomap[ny][nx] == SokobanTiles.TILE_WALL:
            return False # cant move into a wall

        if self.sokomap[ny][nx] in self.TILES_BLOCKY:
            # is trying to push a block
            # the only way this works is if the space after the block is free
            # or a goal so we calculate where the block is going to be pushed
            # into and see if it's "open"

            xdiff = nx - x
            ydiff = ny - y

            bx = nx + xdiff
            by = ny + ydiff

            if self.sokomap[by][bx] in self.TILES_WRONG_FOR_BLOCK:
                return False

            min_n_off = (-ydiff,-xdiff)

            # Check for a segment of 2*2 adjacent blocks or walls. Like:
            #
            #      $$    #$     #$   $$
            #      ##    #$     $$   $$
            #
            def _my_check(dy1,dx1,dy2,dx2):
                filtered = [SokobanTiles.TILE_BLOCK_ON_GOAL if self.sokomap[by][bx] == SokobanTiles.TILE_GOAL \
                                             else SokobanTiles.TILE_BLOCK]
                for (dy,dx) in [(dy1,dx1),(dy2,dx2),(dy1+dy2,dx1+dx2)]:
                    x = self.sokomap[by+dy][bx+dx]
                    if x in self.TILES_WRONG_FOR_2x2:
                        filtered.append(x)
                # There are 4 in total
                return (len(filtered) == 4 and (SokobanTiles.TILE_BLOCK in filtered))

            for y_offset in [(-1,0),(1,0)]:
                if ((y_offset != min_n_off) and (not (y_offset == (-1,0) and by == 0 ))):
                    for x_offset in [(0,-1),(0,1)]:
                        if ((x_offset != min_n_off) and (not (x_offset == -1 and bx == 0 ))):
                            for dir_offsets in [\
                                    (x_offset,y_offset), \
                                    (y_offset,x_offset) \
                                    ]:
                                if (_my_check(dir_offsets[0][0], dir_offsets[0][1], dir_offsets[1][0], dir_offsets[1][1])):
                                    return False

        # everything is OK
        return True


    def is_solution(self):
        unplaced_blocks = self.get_unplaced_blocks()
        return len(unplaced_blocks) == 0


    def tunnel_macro(self, nMap, box, push):
        (px, py) = push
        (bx, by) = box

        if px != 0:
            # horizontal push
            while nMap[by+1][bx] == SokobanTiles.TILE_WALL and nMap[by-1][bx] == SokobanTiles.TILE_WALL:
                if nMap[by][bx+1] != SokobanTiles.TILE_SPACE:
                    return None
                bx = bx + 1
        if py != 0:
            # vertical push
            while nMap[by][bx+1] == SokobanTiles.TILE_WALL and nMap[by][bx-1] == SokobanTiles.TILE_WALL:
                if nMap[by+1][bx] != SokobanTiles.TILE_SPACE:
                    return None
                by = by + 1

        if (bx, by) != box:
            # Some puzzles have multiple tunnels and require a box to pushed
            # into the tunnel and then the player to travel through another
            # tunnel and push it out of the tunnel again - credit: AJ
            # To solve that, the macro will not push the box out of the tunnel
            # but rather leave it on the edge
            bx -= px
            by -= py

            return (bx, by)

        return None


    def add_move(self, m):
        self.move_list.append(m)


    def set_move_list(self, l):
        self.move_list = deepcopy(l)


    def get_move_list(self):
        return self.move_list


    def move(self, nplayer):
        (x,y) = self.get_player()
        new_map = deepcopy(self.sokomap)
        box = None

        # transform the new location of the player
        if new_map[y][x] == SokobanTiles.TILE_PLAYER:
            new_map[y][x] = SokobanTiles.TILE_SPACE
        elif new_map[y][x] == SokobanTiles.TILE_PLAYER_ON_DEADLOCK:
            new_map[y][x] = SokobanTiles.TILE_DEADLOCK
        elif new_map[y][x] == SokobanTiles.TILE_PLAYER_ON_GOAL:
            new_map[y][x] = SokobanTiles.TILE_GOAL

        (nx,ny) = nplayer
        xdiff = nx - x
        ydiff = ny - y
        m = (xdiff, ydiff)
        carry = False
        if new_map[ny][nx] == SokobanTiles.TILE_BLOCK:
            carry = True
            new_map[ny][nx] = SokobanTiles.TILE_SPACE
        elif new_map[ny][nx] == SokobanTiles.TILE_BLOCK_ON_GOAL:
            carry = True
            new_map[ny][nx] = SokobanTiles.TILE_GOAL

        # push a block into a new space if necessary
        if carry:
            bx = nx + xdiff
            by = ny + ydiff

            box = self.tunnel_macro(new_map, (bx, by), m)
            #box = None
            if box is not None:
                (bx, by) = box

                nx = bx - xdiff
                ny = by - ydiff
                # it must be a space (that's checked inside tunnel_macro)

                new_map[ny][nx] = SokobanTiles.TILE_SPACE

            # Place the box
            if new_map[by][bx] == SokobanTiles.TILE_SPACE:
                new_map[by][bx] = SokobanTiles.TILE_BLOCK
            elif new_map[by][bx] == SokobanTiles.TILE_GOAL:
                new_map[by][bx] = SokobanTiles.TILE_BLOCK_ON_GOAL
            else:
                pass

        if new_map[ny][nx] == SokobanTiles.TILE_SPACE:
            new_map[ny][nx] = SokobanTiles.TILE_PLAYER
        elif new_map[ny][nx] == SokobanTiles.TILE_DEADLOCK :
            new_map[ny][nx] = SokobanTiles.TILE_PLAYER_ON_DEADLOCK
        elif new_map[ny][nx] == SokobanTiles.TILE_GOAL:
            new_map[ny][nx] = SokobanTiles.TILE_PLAYER_ON_GOAL
        

        new_sokomap = SokoMap()
        new_sokomap.set_map(new_map, (nx, ny))
        new_sokomap.set_move_list(self.get_move_list())
        new_sokomap.add_move(m)

        return new_sokomap


    def _filter_neighbours(self, xy, offsets, filt):
        x, y = xy
        for (dx,dy) in offsets:
            nxy = (x+dx,y+dy)
            if (filt(nxy)):
                yield nxy


    def children(self):
        return [self.move(nxy) for nxy in self._filter_neighbours(self.get_player(), [(0,-1),(0,1),(-1,0),(1,0)], (lambda nxy: self.is_legal(nxy)))]


    def get_neighbors(self, node):
        def filt(nx,ny):
            try:
                return ny >= 0 and nx >= 0 and self.sokomap[ny][nx] != SokobanTiles.TILE_WALL
            except IndexError:
                return False

        return self._filter_neighbours(node, [(1,0),(-1,0),(0,1),(0,-1)], filt)


    def shortest_path(self, source, target):
        """Dijkstra's algorithm from the pseudocode in wikipedia"""
        dist = {}
        prev = {}
        q = []
        for y,a in enumerate(self.sokomap):
             for x,b in enumerate(self.sokomap[y]):
                 dist[(x,y)] = float('inf')
                 prev[(x,y)] = None
                 q.append((x,y))
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
        for sy,a in enumerate(self.sokomap):
            for sx,b in enumerate(self.sokomap[sy]):
                inf = {}
                if self.sokomap[sy][sx] == SokobanTiles.TILE_WALL:
                    break
                for ty,a in enumerate(self.sokomap):
                    for tx,b in enumerate(self.sokomap[ty]):
                        if self.sokomap[ty][tx] == SokobanTiles.TILE_WALL:
                            break
                        path = self.shortest_path((sx, sy), (tx, ty))
                        score = 0.0
                        for s in path:
                            (x, y) = s
                            sscore = 0.0
                            # Alternatives
                            for n in self.get_neighbors(s):
                                if n not in path:
                                    (nx, ny) = n
                                    px = nx - x
                                    py = ny - y
                                    hx = x - px
                                    hy = y - py
                                    if self.sokomap[ny][nx] == SokobanTiles.TILE_WALL:
                                        sscore = 0
                                    elif self.sokomap[hy][hx] != SokobanTiles.TILE_WALL:
                                        # "pushability" test
                                        # this tests if we can push a box from
                                        # s to n. It's an inacurate test
                                        # i.e. it's not always possible with
                                        # this condition but it will do
                                        sscore = 2
                                    else:
                                        sscore = 1
                            # Goal-Skew
                            for g in self.get_goals():
                                gpath = self.shortest_path((sx,sy), g)
                                if s in gpath:
                                    sscore /= 2
                                    break

                            # Connection
                            si = path.index(s)
                            if len(path) < si+1:
                                n = path[si+1]
                                (nx, ny) = n
                                px = nx - x
                                py = ny - y
                                hx = x - px
                                hy = y - py
                                # Same poor test for "pushability" as before
                                if self.sokomap[hy][hx] != SokobanTiles.TILE_WALL:
                                    sscore += 2
                                else:
                                    sscore += 1

                            # Tunnel
                            if si > 0:
                                (mx, my) = path[si-1]
                                px = x - mx
                                py = y - my

                                if px != 0: # horizontal push
                                    if self.sokomap[my+1][mx] == SokobanTiles.TILE_WALL and \
                                       self.sokomap[my-1][mx] == SokobanTiles.TILE_WALL:
                                        sscore = 0
                                else:   # vertical push
                                    if self.sokomap[my][mx+1] == SokobanTiles.TILE_WALL and \
                                       self.sokomap[my][mx-1] == SokobanTiles.TILE_WALL:
                                        sscore = 0

                            score += sscore
                        inf[(tx, ty)] = score
                self.influence_table[(sx, sy)] = deepcopy(inf)

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
            return self.sokomap[y][x]


        def set(self, y, x, val):
            self.sokomap[y][x] = val
            return


        def y_len(self):
            return len(self.sokomap)


        def x_len(self):
            return max([row.len for row in self.sokomap])




    class Proxy_View:
        def __init__(self, v):
            self.v = v

        def _map(self, y, x):
            return y, x


        def get(self, y, x):
            return self.v.get(*self._map(y, x))


        def set(self, y, x, val):
            return self.v.set(*self._map(y, x), val)


        def y_len(self):
            return self.v.y_len()


        def x_len(self):
            return self.v.x_len()




    class Swap_XY_View(Proxy_View):
        def _map(self, y, x):
            return x,y


        def y_len(self):
            return self.v.x_len()


        def x_len(self):
            return self.v.y_len()



    def static_deadlock(self):
        """Detects fixed deadlocks (very basic, not perfect"""

        def _place_deadlock(y,x,delta_y,delta_x):
            try:
                if self.sokomap[y+delta_y][x] == SokobanTiles.TILE_WALL and \
                   self.sokomap[y][x+delta_x] == SokobanTiles.TILE_WALL:
                    self.sokomap[y][x] = SokobanTiles.TILE_DEADLOCK
                    return True
            except IndexError:
                pass
            return False

        # Place _deadlock Markers in corners (without goals)
        for y,a in enumerate(self.sokomap):
            for x,b in enumerate(self.sokomap[y]):
                if x == 0 or x == (len(self.sokomap[0])-1) or \
                   y == 0 or (y == len(self.sokomap)-1):
                    continue
                if self.sokomap[y][x] == SokobanTiles.TILE_SPACE:
                    _place_deadlock(y,x,-1,-1) or \
                    _place_deadlock(y,x,-1,1) or \
                    _place_deadlock(y,x,1,-1) or \
                    _place_deadlock(y,x,1,1)


        # Connect _deadlock Markers if they next to a contin. wall w/o goals
        def connect_markers(dx,dy, view):
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
        yx_v = self.Swap_XY_View(xy_v)
        for dead in self.get_deadlocks():
            (dx,dy) = dead
            connect_markers(dx, dy, xy_v)
            connect_markers(dy, dx, yx_v)
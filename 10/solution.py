#!/usr/bin/env python3
from collections import defaultdict
from collections.abc import Mapping
from tools.colors import *

ONLY_PIPES = False
ONLY_LOOPS = False

class MazeTile:
    def __init__(self, x: int, y: int, symbol: str, looped = False):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.looped = looped
        self.outside = False
        self.inside = False
    
    def __str__(self):
        # print(repr(self))
        color = Color.GREY
        s = self.symbol
        if self.symbol == 'S':
            color = Color.RED
        elif self.looped:
            color = Color.GREEN
        elif self.outside:
            color = Color.GREY
            s = ' ' if ONLY_LOOPS else 'O'
        elif self.inside:
            color = Color.WHITE
            s = ' ' if ONLY_LOOPS else 'I'
        elif self.symbol in '|-LJ7F':
            color = Color.GREY if ONLY_PIPES else Color.WHITE
            s = ' ' if ONLY_LOOPS else self.symbol
        elif ONLY_PIPES or ONLY_LOOPS:
            s = ' '
        return highlight(color, s)

    def __repr__(self):
        return f'{self.symbol}@({self.x}, {self.y}){"T" if self.looped else "F"}'

    def _neighbors(self, maze: 'Maze') -> list[tuple[int, int]]:
        x, y = self.x, self.y
        possible = [(x, y-1), (x-1, y), (x, y+1), (x+1, y)]
        possible = filter(lambda p: (p[0] > -1 and p[0] < maze.width and (p[1] > -1 and p[1] < maze.height)), possible)
        return list(possible)

    def neighbors(self, maze: 'Maze') -> list['MazeTile']:
        return list(map(lambda p: maze.get_tile(p[0], p[1]), self._neighbors(maze)))

    def next_tile(self, maze: 'Maze', from_tile: 'MazeTile') -> 'MazeTile':
        x = self.x - from_tile.x
        y = self.y - from_tile.y
        should_move_to = (self.x, self.y)
        if x == 0 and y == 1: # headed down
            if self.symbol == '|':
                should_move_to = (self.x, self.y + 1)
            elif self.symbol == 'L':
                should_move_to = (self.x + 1, self.y)
            elif self.symbol == 'J':
                should_move_to = (self.x - 1, self.y)
            else:
                assert False, 'Invalid Path'
        elif x == 0 and y == -1: # headed up
            if self.symbol == '|':
                should_move_to = (self.x, self.y - 1)
            elif self.symbol == 'F':
                should_move_to = (self.x + 1, self.y)
            elif self.symbol == '7':
                should_move_to = (self.x - 1, self.y)
            else:
                assert False, 'Invalid Path'
        elif x == -1 and y == 0: # headed left
            if self.symbol == '-':
                should_move_to = (self.x - 1, self.y)
            elif self.symbol == 'F':
                should_move_to = (self.x, self.y + 1)
            elif self.symbol == 'L':
                should_move_to = (self.x, self.y - 1)
            else:
                assert False, 'Invalid Path'
        elif x == 1 and y == 0: # headed right
            if self.symbol == '-':
                should_move_to = (self.x + 1, self.y)
            elif self.symbol == 'J':
                should_move_to = (self.x, self.y - 1)
            elif self.symbol == '7':
                should_move_to = (self.x, self.y + 1)
            else:
                assert False, 'Invalid Path'
        else:
            assert repr(self)

        return maze.get_tile(should_move_to[0], should_move_to[1])

    '''
    s 1 2 3 4 5 t
    -------------
    f c n - - - t
    s f c n - - t
    s - f c n - t
    s - - f c n t
    s - - - f c n
    '''
    def find_target(self, maze: 'Maze', from_tile: 'MazeTile', target: 'MazeTile') -> list['MazeTile']:
        try:
            current_tile = self
            next_tile = current_tile.next_tile(maze, from_tile)
            path: list['MazeTile'] = []
            path.append(current_tile)
            while next_tile != target:
                from_tile = current_tile
                current_tile = next_tile
                next_tile = current_tile.next_tile(maze, from_tile)
                path.append(current_tile)
            return path
        except:
            return []

    # helper function because you can't assign variables in a map()
    def set_looped(self, is_looped: bool) -> 'MazeTile':
        self.looped = is_looped
        return self

    def find_loop(self, maze: 'Maze') -> list['MazeTile']:
        assert self.symbol == 'S'
        self.looped = True
        possible: Mapping[tuple[int, int], 'MazeTile'] = map(lambda p: maze.get_tile(p[0], p[1]), self._neighbors(maze))
        possible_pipes: list['MazeTile'] = list(filter(lambda tile: tile.symbol != '.', possible))
        for tile in possible_pipes:
            path = tile.find_target(maze, self, self)
            if path:
                path = list(map(lambda x: x.set_looped(True), path))
                return path
        return []

    def _looped_tiles(self, maze: 'Maze') -> list['MazeTile']:
        possible_tiles = []

        y = self.y
        for x in range(maze.width):
            try:
                possible_tiles.append(maze.get_tile(x, y))
            except:
                pass

        x = self.x
        for y in range(maze.height):
            try:
                possible_tiles.append(maze.get_tile(x, y))
            except:
                pass

        return list(filter(lambda tile: tile != self and tile.looped, possible_tiles))

    def is_enclosed(self, maze: 'Maze') -> bool:
        looped_tiles = self._looped_tiles(maze)
        num_to_left_wall = len(list(filter(lambda tile: tile.x < self.x, looped_tiles)))
        num_to_right_wall = len(list(filter(lambda tile: tile.x > self.x, looped_tiles)))
        num_to_down_wall = len(list(filter(lambda tile: tile.y > self.y, looped_tiles)))
        num_to_up_wall = len(list(filter(lambda tile: tile.y < self.y, looped_tiles)))

        return bool(num_to_left_wall) and bool(num_to_right_wall) and bool(num_to_down_wall) and bool(num_to_up_wall)

    def is_outside(self, maze: 'Maze') -> bool:
        return not self.is_enclosed(maze)

    def find_group(self, maze: 'Maze') -> list['MazeTile']:
        if self.looped:
            return []
        group: list['MazeTile'] = []
        to_visit: list['MazeTile'] = [self]
        visited: list['MazeTile'] = [self]
        while len(to_visit) > 0:
            # print('.', end='', flush=True)
            # print(len(group), len(to_visit), len(visited), maze.width * maze.height)
            # print(len(to_visit))
            tile = to_visit.pop(0)
            visited.append(tile)
            if tile.looped:
                continue
            group.append(tile)
            for neighbor in tile.neighbors(maze):
                if not neighbor.looped and neighbor not in visited and neighbor not in to_visit:
                    to_visit.append(neighbor)
                    # print(neighbor, to_visit)
        # print('')
        # if not self.is_enclosed(maze):
        for tile in group:
            tile.outside = not self.is_enclosed(maze)
            tile.inside = self.is_enclosed(maze)
        return group

class Maze:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.maze: dict[tuple[int, int], MazeTile] = defaultdict(lambda: MazeTile(-1, -1, '.'))
        self.starting: MazeTile = self.get_tile(0, 0)
    
    def __str__(self):
        output = []
        for y in range(self.height):
            output.append(''.join([str(self.maze[(x,y)]) for x in range(self.width)]))
        return '\n'.join(output)

    def __repr__(self):
        return str(self)
    
    def get_tile(self, x: int, y: int) -> MazeTile:
        assert x > -1 and x < self.width and y > -1 and y < self.height, 'Out of bounds'
        return self.maze[(x,y)]
    
    def set_tile(self, x: int, y: int, s: str) -> MazeTile:
        tile = self.get_tile(x, y)
        tile.x = x
        tile.y = y
        tile.symbol = s
        if s == 'S':
            self.starting = tile
        return tile

    def find_outside(self) -> int:
        to_visit = []#list(self.maze.values())
        for y in range(self.height):
            for x in range(self.width):
                to_visit.append(self.maze[(x, y)])
        # for k,v in list(self.maze.items()):
        #     print(k, repr(v))
        while len(to_visit) > 0:
            # print('.', end='', flush=True)
            # print(len(to_visit))
            tile = to_visit.pop(0)
            if tile.looped:
                continue
            group = tile.find_group(self)
            for t in group:
                # print(t)
                if t in to_visit:
                    to_visit.remove(t)
                if t.is_outside(self):
                    t.outside = True
        # print('')
        count = 0
        for tile in self.maze.values():
            if not tile.outside and not tile.looped:
                count += 1
        return count

    def find_outside2(self) -> int:
        loop = self.starting.find_loop(self)
        # print(self)
        # print('expand')
        self.expand()
        # print(self)
        # print('find_outside')
        self.find_outside()
        # print(self)
        # print('contract')
        self.contract()
        count = 0
        for tile in self.maze.values():
            if not tile.outside and not tile.looped:
                count += 1
        # print(self)
        return count

    def expand(self):
        new_width = 2 * self.width
        new_height = 2 * self.height
        new_maze: dict[tuple[int, int], MazeTile] = defaultdict(lambda: MazeTile(-1, -1, '.'))
        for y in range(new_height):
            for x in range(new_width):
                # print(x, y, x//2, y//2)
                if x % 2 == 0 and y % 2 == 0:
                    tile = self.get_tile(x//2, y//2)
                    # print(x, y, repr(tile))
                    tile.x = x
                    tile.y = y
                    new_maze[(x,y)] = tile
                    if not tile.looped:
                        continue
                    if tile.symbol in '-7J':
                        ltile = new_maze[(tile.x - 1, tile.y)]
                        ltile.symbol = '-'
                        ltile.looped = True
                    if tile.symbol in '-FL':
                        rtile = new_maze[(tile.x + 1, tile.y)]
                        rtile.symbol = '-'
                        rtile.looped = True
                    if tile.symbol in '|JL':
                        utile = new_maze[(tile.x, tile.y - 1)]
                        utile.symbol = '|'
                        utile.looped = True
                    if tile.symbol in '|F7':
                        dtile = new_maze[(tile.x, tile.y + 1)]
                        dtile.symbol = '|'
                        dtile.looped = True
                else:
                    tile = new_maze[(x, y)]
                    tile.x = x
                    tile.y = y

        self.maze = new_maze
        self.width = new_width
        self.height = new_height

    def contract(self):
        new_width = self.width // 2
        new_height = self.height // 2
        new_maze: dict[tuple[int, int], MazeTile] = defaultdict(lambda: MazeTile(-1, -1, '.'))
        for y in range(new_height):
            for x in range(new_width):
                new_maze[(x, y)] = self.maze[(x*2, y*2)]
        self.maze = new_maze
        self.width = new_width
        self.height = new_height

def parse(my_input: list[str]) -> Maze:
    maze = Maze(len(my_input[0] if len(my_input) else 0), len(my_input))
    for y, line in enumerate(my_input):
        try:
            for x, symbol in enumerate(line):
                tile = maze.set_tile(x, y, symbol)
                # print(tile)
        except BaseException as e:
            print(line)
            raise e
    # print(maze)
    return maze

def solution1(my_input: list[str]) -> int:
    maze = parse(my_input)
    loop = maze.starting.find_loop(maze)
    # print(maze)
    return len(loop) // 2 + 1

def solution2(my_input: list[str]) -> int:
    maze = parse(my_input)
    loop = maze.starting.find_loop(maze)
    # outside = maze.find_outside()
    print(str(maze) + '\n')
    num_inside = maze.find_outside2()
    print(maze)
    return num_inside

if __name__ == '__main__':
    for part in [1, 2]:
    # for part in [2]:
        print(f"---- Part { 'One' if part == 1 else 'Two' } ----")
        for file in ['simple.txt', 'complex.txt', 'cluttered.txt', 'sample.txt', 'loop.txt', 'closed_loop.txt', 'larger.txt', 'sample2.txt', 'input.txt']:
        # for file in ['simple.txt', 'input.txt']:
            print(f'-- {file} --')
            print(str(eval(f'solution{part}')(open(file, 'r').read().split('\n'))))
            text = input('continue? ')
            if text:
                break
        if text:
            break

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
    
    def __str__(self):
        # print(repr(self))
        color = Color.GREY
        s = self.symbol
        if self.symbol == 'S':
            color = Color.RED
        elif self.looped:
            color = Color.GREEN
        elif self.symbol in '|-LJ7F':
            color = Color.GREY if ONLY_PIPES else Color.WHITE
            s = ' ' if ONLY_LOOPS else self.symbol
        elif ONLY_PIPES or ONLY_LOOPS:
            s = ' '
        return highlight(color, s)

    def __repr__(self):
        return f'{self.symbol}@({self.x}, {self.y})'

    def _neighbors(self, maze: 'Maze') -> list[tuple[int, int]]:
        x, y = self.x, self.y
        possible = [(x, y-1), (x-1, y), (x, y+1), (x+1, y)]
        possible = filter(lambda p: (p[0] > -1 and p[0] < maze.width and (p[1] > -1 and p[1] < maze.height)), possible)
        return list(possible)

    def find_target(self, maze: 'Maze', from_tile: 'MazeTile', target: 'MazeTile') -> list['MazeTile']:
        x = self.x - from_tile.x
        y = self.y - from_tile.y
        print(repr(self), x, y)
        if x == 0 and y == 1: # headed down
            if self.symbol == '|':
                should_move_to = (self.x, self.y + 1)
            elif self.symbol == 'L':
                should_move_to = (self.x + 1, self.y)
            elif self.symbol == 'J':
                should_move_to = (self.x - 1, self.y)
            else:
                print(f'Tried to go {self.symbol} from {repr(from_tile)}')
                assert False, 'Invalid Path'
        elif x == 0 and y == -1: # headed up
            if self.symbol == '|':
                should_move_to = (self.x, self.y - 1)
            elif self.symbol == 'F':
                should_move_to = (self.x + 1, self.y)
            elif self.symbol == '7':
                should_move_to = (self.x - 1, self.y)
            else:
                print(f'Tried to go {self.symbol} from {repr(from_tile)}')
                return []
        elif x == -1 and y == 0: # headed left
            if self.symbol == '-':
                should_move_to = (self.x - 1, self.y)
            elif self.symbol == 'F':
                should_move_to = (self.x, self.y + 1)
            elif self.symbol == 'L':
                should_move_to = (self.x, self.y - 1)
            else:
                print(f'Tried to go {self.symbol} from {repr(from_tile)}')
                return []
        elif x == 1 and y == 0: # headed right
            if self.symbol == '-':
                should_move_to = (self.x + 1, self.y)
            elif self.symbol == 'J':
                should_move_to = (self.x, self.y - 1)
            elif self.symbol == '7':
                should_move_to = (self.x, self.y + 1)
            else:
                print(f'Tried to go {self.symbol} from {repr(from_tile)}')
                return []
        else:
            assert repr(self)

        try:
            next_tile = maze.get_tile(should_move_to[0], should_move_to[1])
        except:
            return []
        
        if next_tile == target:
            self.looped = True
            return [self]
        
        path = next_tile.find_target(maze, self, target)
        if path:
            self.looped = True
            return [self] + path

        return []

    def find_loop(self, maze: 'Maze') -> list['MazeTile']:
        assert self.symbol == 'S'
        print(repr(self))
        possible: Mapping[tuple[int, int], 'MazeTile'] = map(lambda p: maze.get_tile(p[0], p[1]), self._neighbors(maze))
        possible_pipes: list['MazeTile'] = list(filter(lambda tile: tile.symbol != '.', possible))
        for tile in possible_pipes:
            path = tile.find_target(maze, self, self)
            if path:
                return path
        return []

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
    print(maze)
    maze.starting.find_loop(maze)
    print(maze)
    return maze

def solution1(my_input: list[str]) -> int:
    maze = parse(my_input)
    print(maze)
    return -1 # TODO

def solution2(my_input: list[str]) -> int:
    maze = parse(my_input)
    return -1 # TODO

if __name__ == '__main__':
    for part in [1, 2]:
        print(f"---- Part { 'One' if part == 1 else 'Two' } ----")
        for file in ['simple.txt', 'complex.txt', 'cluttered.txt', 'sample.txt', 'input.txt']:
            print(f'-- {file} --')
            print(str(eval(f'solution{part}')(open(file, 'r').read().split('\n'))))
            text = input('continue? ')
            if text:
                break
        if text:
            break

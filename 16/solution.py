#!/usr/bin/env python3
from tools.colors import *
from tools.position import Position
from enum import Enum

class GridTile(Position):
    def __init__(self, x: int, y: int, symbol: str):
        assert symbol in '/\\|-.', symbol
        super().__init__(x, y)
        self.symbol = symbol

    def __str__(self) -> str:
        return self.symbol
    
    def __repr__(self) -> str:
        return f'{self.symbol}@({self.x}, {self.y})'

    def process_beam(self, move_direction: str) -> list[Position]:
        assert move_direction in ['north', 'south', 'east', 'west']
        if self.symbol == '.':
            return [eval(f'self.{move_direction}()')]
        if self.symbol == '/':
            if move_direction == 'north':
                return [self.east()]
            if move_direction == 'south':
                return [self.west()]
            if move_direction == 'east':
                return [self.north()]
            if move_direction == 'west':
                return [self.south()]
        if self.symbol == '\\':
            if move_direction == 'north':
                return [self.west()]
            if move_direction == 'south':
                return [self.east()]
            if move_direction == 'east':
                return [self.south()]
            if move_direction == 'west':
                return [self.north()]
        if self.symbol == '-':
            if move_direction in ['east', 'west']:
                return [eval(f'self.{move_direction}()')]
            if move_direction in ['north', 'south']:
                return [self.east(), self.west()]
        if self.symbol == '|':
            if move_direction in ['north', 'south']:
                return [eval(f'self.{move_direction}()')]
            if move_direction in ['east', 'west']:
                return [self.north(), self.south()]
        assert f'How did I get here? {self.symbol}'

    def move_from(self, other: 'GridTile') -> list[Position]:
        o = other.to_tuple()
        if self.north() == o:
            move_direction = 'south'
        elif self.south() == o:
            move_direction = 'north'
        elif self.east() == o:
            move_direction = 'west'
        elif self.west() == o:
            move_direction = 'east'
        else:
            assert False, f'Should not be able to get here ({repr(self)}) from {repr(other)}'
        return self.process_beam(move_direction)

class Pairing:
    def __init__(self, from_tile: 'GridTile', to_tile: 'GridTile'):
        self.from_tile = from_tile
        self.to_tile = to_tile

    def __str__(self) -> str:
        return f'{repr(self.from_tile)} -> {repr(self.to_tile)}'
    
    def __repr__(self) -> str:
        return str((self.from_tile.to_tuple(), self.to_tile.to_tuple()))
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pairing):
            return NotImplemented
        return repr(self) == repr(other)
    
class Grid:
    def __init__(self, grid_tiles: list[list[GridTile]]):
        self.grid_tiles = grid_tiles

    def __str__(self) -> str:
        lines: list[str] = []
        for row in self.grid_tiles:
            line = ''
            for col in row:
                line += str(col)
            lines.append(line)
        return '\n'.join(lines)

    def get(self, x: int, y: int) -> GridTile:
        assert self.in_bounds(x, y)
        return self.grid_tiles[y][x]

    def in_bounds(self, x: int, y: int) -> bool:
        return not (x < 0 or x >= len(self.grid_tiles[0]) or y < 0 or y >= len(self.grid_tiles))

    def go(self, starting_x: int, starting_y: int, direction: str) -> int:
        print(starting_x, starting_y, direction)
        assert direction in ['north', 'south', 'east', 'west']
        to_try: list[Pairing] = []
        visited: list[Pairing] = []

        starting_tile = self.get(starting_x, starting_y)
        moves = starting_tile.process_beam(direction)
        for move in moves:
            if self.in_bounds(move[0], move[1]):
                p = Pairing(starting_tile, self.get(move[0], move[1]))
                to_try.append(p)
        visited_tiles: list[GridTile] = [starting_tile]
        # print(visited)
        # print(visited_tiles)
        # print(to_try)
        # print(moves)
        while to_try:
            # print('visited:', len(visited), visited)
            # print('to_try:', len(to_try), to_try)
            pair = to_try.pop(0)
            if pair.to_tile not in visited_tiles:
                visited_tiles.append(pair.to_tile)
            visited.append(pair)
            moves = pair.to_tile.move_from(pair.from_tile)
            for move in moves:
                if self.in_bounds(move[0], move[1]):
                    p = Pairing(pair.to_tile, self.get(move[0], move[1]))
                    if p not in visited:
                        to_try.append(p)
        return len(visited_tiles)

def parse(my_input: list[str]) -> Grid:
    grid_tiles: list[list[GridTile]] = []
    for y, line in enumerate(my_input):
        try:
            grid_row: list[GridTile] = []
            for x, symbol in enumerate(line):
                grid_row.append(GridTile(x, y, symbol))
            grid_tiles.append(grid_row)
        except BaseException as e:
            print(line)
            raise e
    return Grid(grid_tiles)

def solution1(my_input: list[str]) -> int:
    grid = parse(my_input)
    # print(grid)
    return grid.go(0, 0, 'east')

def solution2(my_input: list[str]) -> int:
    grid = parse(my_input)
    energized = []
    for x in range(len(grid.grid_tiles[0])):
        energized.append(grid.go(x, 0, 'south'))
        energized.append(grid.go(x, len(grid.grid_tiles) - 1, 'north'))
    for y in range(len(grid.grid_tiles)):
        energized.append(grid.go(0, y, 'east'))
        energized.append(grid.go(len(grid.grid_tiles[0]) - 1, y, 'west'))
    return max(energized)

if __name__ == '__main__':
    # for part in [1, 2]:
    for part in [2]:
        print(f"---- Part { 'One' if part == 1 else 'Two' } ----")
        for file in ['sample.txt', 'input.txt']:
            print(f'-- {file} --')
            print(str(eval(f'solution{part}')(open(file, 'r').read().split('\n'))))
            text = input('continue? ')
            if text:
                break
        if text:
            break


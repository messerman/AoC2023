#!/usr/bin/env python3
from tools.colors import *
from tools.position import Position
from enum import Enum

class GridTile(Position):
    def __init__(self, x: int, y: int, symbol: str):
        super().__init__(x, y)
        self.symbol = symbol

    def __str__(self) -> str:
        return self.symbol
    
    def __repr__(self) -> str:
        return f'{self.symbol}@({self.x}, {self.y})'

    def move_from(self, other: 'GridTile') -> list[Position]:
        pass

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
    data = parse(my_input)
    print(data)
    return -1 # TODO

def solution2(my_input: list[str]) -> int:
    data = parse(my_input)
    return -1 # TODO

if __name__ == '__main__':
    for part in [1, 2]:
        print(f"---- Part { 'One' if part == 1 else 'Two' } ----")
        for file in ['sample.txt', 'input.txt']:
            print(f'-- {file} --')
            print(str(eval(f'solution{part}')(open(file, 'r').read().split('\n'))))
            text = input('continue? ')
            if text:
                break
        if text:
            break


#!/usr/bin/env python3
from tools.colors import *

class Universe:
    def __init__(self, width: int, height: int, galaxies: list[tuple[int, int]]):
        self.width = width
        self.height = height
        # self.universe = [list('.' * width)] * height
        self.galaxies = galaxies
    
    def get(self, x: int, y: int) -> str:
        if (x, y) in self.galaxies:
            return '#'
        # return self.universe[y][x]
        return '.'
    
    def __str__(self):
        output = ''
        for y in range(self.height):
            for x in range(self.width):
                output += self.get(x, y)
            output += '\n'
        return output
    
    def find_distance(self, galaxy1: int, galaxy2: int) -> int:
        x1, y1 = self.galaxies[galaxy1]
        x2, y2 = self.galaxies[galaxy2]
        return abs(x1-x2) + abs(y1-y2)

    def expand(self):
        cols_without_galaxies = sorted(list(set(range(self.height)) - set(map(lambda galaxy: galaxy[0], self.galaxies))))
        rows_without_galaxies = sorted(list(set(range(self.width)) - set(map(lambda galaxy: galaxy[1], self.galaxies))))
        self.width += len(cols_without_galaxies)
        self.height += len(rows_without_galaxies)
        # print(rows_without_galaxies, cols_without_galaxies)
        for n, galaxy in enumerate(self.galaxies):
            # print(n, galaxy)
            # print(len(list(filter(lambda x: x < galaxy[0], cols_without_galaxies))))
            new_x = galaxy[0] + len(list(filter(lambda x: x < galaxy[0], cols_without_galaxies)))
            new_y = galaxy[1] + len(list(filter(lambda y: y < galaxy[1], rows_without_galaxies)))
            self.galaxies[n] = (new_x, new_y)
            # print(galaxy, self.galaxies[n])

def parse(my_input: list[str]) -> Universe:
    galaxies: list[tuple[int, int]] = [] # TODO - more accurate type, also for return type, above
    width = len(my_input[0])
    height = len(my_input)
    for y, line in enumerate(my_input):
        try:
            x = line.find('#', 0)
            # print(x, y, line)
            while x > -1:
                galaxies.append((x, y))
                x = line.find('#', x+1)
        except BaseException as e:
            print(line)
            raise e
    # print(len(galaxies), galaxies)
    return Universe(width, height, galaxies)

def solution1(my_input: list[str]) -> int:
    universe = parse(my_input)
    # print(str(universe))
    universe.expand()
    # print(str(universe))
    d = 0
    for i in range(len(universe.galaxies) - 1):
        for j in range(i+1, len(universe.galaxies)):
            d += universe.find_distance(i, j)
    return d

def solution2(my_input: list[str]) -> int:
    universe = parse(my_input)
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


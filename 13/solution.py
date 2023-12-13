#!/usr/bin/env python3
from tools.colors import *

class AshGrid:
    def __init__(self, grid: list[str]):
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)
        self.highlighted_row = -1
        self.highlighted_col = -1

    def __str__(self) -> str:
        result = []
        for y, row in enumerate(self.grid):
            if y == self.highlighted_row:
                result.append(highlight(Color.RED, row))
                continue
            r = ''
            for x, col in enumerate(row):
                r += highlight(Color.RED, col) if x == self.highlighted_col else col
            result.append(r)
        return '\n'.join(result)
    
    def __repr__(self) -> str:
        return str(self)

    def get_row(self, row: int) -> str:
        try:
            return self.grid[row]
        except:
            print(f'UNABLE TO FIND ROW {row} IN GRID WITH HEIGHT {self.height}:')
            print(self)
            raise Exception('ROW ERROR')


    def get_col(self, col: int) -> str:
        try:
            return ''.join(map(lambda row: row[col], self.grid))
        except:
            print(f'UNABLE TO FIND COLUMN {col} IN GRID WITH WIDTH {self.width}:')
            print(self)
            raise Exception('COLUMN ERROR')

    def find_mirror_row(self) -> int:
        print('find_mirror_row')
        mirror_pairs: list[tuple[int, int]] = []
        for row in range(self.height - 1):
            if self.get_row(row) == self.get_row(row + 1):
                mirror_pairs.append((row, row+1))
        # print(mirror_pairs)
        if not mirror_pairs:
            return -1

        result = -1
        for pair in mirror_pairs:
            closest_edge = min(pair[1], self.height - pair[0] - 1)
            # print(pair, closest_edge, self.height)
            failed = False
            r = -1
            for r in range(closest_edge):
                # print(r)
                if self.get_row(pair[0] - r) != self.get_row(pair[1] + r):
                    failed = True
                    print(f'"{self.get_row(pair[0] - r)}" != "{self.get_row(pair[1] + r)}"')
                    break
            if not failed and r >= 0:
                # print(pair, r, pair[0] - r, pair[1] + r, self.height - 1)
                if pair[0] - r == 0 or pair[1] + r == self.height - 1:
                    # print(r, pair[0] - r, pair[1] + r)
                    result = pair[1]
                    break
        return result

    def find_mirror_col(self) -> int:
        print('find_mirror_col')
        mirror_pairs: list[tuple[int, int]] = []
        for col in range(self.width - 1):
            if self.get_col(col) == self.get_col(col + 1):
                mirror_pairs.append((col, col+1))
        print(mirror_pairs)
        if not mirror_pairs:
            return -1
        
        result = -1
        for pair in mirror_pairs:
            closest_edge = min(pair[1], self.width - pair[0] - 1)
            print(pair, closest_edge, self.height)
            failed = False
            r = -1
            for r in range(closest_edge):
                print(r, pair[0] - r, pair[1] + r)
                if self.get_col(pair[0] - r) != self.get_col(pair[1] + r):
                    failed = True
                    print(f'"{self.get_col(pair[0] - r)}" != "{self.get_col(pair[1] + r)}"')
                    break
            if not failed and r >= 0:
                print(pair, r, pair[0] - r - 1, pair[1] + r, self.width - 1)
                if pair[0] - r == 0 or pair[1] + r == self.width - 1:
                    print(r, pair[0] - r, pair[1] + r)
                    result = pair[1]
                    break
        return result

    def find_mirrors(self) -> tuple[int, int]:
        # print('find_mirrors')
        self.highlighted_row = self.find_mirror_row()
        self.highlighted_col = self.find_mirror_col()
        if self.highlighted_row < self.highlighted_col:
            self.highlighted_row = -1
        else:
            self.highlighted_col = -1
        return (self.highlighted_row, self.highlighted_col)

def parse(my_input: list[str]) -> list[AshGrid]:
    result: list[AshGrid] = []
    current_grid: list[str] = []
    for line in my_input:
        try:
            if line:
                current_grid.append(line)
            else:
                result.append(AshGrid(current_grid))
                current_grid = []
        except BaseException as e:
            print(line)
            raise e
    if current_grid:
        result.append(AshGrid(current_grid))
    return result

def solution1(my_input: list[str]) -> int:
    grids = parse(my_input)
    total_rows = 0
    total_cols = 0
    for i, grid in enumerate(grids):
        print(f'----- {i} -----')
        print(str(grid))
        row, col = grid.find_mirrors()
        print(str(grid))
        # print(row, col)
        if row != -1:
            total_rows += row
        elif col != -1:
            total_cols += col
        else:
            print('FAILURE')
            # print(f'----- {i} -----')
            # print(str(grid))
            return -1
            # print()
    # print(total_rows, total_cols)
    return total_rows * 100 + total_cols

def solution2(my_input: list[str]) -> int:
    data = parse(my_input)
    return -1 # TODO

if __name__ == '__main__':
    for part in [1, 2]:
        print(f"---- Part { 'One' if part == 1 else 'Two' } ----")
        for file in ['sample.txt', 'input.txt']:
        # for file in ['failing.txt']:
            print(f'-- {file} --')
            print(str(eval(f'solution{part}')(open(file, 'r').read().split('\n'))))
            text = input('continue? ')
            if text:
                break
        if text:
            break


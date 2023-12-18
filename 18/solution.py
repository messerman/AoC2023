#!/usr/bin/env python3
from tools.colors import *
from tools.position import Position
from itertools import chain

class GridTile(Position):
    def __init__(self, x: int, y: int, symbol: str, color: tuple[int, int, int] = (255, 255, 255)):
        super().__init__(x, y)
        self.symbol = symbol
        self.color = color

    def __str__(self) -> str:
        return highlight_rgb(self.color, self.symbol)
    
    def __repr__(self) -> str:
        return f'{self.symbol}@({self.x}, {self.y})'

class Grid:
    def __init__(self, grid_tiles: dict[tuple[int, int], GridTile]):
        xs = list(map(lambda pos: pos[0], grid_tiles.keys()))
        ys = list(map(lambda pos: pos[1], grid_tiles.keys()))
        self.min_x = min(xs)
        self.max_x = max(xs) + 1
        self.min_y = min(ys)
        self.max_y = max(ys) + 1
        # print(min_x, max_x)
        # print(min_y, max_y)        
        self.grid_tiles: list[list[GridTile]] = []
        for y in range(self.min_y, self.max_y):
            row: list[GridTile] = []
            for x in range(self.min_x, self.max_x):
                if (x, y) in grid_tiles:
                    row.append(grid_tiles[(x, y)])
                else:
                    row.append(GridTile(x, y, '.'))
            self.grid_tiles.append(row)

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
        return self.grid_tiles[y - self.min_y][x - self.min_x]

    def in_bounds(self, x: int, y: int) -> bool:
        return x >= self.min_x and x < self.max_x and y >= self.min_y and y < self.max_y

    def _is_inside(self, tile: GridTile) -> bool:
        # TODO - this is inefficient
        # TODO - this is also WRONG - doesn't account for convex polygons
        count = 0

        # west
        x = tile.x
        y = tile.y
        while self.in_bounds(x, y) and self.get(x, y).symbol != '#':
            x -= 1
        count += 1 if self.in_bounds(x, y) else 0

        # east
        x = tile.x
        y = tile.y
        while self.in_bounds(x, y) and self.get(x, y).symbol != '#':
            x += 1
        count += 1 if self.in_bounds(x, y) else 0

        # north
        x = tile.x
        y = tile.y
        while self.in_bounds(x, y) and self.get(x, y).symbol != '#':
            y -= 1
        count += 1 if self.in_bounds(x, y) else 0

        # south
        x = tile.x
        y = tile.y
        while self.in_bounds(x, y) and self.get(x, y).symbol != '#':
            x += 1
        count += 1 if self.in_bounds(x, y) else 0

        return count == 4

    def grouping(self, tile: GridTile) -> list[GridTile]:
        print('--- grouping ---')
        # print(tile.to_tuple())
        to_visit: list[tuple[int, int]] = tile.neighbors()
        grouping: list[GridTile] = [tile]
        visited: list[tuple[int, int]] = [tile]
        while to_visit:
            # input('> ')
            # print('to_visit:', to_visit)
            candidate = to_visit.pop(0)
            # print('candidate:', candidate)
            if candidate in visited:
                # print('already seen')
                continue
            visited.append(candidate)
            # print('visited:', visited)
            if not self.in_bounds(candidate[0], candidate[1]):
                # print('not in bounds')
                continue
            candidate = self.get(candidate[0], candidate[1])
            if candidate.symbol == '#':
                # print('wall')
                continue
            grouping.append(candidate)
            # print('grouping:', grouping)
            to_visit += candidate.neighbors()
        return grouping

    def _can_reach_outside(self, tile: GridTile) -> bool:
        print('--- _can_reach_outside ---')
        to_visit: list[tuple[int, int]] = tile.neighbors()
        visited: list[tuple[int, int]] = [tile.to_tuple()]
        while to_visit:
            # print('>>', len(to_visit), to_visit, visited)
            # print('>>', len(to_visit))
            candidate = to_visit.pop(0)
            if candidate in visited:
                # print(f'already visited {candidate}')
                continue
            visited.append(candidate)
            if not self.in_bounds(candidate[0], candidate[1]):
                # print(f'out of bounds {candidate}')
                return True
            candidate = self.get(candidate[0], candidate[1])
            if candidate.symbol == '#':
                # print(f'wall {candidate}')
                continue
            to_visit += candidate.neighbors()
        return False

    def fill(self):
        print('--- fill ---')
        dots = list(filter(lambda tile: tile.symbol == '.', chain(*self.grid_tiles)))
        while dots:
            # print(len(dots))
            g = self.grouping(dots[0])
            # print(len(g))
            # assert g
            # print('before')
            # # dots = [dot for dot in dots if dot not in g]
            # new_dots = []
            # for dot in dots:
            #     print(dot.to_tuple(), len(new_dots))
            #     if dot not in g:
            #         new_dots.append(dot)
            # dots = new_dots
            # print('after')
            # print(len(dots))
            if self._can_reach_outside(self.get(g[0].x, g[0].y)):
                for tile in g:
                    tile.symbol='o'
                    tile.color=(255,0,255)
                # print('inside')
            else:
                for tile in g:
                    tile.symbol = '#'
                    tile.color = (255, 0, 0)
                for tile in list(filter(lambda tile: tile.symbol == '.', dots)):
                    tile.symbol='o'
                    tile.color=(255,0,255)
                return
            dots = list(filter(lambda tile: tile.symbol == '.', dots))

    def num_lava(self) -> int:
        return sum(map(lambda tile: 1 if tile.symbol == '#' else 0, list(chain(*self.grid_tiles))))

def parse(my_input: list[str]) -> Grid:
    x = 0
    y = 0
    tiles: dict[tuple[int, int], GridTile] = {(x, y): GridTile(x, y, '#')}
    for line in my_input: # e.g. 'R 6 (#70c710)'
        try:
            direction, times, color = line.split(' ')
            color = rgb_from_hex(color[1:-1])
            for time in range(int(times)):
                if direction == 'R':
                    x += 1
                elif direction == 'L':
                    x -= 1
                elif direction == 'U':
                    y -= 1
                elif direction == 'D':
                    y += 1
                tiles[(x, y)] = GridTile(x, y, '#', color)
                # print(str(tiles[(x, y)]))
        except BaseException as e:
            print(line)
            raise e
    # print(list(map(str, tiles.values())))
    return Grid(tiles)

def solution1(my_input: list[str]) -> int:
    grid = parse(my_input)
    # print(grid)
    print(grid.num_lava())
    grid.fill()
    print(grid)
    return grid.num_lava()

def solution2(my_input: list[str]) -> int:
    grid = parse(my_input)
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


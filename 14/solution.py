#!/usr/bin/env python3
from tools.colors import *
from copy import deepcopy

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __str__(self):
        return str((self.x, self.y))
    
    def __repr__(self):
        return str(self)
    
    def to_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)
    
    def north(self) -> tuple[int, int]:
        return (self.x, self.y - 1)

    def south(self) -> tuple[int, int]:
        return (self.x, self.y + 1)

    def east(self) -> tuple[int, int]:
        return (self.x + 1, self.y)

    def west(self) -> tuple[int, int]:
        return (self.x - 1, self.y)

    def go_north(self):
        self.x, self.y = self.north()

    def go_south(self):
        self.x, self.y = self.south()

    def go_east(self):
        self.x, self.y = self.east()

    def go_west(self):
        self.x, self.y = self.west()

class Rock(Position):
    def __init__(self, x: int, y: int, symbol: str):
        super().__init__(x, y)
        self.symbol = symbol
        self.blocking = symbol in '#O'
        self.movable = symbol == 'O'

    def __str__(self) -> str:
        return self.symbol
    
    def move_north(self, rock_map: dict[tuple[int, int], 'Rock']) -> bool:
        # print((self.x, self.y), self, rock_map[self.to_tuple()], self.north(), self.blocking, self.movable)
        if self.movable and self.north() in rock_map and not rock_map[self.north()].blocking:
            # print((self.x, self.y), self, rock_map[self.to_tuple()], rock_map[self.north()], rock_map[self.north()].blocking)
            old_x, old_y = self.x, self.y
            super().go_north()
            rock_map[self.to_tuple()] = self
            rock_map[(old_x, old_y)] = Rock(old_x, old_y, '.')
            return True
        return False

    def move_west(self, rock_map: dict[tuple[int, int], 'Rock']) -> bool:
        if self.movable and self.west() in rock_map and not rock_map[self.west()].blocking:
            old_x, old_y = self.x, self.y
            super().go_west()
            rock_map[self.to_tuple()] = self
            rock_map[(old_x, old_y)] = Rock(old_x, old_y, '.')
            return True
        return False

    def move_south(self, rock_map: dict[tuple[int, int], 'Rock']) -> bool:
        if self.movable and self.south() in rock_map and not rock_map[self.south()].blocking:
            old_x, old_y = self.x, self.y
            super().go_south()
            rock_map[self.to_tuple()] = self
            rock_map[(old_x, old_y)] = Rock(old_x, old_y, '.')
            return True
        return False

    def move_east(self, rock_map: dict[tuple[int, int], 'Rock']) -> bool:
        if self.movable and self.east() in rock_map and not rock_map[self.east()].blocking:
            old_x, old_y = self.x, self.y
            super().go_east()
            rock_map[self.to_tuple()] = self
            rock_map[(old_x, old_y)] = Rock(old_x, old_y, '.')
            return True
        return False

    def compute_load(self, height: int) -> int:
        return height - self.y


class Platform:
    def __init__(self, width: int, height: int, rocks: list[Rock]):
        self.width = width
        self.height = height
        self.rocks: dict[tuple[int, int], 'Rock'] = {}
        for rock in rocks:
            self.rocks[rock.to_tuple()] = rock

    def __str__(self) -> str:
        lines: list[str] = []
        for y in range(self.height):
            line = ''
            for x in range(self.width):
                line += self.rocks[(x, y)].symbol
            lines.append(line)
        return '\n'.join(lines)

    def __repr__(self) -> str:
        return f'Platform({self.width} x {self.height})'
    
    def tilt_north(self):
        for y in range(self.height):
            for x in range(self.width):
                rock = self.rocks[(x, y)]
                while rock.move_north(self.rocks):
                    pass

    def run_cycle(self, times: int = 1) -> list[str]:
        history: list[str] = []#dict[str, str] = {}
        for time in range(times):
            me = str(self)
            if me in history:
                # keys = []
                # for k,v in history.items():
                #     if v == before:
                #         keys.append(k)
                history.append(me)
                return history
            for y in range(self.height):
                for x in range(self.width):
                    rock = self.rocks[(x, y)]
                    while rock.move_north(self.rocks):
                        pass
            for y in range(self.height):
                for x in range(self.width):
                    rock = self.rocks[(x, y)]
                    while rock.move_west(self.rocks):
                        pass
            for y in range(self.height - 1, -1, -1):
                for x in range(self.width):
                    rock = self.rocks[(x, y)]
                    while rock.move_south(self.rocks):
                        pass
            for y in range(self.height):
                for x in range(self.width - 1, -1, -1):
                    rock = self.rocks[(x, y)]
                    while rock.move_east(self.rocks):
                        pass
            history.append(me)#[before] = str(self)
            # print(time)
            # print(before)
            # print(time)
            # print(history[before])
            # print(time)

def parse(my_input: list[str]) -> Platform:
    rocks: list[Rock] = []
    for y, line in enumerate(my_input):
        try:
            for x, c in enumerate(line):
                rocks.append(Rock(x, y, c))
        except BaseException as e:
            print(line)
            raise e
    return Platform(len(my_input[0]), len(my_input), rocks)

def solution1(my_input: list[str]) -> int:
    platform = parse(my_input)
    # print(platform)
    # print()
    platform.tilt_north()
    # print(platform)
    # print(platform.rocks[(0,0)].compute_load(platform.height))
    return sum(list(map(lambda rock: rock.compute_load(platform.height), filter(lambda rock: rock.movable, platform.rocks.values()))))

def solution2(my_input: list[str]) -> int:
    platform = parse(my_input)
    runs = 1000000000
    # print(platform)
    # print()
    history = platform.run_cycle(runs)
    for i,h in enumerate(history[:-1], -1):
        if h == history[-1]:
            cycle_begin = i
            cycle_end = len(history) - 2
    # print(cycle_begin)
    # print(history[cycle_begin])
    # print(cycle_end)
    # print(history[cycle_end])
    # print(cycle_end - cycle_begin)
    # print(runs - cycle_begin - 1)
    # print((runs - cycle_begin - 1) % (cycle_end - cycle_begin))
    # print((runs - cycle_begin - 1) % (cycle_end - cycle_begin))

    platform = parse(history[cycle_begin].split('\n'))
    platform.run_cycle((runs - cycle_begin) % (cycle_end - cycle_begin))

    # ps: list[Platform] = []
    # platform = parse(my_input)
    # times = 0
    # while str(platform) != p:
    #     platform.run_cycle(1)
    #     ps.append(deepcopy(platform))
    #     times += 1
    # print(platform)
    # print(times)
    # # print(platform)
    # print('--' * 20)
    # for plat in ps:
    #     print(str(plat) + '\n')
    return sum(list(map(lambda rock: rock.compute_load(platform.height), filter(lambda rock: rock.movable, platform.rocks.values()))))

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

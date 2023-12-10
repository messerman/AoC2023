#!/usr/bin/env python3
from functools import reduce
import re

class GridItem:
    def __init__(self, line_num: int, match: re.match):
        self.y = line_num
        self.value = match.group()
        self.x_start = match.start()
        self.x_end = match.end()
        self.pos = (self.x_start, self.y)
        self.positions = []
        for x in range(self.x_start, self.x_end):
            self.positions.append((x,self.y))
    
    def adjacent_positions(self):
        positions = []
        for x in range(self.x_start-1, self.x_end+1):
            positions.append((x, self.y-1))
        positions.append((self.x_start-1, self.y))
        positions.append((self.x_end, self.y))
        for x in range(self.x_start-1, self.x_end+1):
            positions.append((x, self.y+1))
        return positions
    
    def is_adjacent(self, other: "GridItem") -> bool:
        me = set(self.adjacent_positions())
        you = set(other.positions)
        return bool(me.intersection(you))

def find_pattern(pattern: str, line_num: int, line: str):
    result = []
    for match in re.finditer(pattern, line):
        result.append((match.start(), line_num))
    return result

def find_item(pattern: str, line_num: int, line: str):
    result = []
    for match in re.finditer(pattern, line):
        result.append(GridItem(line_num, match))
    return result

def is_part_num(num: GridItem, symbol_positions):
    for position in num.adjacent_positions():
        if position in symbol_positions:
            return True
    return False

def gear_ratio(star: GridItem, nums):
    for position in star.adjacent_positions():
        values: list(GridItem) = []
        for num in filter(star.is_adjacent, nums):
            if star.is_adjacent(num):
                values.append(int(num.value))
    # print(star.pos, values[0] * values[1] if len(values) == 2 else values)
    return values[0] * values[1] if len(values) == 2 else 0

def solution1(my_input: list[str]):
    symbol_positions = []
    nums = []
    line_num = 0    
    pattern = r'\+|\*|\=|\-|\&|\#|\/|\%|\$|\@' # +*=-&#/%$@
    for line in my_input:
        symbol_positions += find_pattern(pattern, line_num, line)
        nums += find_item(r'\d+', line_num, line)
        line_num += 1
    return sum(list(map(lambda num: int(num.value), filter(lambda num: is_part_num(num, symbol_positions), nums))))

def solution2(my_input: list[str]):
    stars = []
    line_num = 0
    nums = []
    for line in my_input:
        nums += find_item(r'\d+', line_num, line)
        stars += find_item(r'\*', line_num, line)
        line_num += 1
    # num_positions = { num.pos:num for num in nums }
    ratio_sum = 0
    for star in stars:
        ratio_sum += gear_ratio(star, nums)
    return ratio_sum

if __name__ == '__main__':
    print('---- Part One ----')
    print(solution1(open('sample1.txt', 'r').read().split('\n')))
    print(solution1(open('input.txt', 'r').read().split('\n')))
    print('---- Part Two ----')
    print(solution2(open('sample2.txt', 'r').read().split('\n')))
    print(solution2(open('test.txt', 'r').read().split('\n')))
    print(solution2(open('input.txt', 'r').read().split('\n')))

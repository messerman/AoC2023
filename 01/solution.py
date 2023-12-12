#!/usr/bin/env python3
import re

def solution1(my_input: list[str]):
    sum = 0
    for line in my_input:
        nums = re.findall(r'\d', line)
        sum += int(nums[0] + nums[-1])
    return sum

def solution2(my_input: list[str]):
    lookup = { 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9 }
    rlookup = { 'eno': 1, 'owt': 2, 'eerht': 3, 'ruof': 4, 'evif': 5, 'xis': 6, 'neves': 7, 'thgie': 8, 'enin': 9, '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, }
    sum = 0
    for line in my_input:
        words = 'one|two|three|four|five|six|seven|eight|nine'
        nums = re.findall(re.compile('\d|' + words), line)
        rnums = re.findall(re.compile('\d|' + words[::-1]), line[::-1])
        val = 10 * lookup[nums[0]] + rlookup[rnums[0]]
        sum += val
    return sum

if __name__ == '__main__':
    print('---- Part One ----')
    print(solution1(open('sample1.txt', 'r').read().split('\n')))
    print(solution1(open('input.txt', 'r').read().split('\n')))
    print('---- Part Two ----')
    print(solution2(open('sample2.txt', 'r').read().split('\n')))
    print(solution2(open('input.txt', 'r').read().split('\n')))

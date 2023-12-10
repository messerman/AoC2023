#!/usr/bin/env python3
from functools import reduce
import math
import re

def assertEqual(a, b):
    assert a == b, f'{a} != {b}'

def x(t, d):
    neg_b = (t/2)
    quad = math.sqrt((t**2/4) - d)
    return (neg_b-quad, neg_b+quad)

def to_beat(t,d):
    (low, high) = x(t,d+1)
    return math.floor(high) - math.ceil(low) + 1

def parse(my_input: list[str]) -> (list[int], list[int]):
    time_line = my_input[0]
    dist_line = my_input[1]
    times = list(map(lambda x: int(x), re.findall(r'(\d+)', time_line)))
    dists = map(lambda x: int(x), re.findall(r'(\d+)', dist_line))
    return (times, dists)

def solution1(my_input: list[str]):
    try:
        (times, dists) = parse(my_input)
        results = map(lambda z: to_beat(z[0], z[1]), zip(times, dists))
        return reduce(lambda a,b: a*b, results)
    except BaseException as e:
        raise e

def solution2(my_input: list[str]):
    try:
        (times, dists) = parse(my_input)
        t = int(''.join(map(lambda x: str(x), times)))
        d = int(''.join(map(lambda x: str(x), dists)))
        return to_beat(t, d)
    except BaseException as e:
        raise e

if __name__ == '__main__':
    print('---- Part One ----')
    print(solution1(open('sample1.txt', 'r').read().split('\n')))
    print(solution1(open('input.txt', 'r').read().split('\n')))
    print('---- Part Two ----')
    print(solution2(open('sample2.txt', 'r').read().split('\n')))
    print(solution2(open('input.txt', 'r').read().split('\n')))

    assertEqual(to_beat(7,9), 4)
    assertEqual(to_beat(15,40), 8)
    assertEqual(to_beat(30,200), 9)
    assertEqual(to_beat(71530,940200), 71503)

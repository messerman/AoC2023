#!/usr/bin/env python3
from functools import reduce

class OasisSequence:
    def __init__(self, values: list[int], depth: int = 0):
        self.values = values
        self.depth = depth
    
    def __str__(self):
        sep = ' '
        s = sep[:len(sep)//2] * self.depth
        return s + sep.join(map(str, self.values)) + s

    def __repr__(self):
        return str(self)

    def infer_next(self) -> int:
        all_zeroes = reduce(lambda l, r: l == 0 and r == 0, self.values, 0)
        if all_zeroes == len(self.values):
            return 0
        values: list[int] = list(map(lambda e: e[1] - self.values[e[0]], list(enumerate(self.values[1:]))))
        delta_sequence = OasisSequence(values, self.depth + 1)
        self.values.append(self.values[-1] + delta_sequence.infer_next())
        return self.values[-1]

    def infer_prev(self) -> int:
        values = self.values
        values.reverse()
        self.values.insert(0, self.infer_next())
        return self.values[0]

def parse(my_input: list[str]) -> list:
    result: list[OasisSequence] = []
    for line in my_input:
        try:
            result.append(OasisSequence(list(map(int, line.split(' ')))))
        except BaseException as e:
            print(line)
            raise e
    return result

def solution1(my_input: list[str]) -> int:
    sequences: list[OasisSequence] = parse(my_input)
    return sum(map(OasisSequence.infer_next, sequences))

def solution2(my_input: list[str]) -> int:
    sequences: list[OasisSequence] = parse(my_input)
    return sum(map(OasisSequence.infer_prev, sequences))

if __name__ == '__main__':
    print('---- Part One ----')
    print(solution1(open('sample.txt', 'r').read().split('\n')))
    print(solution1(open('input.txt', 'r').read().split('\n')))
    print('---- Part Two ----')
    print(solution2(open('sample.txt', 'r').read().split('\n')))
    print(solution2(open('input.txt', 'r').read().split('\n')))

#!/usr/bin/env python3
from tools.colors import *

def parse(my_input: list[str]) -> list[str]:
    result: list[str] = [] # TODO - more accurate type, also for return type, above
    for line in my_input:
        try:
            result.append(line) # TODO - processing
        except BaseException as e:
            print(line)
            raise e
    return result

def solution1(my_input: list[str]) -> int:
    sequences = parse(my_input)
    return -1 # TODO

def solution2(my_input: list[str]) -> int:
    sequences = parse(my_input)
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


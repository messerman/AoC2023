#!/usr/bin/env python3
from tools.colors import *
from functools import cache

@cache
def possibles(s: str) -> list[str]:
    if '?' not in s:
        return [s]
    result = []
    result += possibles(s.replace('?', '.', 1))
    result += possibles(s.replace('?', '#', 1))
    return result

class ConditionRecord:
    def __init__(self, springs: str, damaged: list[int]):
        self.springs = springs
        self.damaged: list[str] = list(map(lambda x: '#' * x, damaged))
    
    def __str__(self):
        return f'{self.springs} {",".join(map(str, self.damaged))}'
    
    def __repr__(self):
        return str(self)

    def repair(self) -> int:
        possibilities = possibles(self.springs)
        count = 0
        for p in possibilities:
            q = list(filter(bool, p.split('.')))
            if q == self.damaged:
                count += 1
        return count

def parse(my_input: list[str], copies: int = 1) -> list[ConditionRecord]:
    result: list[ConditionRecord] = []
    for line in my_input:
        try:
            springs, dmg_list = line.split(' ')
            springs = '?'.join([springs] * copies)
            dmg_list = ','.join([dmg_list] * copies)
            damaged = list(map(int, dmg_list.split(',')))
            condition_record = ConditionRecord(springs, damaged)
            result.append(condition_record)
        except BaseException as e:
            print(line)
            raise e
    return result

def solution1(my_input: list[str]) -> int:
    condition_records = parse(my_input)
    count = 0
    for condition_record in condition_records:
        x = condition_record.repair()
        # print(x)
        count += x
    return count

def solution2(my_input: list[str]) -> int:
    condition_records = parse(my_input, 5)
    count = 0
    for condition_record in condition_records:
        # print(condition_record)
        x = condition_record.repair()
        # print(x)
        count += x
    return count

if __name__ == '__main__':
    for part in [1, 2]:
        print(f"---- Part { 'One' if part == 1 else 'Two' } ----")
        for file in ['sample.txt', 'input.txt', 'input.txt']:
            print(f'-- {file} --')
            print(str(eval(f'solution{part}')(open(file, 'r').read().split('\n'))))
            text = input('continue? ')
            if text:
                break
        if text:
            break


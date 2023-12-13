#!/usr/bin/env python3
from tools.colors import *
import re

MEMO: dict[tuple[int, int], list[list[str]]] = { }
class ConditionRecord:
    def __init__(self, springs: str, damaged: list[int]):
        self.springs = springs
        self.num_damaged = sum(damaged)
        self.damaged: list[str] = list(map(lambda x: '#' * x, damaged))
    
    def __str__(self):
        return f'{self.springs} {self.damaged}'
    
    def __repr__(self):
        return str(self)

    @classmethod
    def permute(cls, bits: int, bins: int) -> list[list[str]]:
        # print(f'permute({bits}, {bins}), {len(MEMO)}')
        if (bits, bins) in MEMO:
            return MEMO[(bits, bins)]

        if bits == 0 or bins == 0:
            MEMO[(bits, bins)] = [[''] * bins]
            return MEMO[(bits, bins)]

        if bins == 1:
            MEMO[(bits, bins)] = [['.' * bits]]
            return MEMO[(bits, bins)]

        result = []
        for value in range(bits + 1):
            permutations = cls.permute(bits - value, bins - 1)
            # print(f'permute({bits}, {bins})', value, permutations)
            s = ['.' * value]
            for p in permutations:
                # x = (s + p).split('.')
                result.append(s + p)

        MEMO[(bits, bins)] = result
        return MEMO[(bits, bins)]
    
    @classmethod
    def interleave(cls, s1: list[str], s2: list[str]) -> str:
        assert len(s1) >= len(s2), f'{s1}, {s2}'
        c = s1 + s2
        c[::2] = s1
        c[1::2] = s2
        return ''.join(c)

    def possibles(self) -> list[str]:
        result = []
        num_commas = len(self.damaged) - 1
        bits = len(self.springs) - self.num_damaged
        bins = num_commas + 2
        for p in self.permute(bits, bins):
            s = self.interleave(p, self.damaged)
            if self.match(s):
                result.append(s)
        return result

    def match(self, potential: str) -> bool:
        if len(potential) != len(self.springs):
            return False
        if self.damaged != list(map(lambda x: x.group(), re.finditer('\#+', potential))):
            return False
        for i,c in enumerate(potential):
            if self.springs[i] != '?' and self.springs[i] != c:
                return False
        return True

    def repair(self) -> int:
        possibilities = self.possibles()
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
        print(condition_record)
        x = condition_record.repair()
        # print(x)
        count += x
    return count

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

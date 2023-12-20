#!/usr/bin/env python3
from tools.colors import *
from typing import Optional
import re

class Rule:
    def __init__(self, rule: str):
        self.rule = rule
        parts = rule.split(':')
        if len(parts) == 1:
            self._execute = lambda x: parts[0]
        else:
            destination = parts[1]
            groups = re.match(r'([xmas])([\<\>])(\d+)', parts[0]).groups()
            self._execute = lambda x: destination if eval(f'{x[groups[0]]} {groups[1]} {groups[2]}') else None

    def execute(self, part_rating: dict[str, int]) -> Optional[str]:
        return self._execute(part_rating)

class Workflow:
    def __init__(self, name: str, rules: list[Rule]):
        self.rules = rules

    def execute(self, part_rating: dict[str, int]) -> str:
        for rule in self.rules:
            result = rule.execute(part_rating)
            if result:
                return result
        assert 'wtf?'

def parse(my_input: list[str]) -> tuple[dict[str, Workflow], list[dict[str, int]]]:
    workflows: dict[str, Workflow] = {}
    part_ratings: list[dict[str, int]] = []
    workflows_complete = False
    for line in my_input:
        try:
            if not line:
                workflows_complete = True
                continue
            if workflows_complete:
                ratings = re.findall(r'(\d+)', line)
                part_ratings.append({'x': int(ratings[0]), 'm': int(ratings[1]), 'a': int(ratings[2]), 's': int(ratings[3])})
            else:
                match = re.fullmatch(r'(?P<name>[a-z]+)\{(?P<workflow>.*)\}', line)
                name: str = match.groupdict()['name']
                rules: list[Rule] = [Rule(rule) for rule in match.groupdict()['workflow'].split(',')]
                workflows[name] = Workflow(name, rules)
        except BaseException as e:
            print(line)
            raise e
    return (workflows, part_ratings)

def solution1(my_input: list[str]) -> int:
    workflows, part_ratings = parse(my_input)
    accepted = []
    for part_rating in part_ratings:
        next_workflow = 'in'
        while next_workflow not in 'AR':
            next_workflow = workflows[next_workflow].execute(part_rating)
            if next_workflow == 'A':
                accepted.append(sum(list(part_rating.values())))
    return sum(accepted)

def solution2(my_input: list[str]) -> int:
    data = parse(my_input)
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


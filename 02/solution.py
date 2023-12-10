#!/usr/bin/env python3
import functools

def get_rounds(game_line: str):
    game = game_line.split(': ')
    game_num = int(game[0].split(' ')[1])
    all_rounds = game[1].split(';')
    rounds = []
    for round in all_rounds:
        round_values = { 'blue': 0, 'green': 0, 'red': 0 }
        cubes = round.split(', ')
        for cube in cubes:
            cube = cube.strip()
            values = cube.split(' ')
            round_values[values[1]] = int(values[0])
        rounds.append(round_values)
    return (game_num, rounds)

def solution1(my_input: list[str]):
    goal = { 'blue': 14, 'green': 13, 'red': 12 }
    valid_games = []
    for game in my_input:
        rounds = get_rounds(game)
        most = { 'blue': 0, 'green': 0, 'red': 0 }
        for round in rounds[1]:
            most['blue'] = max(round['blue'], most['blue'])
            most['green'] = max(round['green'], most['green'])
            most['red'] = max(round['red'], most['red'])
        if most['blue'] <= goal['blue'] and most['green'] <= goal['green'] and most['red'] <= goal['red']:
            valid_games.append(rounds[0])
    return sum(valid_games)

def solution2(my_input: list[str]):
    powers = []
    for game in my_input:
        rounds = get_rounds(game)
        most = { 'blue': 0, 'green': 0, 'red': 0 }
        for round in rounds[1]:
            most['blue'] = max(round['blue'], most['blue'])
            most['green'] = max(round['green'], most['green'])
            most['red'] = max(round['red'], most['red'])
        powers.append(functools.reduce(lambda x,y: x*y, most.values()))

    return sum(powers)

if __name__ == '__main__':
    print('---- Part One ----')
    print(solution1(open('sample1.txt', 'r').read().split('\n')))
    print(solution1(open('input.txt', 'r').read().split('\n')))
    print('---- Part Two ----')
    print(solution2(open('sample2.txt', 'r').read().split('\n')))
    print(solution2(open('input.txt', 'r').read().split('\n')))

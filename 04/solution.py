#!/usr/bin/env python3
import re

# e.g:  'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53'
class Scratchcard:
    def __init__(self, line: str):
        pattern = r'Card +(\d+): ([ +\d+ +]+) \| ([ +\d+ +]+)'
        match = re.match(pattern, line)
        self.card_num = int(match.groups()[0])
        self.numbers = set(map(lambda x: int(x), filter(lambda x: x, re.match(pattern, line).groups()[1].split(' '))))
        self.winners = set(map(lambda x: int(x), filter(lambda x: x, re.match(pattern, line).groups()[2].split(' '))))
    
    def winning_numbers(self) -> list[int]:
        return list(self.numbers.intersection(self.winners))

def solution1(my_input: list[str]):
    cards: list[Scratchcard] = []
    winners: list[int] = []
    for line in my_input:
        try:
            cards.append(Scratchcard(line))
            winners.append(int(2**(len(cards[-1].winning_numbers())-1)))
        except BaseException as e:
            print(line)
            raise e

    return sum(winners)

def solution2(my_input: list[str]):
    num_copies: dict[int, int] = {}
    for line in my_input:
        try:
            card = Scratchcard(line)
            num_copies[card.card_num] = len(card.winning_numbers())
        except BaseException as e:
            print(line)
            raise e

    card_copies = {key: 1 for key in num_copies.keys()}
    for key, value in num_copies.items():
        for i in range(key + 1, key + 1 + value):
            card_copies[i] += card_copies[key]

    return sum(card_copies.values())

if __name__ == '__main__':
    print('---- Part One ----')
    print(solution1(open('sample1.txt', 'r').read().split('\n')))
    print(solution1(open('input.txt', 'r').read().split('\n')))
    print('---- Part Two ----')
    print(solution2(open('sample2.txt', 'r').read().split('\n')))
    print(solution2(open('input.txt', 'r').read().split('\n')))

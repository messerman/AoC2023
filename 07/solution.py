#!/usr/bin/env python3
from collections import defaultdict
from enum import Enum
from functools import cmp_to_key

CamelCards = { k:v for k,v in zip(list('123456789TJQKA'), range(1,15))}
CamelCards2 = { k:v for k,v in zip(list('J123456789TQKA'), range(1,15))} # Jokers are worth the least

class CamelHandRank(Enum):
    FIVE_OF_A_KIND =  7
    FOUR_OF_A_KIND =  6
    FULL_HOUSE =      5
    THREE_OF_A_KIND = 4
    TWO_PAIR =        3
    ONE_PAIR =        2
    HIGH_CARD =       1

class CamelHand:
    def __init__(self, hand: list[str], bid: int, jokers: bool = False):
        self.hand = hand
        self.bid = bid
        self.jokers = jokers
        self.score = self.score_hand().value
    
    def score_hand(self) -> CamelHandRank:
        counts: dict[int, list[str]] = defaultdict(lambda: [])
        hand = self.hand
        for k in CamelCards.keys():
            count = hand.count(k)
            counts[count].append(k)

        num_jokers = self.hand.count('J') if self.jokers else 0

        if 5 in counts:
            return CamelHandRank.FIVE_OF_A_KIND
        elif 4 in counts:
            return CamelHandRank.FOUR_OF_A_KIND if num_jokers == 0 else CamelHandRank.FIVE_OF_A_KIND
        elif 3 in counts and 2 in counts:
            return CamelHandRank.FULL_HOUSE if num_jokers == 0 else CamelHandRank.FIVE_OF_A_KIND
        elif 3 in counts:
            return CamelHandRank.THREE_OF_A_KIND if num_jokers == 0 else CamelHandRank.FOUR_OF_A_KIND
        elif 2 in counts and len(counts[2]) == 2:
            if num_jokers == 0:
                return CamelHandRank.TWO_PAIR
            if num_jokers == 1:
                return CamelHandRank.FULL_HOUSE
            if num_jokers == 2:
                return CamelHandRank.FOUR_OF_A_KIND
        elif 2 in counts:
            return CamelHandRank.ONE_PAIR if num_jokers == 0 else CamelHandRank.THREE_OF_A_KIND
        # else
        return CamelHandRank.HIGH_CARD if num_jokers == 0 else CamelHandRank.ONE_PAIR

    def compare(self, other: "CamelHand") -> int:
        card_type = CamelCards2 if self.jokers else CamelCards
        if self.score > other.score:
            return -1
        if other.score > self.score:
            return 1
        for i in range(0, 6):
            if card_type[self.hand[i]] > card_type[other.hand[i]]:
                return -1
            if card_type[other.hand[i]] > card_type[self.hand[i]]:
                return 1
        return 0 # should never happen

def solution(my_input: list[str], jokers: bool) -> int:
    hands: list[CamelHand] = []
    for line in my_input:
        try:
            (hand_s, bid_s) = line.split(' ')
            bid = int(bid_s)
            hand = list(hand_s)
            hands.append(CamelHand(hand, bid, jokers))
        except BaseException as e:
            print(f'"{line}"')
            raise e
        hands.sort(key=cmp_to_key(CamelHand.compare), reverse=True)
    hands.sort(key=cmp_to_key(CamelHand.compare), reverse=True)
    total = 0
    for i in range(len(hands)):
        total += hands[i].bid * (i+1)
    return total    

def solution1(my_input: list[str]):
    return solution(my_input, False)

def solution2(my_input: list[str]):
    return solution(my_input, True)

if __name__ == '__main__':
    print('---- Part One ----')
    print(solution1(open('sample.txt', 'r').read().split('\n')))
    print(solution1(open('input.txt', 'r').read().split('\n')))
    print('---- Part Two ----')
    print(solution2(open('sample.txt', 'r').read().split('\n')))
    print(solution2(open('input.txt', 'r').read().split('\n')))

#!/usr/bin/env python3
from tools.colors import *
from collections import defaultdict
import re

# TODO - there's probably a python way to do this, but I'm on a plane
ASCII_MAP: dict[str, int] = {'nul': 0, 'soh': 1, 'stx': 2, 'etx': 3, 'eot': 4, 'enq': 5, 'ack': 6, 'bel': 7, 'bs': 8, 'ht': 9, 'nl': 10, 'vt': 11, 'np': 12, 'cr': 13, 'so': 14, 'si': 15, 'dle': 16, 'dc1': 17, 'dc2': 18, 'dc3': 19, 'dc4': 20, 'nak': 21, 'syn': 22, 'etb': 23, 'can': 24, 'em': 25, 'sub': 26, 'esc': 27, 'fs': 28, 'gs': 29, 'rs': 30, 'us': 31, 'sp': 32, '!': 33, '"': 34, '#': 35, '$': 36, '%': 37, '&': 38, "'": 39, '(': 40, ')': 41, '*': 42, '+': 43, ',': 44, '-': 45, '.': 46, '/': 47, '0': 48, '1': 49, '2': 50, '3': 51, '4': 52, '5': 53, '6': 54, '7': 55, '8': 56, '9': 57, ':': 58, ';': 59, '<': 60, '=': 61, '>': 62, '?': 63, '@': 64, 'A': 65, 'B': 66, 'C': 67, 'D': 68, 'E': 69, 'F': 70, 'G': 71, 'H': 72, 'I': 73, 'J': 74, 'K': 75, 'L': 76, 'M': 77, 'N': 78, 'O': 79, 'P': 80, 'Q': 81, 'R': 82, 'S': 83, 'T': 84, 'U': 85, 'V': 86, 'W': 87, 'X': 88, 'Y': 89, 'Z': 90, '[': 91, '\\': 92, ']': 93, '^': 94, '_': 95, '`': 96, 'a': 97, 'b': 98, 'c': 99, 'd': 100, 'e': 101, 'f': 102, 'g': 103, 'h': 104, 'i': 105, 'j': 106, 'k': 107, 'l': 108, 'm': 109, 'n': 110, 'o': 111, 'p': 112, 'q': 113, 'r': 114, 's': 115, 't': 116, 'u': 117, 'v': 118, 'w': 119, 'x': 120, 'y': 121, 'z': 122, '{': 123, '|': 124, '}': 125, '~': 126, 'del': 127}

'''
Determine the ASCII code for the current character of the string.
Increase the current value by the ASCII code you just determined.
Set the current value to itself multiplied by 17.
Set the current value to the remainder of dividing itself by 256.
After following these steps for each character in the string in order, the current value is the output of the HASH algorithm.
'''
def hash_algo(sequence: str) -> int:
    result = 0
    for c in list(sequence):
        value = ASCII_MAP[c]
        result += value
        result *= 17
        result %= 256
    return result

def parse(my_input: list[str]) -> list[str]:
    result: list[str] = [] # TODO - more accurate type, also for return type, above
    for line in my_input:
        try:
            for sequence in line.split(','):
                result.append(sequence)
        except BaseException as e:
            print(line)
            raise e
    return result

def solution1(my_input: list[str]) -> int:
    data = parse(my_input)
    hashes = list(map(hash_algo, data))
    return sum(hashes)

def solution2(my_input: list[str]) -> int:
    data = parse(my_input)
    boxen: dict[int, list[str]] = defaultdict(lambda: [])
    for d in data:
        # box = boxen[hash_algo(d)]
        label = re.findall(r'\w+', d)[0]
        box = boxen[hash_algo(label)]
        # print(box)
        if '=' in d:
            label, focal_length = d.split('=')
            # print(d, label, focal_length)
            found = False
            for i, l in enumerate(box):
                if l.split(' ')[0] == label:
                    box[i] = f'{label} {focal_length}'
                    found = True
            if not found:
                box.append(f'{label} {focal_length}')
            # print(box)
            # TODO - put [label focal_length] in box h
        else:
            label = d.split('-')[0]
            for l in box:
                if l.split(' ')[0] == label:
                    box.remove(l)
        # print(d, hash_algo(d), box)

    # print(dict(boxen))

    values: list[int] = []
    for i in range(256):
        if i in boxen and boxen[i]:
            # print(i, boxen[i])
            for slot, lens in enumerate(boxen[i]):
                label, focal_length = lens.split(' ')
                v = (i + 1) * (slot + 1) * int(focal_length)
                # print(label, i, i+1, slot, slot+1, focal_length, v)
                values.append(v)
    return sum(values)

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


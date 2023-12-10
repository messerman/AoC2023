#!/usr/bin/env python3
from collections import defaultdict
from copy import copy
from sys import maxsize

def map_source_to_destination(mapping: list[(int, int, int)], reverse = False) -> dict[tuple[int, int], int]:
    result: dict[int, int] = {}
    for row in mapping:
        d, s, r = row
        if reverse:
            d,s = s,d
        result[(s, s+r)] = d - s
    return result

def map_seed_to_location(seed, maps):
    names = 'seed soil fertilizer water light temperature humidity location'.split(' ')
    mapping_names = [f'{names[i]}-to-{names[i+1]}' for i in range(len(names)-1)]
    source = seed
    for mapping_name in mapping_names:
        dest = find_dest(source, maps[mapping_name])
        # print(f'{source} -> {mapping_name} -> {dest}')
        source = dest
    return dest

def next_line(my_input, i) -> str:
    try:
        line = my_input[i]
    except:
        line = ''
    # print(i, f'"{line}"')
    return line

def find_dest(source, mapping: dict[tuple[int, int], int]):
    for src_begin, src_end in mapping.keys():
        if source >= src_begin and source < src_end:
            return source + mapping[(src_begin, src_end)]
    return source

def order_tuple_keys(mapping: dict[tuple[int, int], int]):
    return(sorted(list(mapping.keys())))

def solution1(my_input: list[str]):
    maps: dict[str, dict[str, dict[int, int]]] = {}
    seeds: list[int] = [int(x) for x in my_input[0].split(' ')[1:]]
    i = 2
    while i < len(my_input):
        line = next_line(my_input, i)
        try:
            if line.endswith(' map:'):
                key = line.split(' ')[0]
                mapping = []
                i += 1
                line = next_line(my_input, i)
                while line:
                    mapping.append(tuple([int(x) for x in line.split(' ')]))
                    i += 1
                    line = next_line(my_input, i)
                maps[key] = map_source_to_destination(mapping)
            i += 1
        except BaseException as e:
            print(f'ERROR:   "{line}"')
            raise e
    closest_location = maxsize
    for seed in seeds:
        location = map_seed_to_location(seed, maps)
        closest_location = min(closest_location, location)
    return closest_location

def solution2(my_input: list[str]):
    maps: dict[str, dict[str, dict[int, int]]] = {}
    seed_nums: list[int] = [int(x) for x in my_input[0].split(' ')[1:]]
    seeds: list[tuple[int, int]] = []
    for i in range(len(seed_nums)//2):
        seeds.append(tuple([seed_nums[2*i], seed_nums[2*i+1]]))

    i = 2
    while i < len(my_input):
        line = next_line(my_input, i)
        try:
            if line.endswith(' map:'):
                key = line.split(' ')[0]
                mapping = []
                i += 1
                line = next_line(my_input, i)
                while line:
                    mapping.append(tuple([int(x) for x in line.split(' ')]))
                    i += 1
                    line = next_line(my_input, i)
                maps[key] = map_source_to_destination(mapping, False)
            i += 1
        except BaseException as e:
            print(f'ERROR:   "{line}"')
            raise e
    closest_location = maxsize
    # print(seeds)
    for start,end in seeds:
        for seed in range(start, start+end):
            # print(seed)
            location = map_seed_to_location(seed, maps)
            closest_location = min(closest_location, location)
    return closest_location
    # closest_location = maxsize
    # print(seeds)
    # print(maps['humidity-to-location'])
    # for (start,end) in order_tuple_keys(maps['humidity-to-location']):
    #     print(start, end)
        # for i in range(start, start+end):
        #     print(i)
        #     x = find_dest(i, maps['humidity-to-location'])
        #     if i == 46:
        #         if x:
        #             print('x')
        #             return x
        #         else:
        #             print('nope')
        #             return None

    # for seed in seeds:
    #     location = map_seed_to_location(seed, maps)
    #     # print(location)
    #     closest_location = min(closest_location, location)
    return closest_location

if __name__ == '__main__':
    print('---- Part One ----')
    print(solution1(open('sample1.txt', 'r').read().split('\n')))
    print(solution1(open('input.txt', 'r').read().split('\n')))
    print('---- Part Two ----')
    print(solution2(open('sample2.txt', 'r').read().split('\n')))
    # print(solution2(open('input.txt', 'r').read().split('\n')))

#!/usr/bin/env python3
from collections import defaultdict
from copy import copy
from sys import maxsize

class Interval:
    def __init__(self, start: int, range_length: int):
        self.first = start
        self.last = start + (range_length - 1)
        self.interval = range(start, start + range_length)
    
    @classmethod
    def new(cls, start: int, last: int) -> "Interval":
        return Interval(start, last - start + 1)        
    
    def __len__(self):
        return self.last - self.first + 1
    
    def __contains__(self, item):
        return item >= self.first and item <= self.last

    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return str((self.first, self.last))

    def __hash__(self):
        return hash((self.first, self.last))

    def __lt__(self, other):
        return self.first < other.first

    def __le__(self, other):
        return self.first <= other.first

    def __gt__(self, other):
        return self.first > other.first

    def __ge__(self, other):
        return self.first >= other.first

    def __eq__(self, other):
        return self.first == other.first

    def __ne__(self, other):
        return self.first != other.first


    def intersect(self, other: "Interval") -> "Interval":
        if self.first in other.interval:
            if self.last in other.interval:
                return Interval(self.first, len(self))
            return Interval(self.first, other.last - self.first + 1)
        elif other.first in self.interval:
            if other.last in self.interval:
                return Interval(other.first, len(other))
            return Interval(other.first, self.last - other.first + 1)
        return None # copy(self)

    def remove(self, other: "Interval") -> list["Interval"]:
        if self.first in other.interval:
            # O..S
            if self.last in other.interval:
                # O..S..O
                return []
            return [Interval.new(other.last + 1, self.last)]
        elif other.first in self.interval:
            # S..O
            remaining = [Interval.new(self.first, other.first - 1)]
            if other.last in self.interval:
                # S..O..S
                remaining.append(Interval.new(other.last + 1, self.last))
            return remaining
        return [copy(self)]


class Mapping:
    def __init__(self, mapping: dict[Interval, Interval]):
        self.mapping = mapping

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str({str(k):str(v) for k,v in self.mapping.items()})

    def map_interval(self, interval: Interval) -> list[Interval]: # returns list of destination intervals
        result = []
        remaining = [interval]
        for source, destination in self.mapping.items():
            delta = destination.first - source.first
            inter = interval.intersect(source)
            if(inter):
                result.append(Interval(inter.first + delta, len(inter)))
                for i in remaining:
                    r = i.remove(inter)
                remaining = r

        # TODO - add back in the unmapped ones

        # print(self, interval, remaining, result)
        return remaining + result

def map_source_to_destination(mapping: list[(int, int, int)]) -> dict[tuple[int, int], int]:
    result: dict[int, int] = {}
    for row in mapping:
        d, s, r = row
        result[(s, s+r)] = d - s
    return result

def map_source_to_destination2(mapping: list[(int, int, int)]) -> Mapping:
    result: dict[Interval, Interval] = {}
    for row in mapping:
        d, s, r = row
        src = Interval(s, r)
        dest = Interval(d, r)
        result[src] = dest
    return Mapping(result)

def map_seed_to_location(seed, maps):
    names = 'seed soil fertilizer water light temperature humidity location'.split(' ')
    mapping_names = [f'{names[i]}-to-{names[i+1]}' for i in range(len(names)-1)]
    source = seed
    for mapping_name in mapping_names:
        dest = find_dest(source, maps[mapping_name])
        # print(f'{source} -> {mapping_name} -> {dest}')
        source = dest
    return dest

def map_seed_to_location2(seed: Interval, maps: dict[str, Mapping]):
    names = 'seed soil fertilizer water light temperature humidity location'.split(' ')
    mapping_names = [f'{names[i]}-to-{names[i+1]}' for i in range(len(names)-1)]
    sources = [seed]
    for mapping_name in mapping_names:
        destinations = []
        m = maps[mapping_name]
        for source in sources:
            dests = m.map_interval(source)
            destinations += dests if dests else [copy(source)]
        # print(f'{sources} -> {mapping_name}{maps[mapping_name]} -> {destinations}')
        sources = destinations
    return destinations
'''
seed number 82
which corresponds to soil 84
fertilizer 84
water 84
light 77
temperature 45
humidity 46
location 46
'''
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

def solution1(my_input: list[str]):
    maps: dict[str, Mapping] = {}
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
                maps[key] = map_source_to_destination2(mapping)
            i += 1
        except BaseException as e:
            print(f'ERROR:   "{line}"')
            raise e
    closest_location = maxsize
    for s in seeds:
        seed = Interval(s, 1)
        location = min(min(map(lambda location: location.interval, map_seed_to_location2(seed, maps))))
        # print(location)
        closest_location = min(location, closest_location)
    return closest_location

def solution2(my_input: list[str]):
    maps: dict[str, Mapping] = {}
    seed_nums: list[int] = [int(x) for x in my_input[0].split(' ')[1:]]
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
                maps[key] = map_source_to_destination2(mapping)
            i += 1
        except BaseException as e:
            print(f'ERROR:   "{line}"')
            raise e
    seeds: list[Interval] = []
    for i in range(len(seed_nums)//2):
        seeds.append(Interval(seed_nums[2*i], seed_nums[2*i+1]))
    # print(seeds)
    closest_location = maxsize
    for seed in seeds:
        # print(seed)
        locations = map_seed_to_location2(seed, maps)
        # print(locations)
        location = min(locations).first
        closest_location = min(location, closest_location)
    # print('=======')
    # print(min(map_seed_to_location2(Interval(79, 14), maps)).first)
    return closest_location

# def solution2(my_input: list[str]):
#     maps: dict[str, Mapping] = {}
#     seeds: list[int] = [int(x) for x in my_input[0].split(' ')[1:]]
#     i = 2
#     maps: dict[str, dict[str, dict[int, int]]] = {}
#     seed_nums: list[int] = [int(x) for x in my_input[0].split(' ')[1:]]
#     seeds: list[tuple[int, int]] = []
#     for i in range(len(seed_nums)//2):
#         seeds.append(tuple([seed_nums[2*i], seed_nums[2*i+1]]))

#     i = 2
#     while i < len(my_input):
#         line = next_line(my_input, i)
#         try:
#             if line.endswith(' map:'):
#                 key = line.split(' ')[0]
#                 mapping = []
#                 i += 1
#                 line = next_line(my_input, i)
#                 while line:
#                     mapping.append(tuple([int(x) for x in line.split(' ')]))
#                     i += 1
#                     line = next_line(my_input, i)
#                 maps[key] = map_source_to_destination(mapping, False)
#             i += 1
#         except BaseException as e:
#             print(f'ERROR:   "{line}"')
#             raise e
#     closest_location = maxsize
#     # print(seeds)
#     for start,end in seeds:
#         for seed in range(start, start+end):
#             # print(seed)
#             location = map_seed_to_location(seed, maps)
#             closest_location = min(closest_location, location)
#     return closest_location
#     # closest_location = maxsize
#     # print(seeds)
#     # print(maps['humidity-to-location'])
#     # for (start,end) in order_tuple_keys(maps['humidity-to-location']):
#     #     print(start, end)
#         # for i in range(start, start+end):
#         #     print(i)
#         #     x = find_dest(i, maps['humidity-to-location'])
#         #     if i == 46:
#         #         if x:
#         #             print('x')
#         #             return x
#         #         else:
#         #             print('nope')
#         #             return None

#     # for seed in seeds:
#     #     location = map_seed_to_location(seed, maps)
#     #     # print(location)
#     #     closest_location = min(closest_location, location)
#     return closest_location

if __name__ == '__main__':
    print('---- Part One ----')
    print(solution1(open('sample1.txt', 'r').read().split('\n')))
    print(solution1(open('input.txt', 'r').read().split('\n')))
    print('---- Part Two ----')
    print(solution2(open('sample2.txt', 'r').read().split('\n')))
    print(solution2(open('input.txt', 'r').read().split('\n')))

    # seed = Interval(79, 2)
    # seed_to_soil = Mapping({Interval(98, 2): Interval(50, 2), Interval(50, 48): Interval(52, 48)})
    # print(seed_to_soil.map_interval(seed))

    # int1 = Interval.new(79, 98)
    # int2 = Interval.new(42, 60)
    # int3 = Interval.new(99, 150)
    # int4 = Interval.new(84, 90)
    # print(int1.remove(int2)) # O  S
    # print(int1.remove(int3)) # S  O
    # print(int1.remove(int4)) # S..O..S
    # print(int4.remove(int1)) # O..S..O


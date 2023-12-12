#!/usr/bin/env python3
from math import gcd

class NetworkNode:
    def __init__(self, name: str, left: str, right: str):
        self.name: str = name
        self.left: str = left
        self.right: str = right
        self.Zs: list[int] = []

    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f'{self.name}:({self.left},{self.right})'

    def is_A(self):
        return self.name[2] == 'A'

    def is_Z(self):
        return self.name[2] == 'Z'

    def left_target(self, network: "NetworkMap") -> "NetworkNode":
        return network.network[self.left]

    def right_target(self, network: "NetworkMap") -> "NetworkNode":
        return network.network[self.right]

    def visit_target(self, network: "NetworkMap", direction: str, step: int, original_node: "NetworkNode") -> "NetworkNode":
        # print(self, direction, step)
        target: "NetworkNode" = self.left_target(network) if direction == 'L' else self.right_target(network)
        if target.is_Z():
            Z = tuple([step, target.name])
            # print(Z)
            original_node.Zs.append(step)
        return target

#####

def lcm(a: list[int]):
    result = 1
    for i in a:
        result = result*i//gcd(result, i)
    return result

class NetworkMap:
    def __init__(self, network: dict[str, NetworkNode]):
        self.network = network

    @classmethod
    def new(cls, my_input: list[str]) -> "NetworkMap":
        network: dict[str, NetworkNode] = {}
        for line in my_input:
            name = line[:3]
            left = line[7:10]
            right = line[12:15]
            network[name] = NetworkNode(name, left, right)
        return cls(network)
    
    def traverse(self, directions: list[str]) -> list[str]:
        node = self.network['AAA']
        path = [node.name]
        # print(node)
        while True:
            for d in directions:
                node = self.network[node.left if d == 'L' else node.right]
                path.append(node.name)
                # print(node)
                if node.name == 'ZZZ':
                    return path

    def find_Zs(self, directions: list[str]) -> int:
        step: int = 0
        As: list[NetworkNode] = list(filter(lambda node: node.is_A(), self.network.values()))
        num_Zs = len(list(filter(lambda node: node.is_Z(), self.network.values())))
        paths_to_try: list[NetworkNode] = As
        while paths_to_try:
            for d in directions:
                if not step % 500:
                    pass
                    # print('.', end='', flush=True)
                # print(paths_to_try, '->', d)
                # input()
                # next_paths: list[NetworkNode] = list(map(lambda node: node.visit_target(self, d, step), paths_to_try))
                next_paths: list[NetworkNode] = list(map(lambda i: paths_to_try[i].visit_target(self, d, step, As[i]), range(num_Zs)))
                Z_nodes: list[NetworkNode] = list(filter(lambda node: node.is_Z(), next_paths))
                As_with_at_least_two_Zs: list[NetworkNode] = list(filter(lambda node: len(node.Zs) > 1, As))
                if (len(Z_nodes) == num_Zs or len(As_with_at_least_two_Zs) == len(As) or step > 1000000):
                    print(f'\n{step} {next_paths}')
                    print(f'\n{step} {Z_nodes}')
                    print(f'\n{step} {As_with_at_least_two_Zs}')
                    deltas: list[int] = []
                    for A in As:
                        deltas.append(A.Zs[1] - A.Zs[0])
                        print(f'{A}: {A.Zs}')
                    return lcm(deltas)
                step += 1
                paths_to_try = next_paths
        return step

#####

def solution1(my_input: list[str]) -> int:
    directions = list(my_input[0])
    network = NetworkMap.new(my_input[2:])
    path = network.traverse(directions)
    # print(' -> '.join(path))
    return len(path) - 1

def solution2(my_input: list[str]) -> int:
    directions = list(my_input[0])
    network = NetworkMap.new(my_input[2:])
    return network.find_Zs(directions)

if __name__ == '__main__':
    # print('---- Part One ----')
    # print(solution1(open('sample.txt', 'r').read().split('\n')))
    # print(solution1(open('sample1.txt', 'r').read().split('\n')))
    # print(solution1(open('input.txt', 'r').read().split('\n')))
    # print('---- Part Two ----')
    # print(solution2(open('sample2.txt', 'r').read().split('\n')))
    # print(solution2(open('sample1.txt', 'r').read().split('\n')))
    print(solution2(open('input.txt', 'r').read().split('\n')))
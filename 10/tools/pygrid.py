#!/usr/bin/env python3
import pygame

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.to_tuple())

    def __repr__(self):
        return str(self)
    
    def to_tuple(self):
        return (self.x, self.y)

class PyGridCell:
    def __init__(self, pos: Position, value):
        self.pos = pos
        self.value = value

    def __repr__(self):
        return f'"{self.value}"@{self.pos}'

    def __str__(self):
        return str(self.value)

class PyGrid:
    def __init__(self, width: int, height: int, default_value = ''):
        self.width = width
        self.height = height
        self.grid: dict[tuple, PyGridCell] = {}
        for h in range(height):
            for w in range(width):
                self.grid[Position(w, h).to_tuple()] = PyGridCell(Position(w, h), default_value)

    def show(self):
        pass

    def __str__(self):
        output = []
        for h in range(self.height):
            s = ''
            for w in range(self.width):
                s += str(self.grid[Position(w, h).to_tuple()])
            output.append(s)
        return '\n'.join(output)

if '__main__' == __name__:
    print(PyGrid(4, 3, '.'))
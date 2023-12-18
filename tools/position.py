class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __str__(self):
        return str((self.x, self.y))
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def to_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)
    
    def north(self) -> tuple[int, int]:
        return (self.x, self.y - 1)

    def south(self) -> tuple[int, int]:
        return (self.x, self.y + 1)

    def east(self) -> tuple[int, int]:
        return (self.x + 1, self.y)

    def west(self) -> tuple[int, int]:
        return (self.x - 1, self.y)

    def neighbors(self) -> list[tuple[int, int]]:
        return [self.north(), self.south(), self.east(), self.west()]

    def go_north(self):
        self.x, self.y = self.north()

    def go_south(self):
        self.x, self.y = self.south()

    def go_east(self):
        self.x, self.y = self.east()

    def go_west(self):
        self.x, self.y = self.west()

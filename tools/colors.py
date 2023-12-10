from enum import Enum

class Color(Enum):
    GREY = 90
    RED = 91
    GREEN = 92
    YELLOW = 93
    BLUE = 94
    MAGENTA = 95
    CYAN = 96
    WHITE = 97

def highlight(c: Color, s: str):
    return f'\033[{c.value}m{s}\033[00m'

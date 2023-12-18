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

def highlight(c: Color, s: str) -> str:
    return f'\033[{c.value}m{s}\033[00m'

def highlight_rgb(rgb: tuple[int, int, int], s: str) -> str:
    red, blue, green = rgb
    return f'\033[38;2;{red};{blue};{green};16m{s}\033[00m'

# strings like #70c710 (# optional) become a tuple like (112, 199, 16)'
def rgb_from_hex(hex_str: str) -> tuple[int, int, int]:
    start = 1 if hex_str[0] == '#' else 0
    red = int(hex_str[start:start+2], base=16)
    green = int(hex_str[start+2:start+4], base=16)
    blue = int(hex_str[start+4:start+6], base=16)
    return (red, green, blue)
    
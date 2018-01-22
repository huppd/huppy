""" useful constants for line, color and marker styles """
from itertools import cycle


# LINES = ['--', '-.', ':', '-']*2
LINES = ['--', '-.', ':']*4
LINEC = cycle(LINES)
# COLORS = ['b', 'g', 'r', 'c', 'm', 'y']*2
COLORS = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
COLORC = cycle(COLORS)
MARKERS = ['o', 'v', '*', 'x', 'd', '^', '2', '>', '4', 'p', 's', 'p', '8',
           'h', 'H', '+', 'p', 'D', '3', '|', '_', 'TICKLEFT', 'TICKRIGHT',
           'TICKDOWN', 'CARETLEFT', 'CARETRIGHT', 'CARETUP', 'CARETDOWN', '.']

MARKERC = cycle(MARKERS)

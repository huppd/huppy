""" useful constants for line, color and marker styles """
from itertools import cycle


LINES = ['--', '-.', ':', '-']
LINEC = cycle(LINES)
COLORS = ['b', 'g', 'r', 'c', 'm', 'y']
COLORC = cycle(COLORS)
MARKERS = ['o', 'v', '*', 'x', 'd', '^', '2', '>', '4', 'p', 's', 'p', '8',
           'h', 'H', '+', 'p', 'D', '3', '|', '_', 'TICKLEFT', 'TICKRIGHT',
           'TICKDOWN', 'CARETLEFT', 'CARETRIGHT', 'CARETUP', 'CARETDOWN', '.']

MARKERC = cycle(MARKERS)

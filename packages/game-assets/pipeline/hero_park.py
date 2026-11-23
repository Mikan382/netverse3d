from math import cos, pi, sin

from hero_kit import HeroPart
from hero_solid import rbox


def build_tile(variant):
    part = HeroPart(f'park_tile_{variant}')
    rbox(part, (0, 0, 0.07), (4, 4, 0.14), 'trim' if variant == 'a' else 'floor')
    if variant != 'a':
        for row in range(4):
            for column in range(4):
                x = column - 1.5
                y = row - 1.5
                rbox(part, (x, y, 0.148), (0.984, 0.984, 0.016),
                     'top' if (row + column) % 4 == 0 else 'floor')
    if variant == 'c':
        rbox(part, (-1.83, 0, 0.16), (0.32, 3.98, 0.16), 'metal', radius=0.025)
    return part


def foliage(part, center, radius, height, row):
    part.revolve(center, 'z', [(0.18 * radius, 0, row), (radius, height * 0.40, row),
                               (0.76 * radius, height * 0.77, row), (0.14 * radius, height, row)],
                 segments=8)


def build_tree(variant):
    part = HeroPart(f'park_tree_{variant}')
    height = 5.2 if variant == 'a' else 3.5
    spread = 1.15 if variant == 'a' else 0.75
    part.revolve((0, 0, 0), 'z', [(0.18, 0, 'body'), (0.13, height * 0.6, 'body'),
                                  (0.06, height * 0.85, 'soft')], segments=9)
    for index in range(5):
        angle = 2 * pi * index / 5
        x, y = spread * cos(angle), spread * sin(angle)
        z = height * (0.54 + 0.035 * (index % 3))
        part.tube([(0, 0, height * 0.38), (x, y, z + 0.22)], 0.08, 'body', sides=6)
        foliage(part, (x, y, z), spread * 0.89, height * 0.30, 'trim')
    foliage(part, (0.10, 0.08, height * 0.72), spread, height * 0.30, 'trim')
    return part


def build_planting(variant):
    part = HeroPart(f'park_planting_{variant}')
    rbox(part, (0, 0, 0.10), (1.84, 0.76, 0.20), 'wall', radius=0.06)
    for index in range(5):
        x = (index - 2) * 0.31
        y = 0.11 if index % 2 == 0 else -0.13
        foliage(part, (x, y, 0.18), 0.26, 0.54 if variant == 'a' else 0.30, 'trim')
        if variant == 'b':
            foliage(part, (x, y, 0.44), 0.10, 0.12, 'top')
    return part


def build_seat():
    part = HeroPart('park_seat_a')
    for x in (-0.72, 0.72):
        rbox(part, (x, 0, 0.21), (0.22, 0.60, 0.42), 'wall', radius=0.04)
    rbox(part, (0, 0, 0.47), (1.92, 0.53, 0.13), 'top', radius=0.05)
    rbox(part, (0, 0.21, 0.67), (1.85, 0.13, 0.28), 'wall', radius=0.045)
    return part


def build_lamp():
    part = HeroPart('park_lamp_a')
    rings = [(0.19, 0, 'wall'), (0.16, 0.12, 'metal'), (0.055, 0.20, 'metal'),
             (0.048, 1.24, 'metal'), (0.14, 1.40, 'strip'), (0.14, 1.48, 'metal'),
             (0.16, 1.55, 'metal')]
    part.revolve((0, 0, 0), 'z', rings, segments=14)
    return part


def build_bin():
    part = HeroPart('park_bin_a')
    part.revolve((0, 0, 0), 'z', [(0.17, 0, 'metal'), (0.21, 0.76, 'body'),
                                  (0.22, 0.80, 'metal'), (0.18, 0.91, 'trim')], segments=14)
    rbox(part, (0, -0.191, 0.743), (0.23, 0.06, 0.13), 'soft', radius=0.018)
    return part


def build_gate():
    part = HeroPart('park_gate_a')
    for x in (-1.65, 1.65):
        rbox(part, (x, 0, 1.25), (0.34, 0.44, 2.50), 'wall', radius=0.04)
        rbox(part, (x, -0.234, 1.38), (0.065, 0.045, 1.75), 'strip')
    rbox(part, (0, 0, 2.72), (3.72, 0.48, 0.48), 'metal', radius=0.09)
    rbox(part, (0, -0.254, 2.72), (2.68, 0.05, 0.098), 'trim')
    return part


def build_fountain():
    part = HeroPart('park_fountain_a')
    rim = [(1.62, 0, 'wall'), (1.78, 0.16, 'wall'), (1.78, 0.43, 'metal'),
           (1.66, 0.50, 'top'), (1.52, 0.49, 'wall'), (1.48, 0.24, 'wall')]
    part.revolve((0, 0, 0), 'z', rim, segments=28)
    part.revolve((0, 0, 0), 'z', [(1.51, 0.26, 'body'), (1.51, 0.31, 'body')], segments=28)
    part.revolve((0, 0, 0), 'z', [(0.40, 0.20, 'wall'), (0.24, 0.72, 'metal'),
                                  (0.33, 0.89, 'trim')], segments=18)
    for index in range(8):
        angle = 2 * pi * index / 8
        part.revolve((1.61 * cos(angle), 1.61 * sin(angle), 0), 'z',
                     [(0.045, 0.494, 'strip'), (0.045, 0.508, 'strip')], segments=8)
    return part


def build_playground():
    part = HeroPart('park_play_a')
    for x in (-0.71, 0.71):
        for y in (-0.35, 0.70):
            rbox(part, (x, y, 0.90), (0.12, 0.12, 1.8), 'metal', radius=0.018)
    rbox(part, (0, 0.15, 1.25), (1.49, 1.15, 0.14), 'trim', radius=0.03)
    for x in (-0.57, 0.57):
        part.tube([(x, 0.72, 1.29), (x, 1.35, 0.03)], 0.045, 'metal', sides=6)
    for index in range(5):
        y = 1.22 - index * 0.11
        part.tube([(-0.57, y, 0.31 + index * 0.19), (0.57, y, 0.31 + index * 0.19)],
                  0.035, 'metal', sides=6)
    part.prism_x([(-2.26, 0.13), (-1.93, 0.17), (-0.35, 1.26),
                  (-0.35, 1.36), (-1.95, 0.26), (-2.26, 0.21)], -0.50, 0.50, 'top')
    for x in (-0.51, 0.51):
        part.tube([(x, -0.37, 1.41), (x, -1.93, 0.32), (x, -2.25, 0.27)], 0.052, 'metal', sides=6)
    rbox(part, (0, 0.20, 2.02), (1.71, 1.33, 0.17), 'trim', radius=0.06)
    return part


def build_park_parts():
    return (*[build_tile(variant) for variant in 'abc'], *[build_tree(variant) for variant in 'ab'],
            *[build_planting(variant) for variant in 'ab'], build_seat(), build_lamp(), build_bin(),
            build_gate(), build_fountain(), build_playground())

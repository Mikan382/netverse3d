from math import cos, pi, sin
from random import Random

from hero_kit import HeroPart
from hero_solid import obox, rbox
from hero_vegetation import build_woody_tree, foliage


def build_tile(variant):
    part = HeroPart(f'park_tile_{variant}')
    grass = variant == 'a'
    rbox(part, (0, 0, 0.068), (4, 4, 0.136), 'grass' if grass else 'metal')
    if grass:
        rng = Random(22)
        for _ in range(66):
            x, y = rng.uniform(-1.91, 1.91), rng.uniform(-1.91, 1.91)
            height = rng.uniform(0.027, 0.075)
            for blade in range(3):
                angle = blade * 2 * pi / 3 + x
                reach = 0.041 * cos(angle), 0.041 * sin(angle)
                part.poly([(x - reach[1] * 0.2, y + reach[0] * 0.2, 0.136),
                           (x + reach[1] * 0.2, y - reach[0] * 0.2, 0.136),
                           (x + reach[0], y + reach[1], 0.136 + height)], 'grass')
        return part
    for row in range(4):
        for column in range(4):
            x, y = column - 1.5, row - 1.5
            rbox(part, (x, y, 0.15), (0.978, 0.978, 0.026),
                 'top' if (row + column) % 4 == 0 else 'floor', radius=0.008)
    if variant == 'c':
        for y in (-1.5, -0.5, 0.5, 1.5):
            rbox(part, (-1.805, y, 0.178), (0.34, 0.984, 0.129), 'wall', radius=0.022, segments=2)
    return part


def build_tree(variant):
    part = HeroPart(f'park_tree_{variant}')
    height, spread, seed = (5.2, 1.18, 64) if variant == 'a' else (3.5, 0.84, 123)
    build_woody_tree(part, height, spread, seed)
    return part


def build_planting(variant):
    part = HeroPart(f'park_planting_{variant}')
    rbox(part, (0, 0, 0.11), (1.83, 0.75, 0.22), 'wall', radius=0.057, segments=2)
    rbox(part, (0, 0, 0.187), (1.57, 0.54, 0.077), 'body', radius=0.021)
    for x in (-0.83, 0.83):
        rbox(part, (x, 0, 0.23), (0.15, 0.70, 0.074), 'metal', radius=0.018)
    for y in (-0.327, 0.327):
        rbox(part, (0, y, 0.242), (1.48, 0.089, 0.073), 'metal', radius=0.014)
    flower = variant == 'b'
    for index in range(5):
        x, y = (index - 2) * 0.31, 0.07 if index % 2 else -0.09
        foliage(part, (x, y, 0.21), 0.245, (0.26 if flower else 0.46) + index % 3 * 0.04,
                16 + index, segments=12)
        if flower:
            z = 0.49 + (index % 3) * 0.04
            part.tube([(x, y, 0.34), (x + 0.027, y - 0.06, z)], 0.012, 'foliage', sides=6)
            for petal in range(5):
                angle = petal * 2 * pi / 5
                part.revolve((x + 0.027 + 0.038 * cos(angle), y - 0.06 + 0.038 * sin(angle), z - 0.012),
                             'z', [(0.008, 0, 'top'), (0.033, 0.018, 'top'), (0.01, 0.031, 'metal')], segments=7)
    return part


def build_seat():
    part = HeroPart('park_seat_a')
    for x in (-0.72, 0.72):
        rbox(part, (x, 0, 0.045), (0.26, 0.60, 0.09), 'wall', radius=0.025, segments=2)
        for y, angle in ((-0.18, -1), (0.18, 1)):
            obox(part, (x, y, 0.075), (x, y - angle * 0.04, 0.417),
                 0.085, 0.091, 'metal', radius=0.012)
        obox(part, (x, 0.15, 0.39), (x, 0.278, 0.79), 0.082, 0.082, 'metal', radius=0.012)
        part.tube([(x, -0.14, 0.48), (x, -0.14, 0.615), (x, -0.07, 0.65), (x, 0.21, 0.65)],
                  0.025, 'metal', sides=10)
    rbox(part, (0, 0, 0.393), (1.61, 0.39, 0.061), 'metal', radius=0.012)
    for index in range(5):
        y = (index - 2) * 0.094
        rbox(part, (0, y, 0.434 + abs(index - 2) * 0.004), (1.91, 0.084, 0.06),
             'top' if index % 2 == 0 else 'wall', radius=0.013, segments=2)
    for index in range(3):
        rbox(part, (0, 0.215 + index * 0.02, 0.581 + index * 0.086), (1.91, 0.071, 0.073),
             'top', radius=0.013, segments=2)
    return part


def build_lamp():
    part = HeroPart('park_lamp_a')
    part.revolve((0, 0, 0), 'z', [(0.18, 0, 'wall'), (0.18, 0.052, 'wall'),
                                  (0.115, 0.085, 'metal'), (0.105, 0.18, 'metal'),
                                  (0.061, 0.22, 'metal'), (0.052, 1.19, 'metal'),
                                  (0.086, 1.24, 'metal')], segments=24)
    part.revolve((0, 0, 1.24), 'z', [(0.103, 0, 'metal'), (0.12, 0.035, 'metal'),
                                     (0.122, 0.058, 'warm_lamp'), (0.115, 0.165, 'warm_lamp'),
                                     (0.118, 0.189, 'metal'), (0.161, 0.22, 'wall'),
                                     (0.161, 0.25, 'metal'), (0.118, 0.284, 'metal'),
                                     (0.035, 0.31, 'top')], segments=24)
    for index in range(6):
        angle = index * pi / 3
        x, y = 0.124 * cos(angle), 0.124 * sin(angle)
        part.tube([(x, y, 1.286), (x, y, 1.444)], 0.012, 'metal', sides=8)
    return part


def build_gate():
    part = HeroPart('park_gate_a')
    for x in (-1.64, 1.64):
        rbox(part, (x, 0, 0.16), (0.44, 0.52, 0.32), 'wall', radius=0.034, segments=2)
        rbox(part, (x, 0, 1.31), (0.26, 0.31, 2.23), 'metal', radius=0.021, segments=2)
        rbox(part, (x, -0.168, 1.45), (0.081, 0.028, 1.62), 'warm_lamp', radius=0.007)
        for z in (0.39, 2.33):
            rbox(part, (x, 0, z), (0.35, 0.40, 0.084), 'wall', radius=0.017)
    rbox(part, (0, 0, 2.56), (3.65, 0.46, 0.19), 'wall', radius=0.027, segments=2)
    rbox(part, (0, 0, 2.73), (3.44, 0.36, 0.17), 'metal', radius=0.026)
    for x in (-1.38, -0.92, -0.46, 0, 0.46, 0.92, 1.38):
        rbox(part, (x, -0.192, 2.733), (0.26, 0.052, 0.062), 'top', radius=0.009)
    return part


def build_fountain():
    part = HeroPart('park_fountain_a')
    bowl = [(1.50, 0, 'wall'), (1.66, 0.06, 'wall'), (1.71, 0.16, 'metal'),
            (1.68, 0.23, 'wall'), (1.72, 0.31, 'wall'), (1.77, 0.405, 'metal'),
            (1.77, 0.45, 'metal'), (1.74, 0.49, 'top'), (1.57, 0.49, 'top'),
            (1.52, 0.455, 'metal'), (1.47, 0.25, 'wall'), (1.46, 0.22, 'wall')]
    part.revolve((0, 0, 0), 'z', bowl, segments=48)
    part.oriented_poly([(1.507 * cos(i * pi / 24), 1.507 * sin(i * pi / 24), 0.414) for i in range(48)],
                       (0, 0, 1), 'body')
    part.revolve((0, 0, 0), 'z', [(0.43, 0.38, 'wall'), (0.45, 0.42, 'wall'),
                                  (0.29, 0.49, 'metal'), (0.19, 0.61, 'metal'),
                                  (0.22, 0.77, 'metal'), (0.34, 0.84, 'top'),
                                  (0.29, 0.89, 'cool_water'), (0.075, 0.9, 'cool_water')], segments=28)
    for index in range(10):
        angle = index * pi / 5
        part.revolve((1.61 * cos(angle), 1.61 * sin(angle), 0), 'z',
                     [(0.044, 0.487, 'metal'), (0.046, 0.500, 'metal'),
                      (0.036, 0.516, 'cool_water'), (0.007, 0.516, 'cool_water')], segments=10)
    return part


def build_playground():
    part = HeroPart('park_play_a')
    for x in (-0.68, 0.68):
        for y in (-0.32, 0.64):
            rbox(part, (x, y, 0.06), (0.21, 0.21, 0.12), 'wall', radius=0.022)
            rbox(part, (x, y, 0.965), (0.12, 0.12, 1.80), 'metal', radius=0.018, segments=2)
        part.tube([(x, -0.29, 1.36), (x, -0.29, 1.705), (x, 0.58, 1.705),
                   (x, 0.63, 1.47)], 0.032, 'metal', sides=10)
        for y in (-0.15, 0.08, 0.34):
            rbox(part, (x, y, 1.53), (0.048, 0.052, 0.34), 'top', radius=0.005)
    rbox(part, (0, 0.14, 1.17), (1.45, 1.02, 0.12), 'metal', radius=0.021)
    for index in range(8):
        x = (index - 3.5) * 0.174
        rbox(part, (x, 0.13, 1.25), (0.157, 0.96, 0.058), 'wall', radius=0.012)
    for x in (-0.54, 0.54):
        part.tube([(x, 1.34, 0.03), (x, 0.72, 1.27), (x, 0.57, 1.53)],
                  0.041, 'metal', sides=10)
    for index in range(5):
        y, z = 1.22 - index * 0.111, 0.27 + index * 0.195
        rbox(part, (0, y, z), (1.09, 0.13, 0.064), 'wall', radius=0.012)
    slide = [(-0.35, 1.27), (-0.65, 1.17), (-1.05, 0.91), (-1.55, 0.51),
             (-1.93, 0.26), (-2.24, 0.21), (-2.24, 0.146), (-1.92, 0.187),
             (-1.51, 0.447), (-1.02, 0.835), (-0.63, 1.087), (-0.35, 1.19)]
    part.prism_x(slide, -0.47, 0.47, 'top')
    for x in (-0.48, 0.48):
        part.tube([(x, y, z + 0.061) for y, z in slide[:6]], 0.051, 'metal', sides=12)
    for y, z in ((-1.38, 0.34), (-0.76, 0.76)):
        rbox(part, (0, y, z * 0.5), (0.146, 0.146, z), 'metal', radius=0.012)
    for index in range(5):
        x = (index - 2) * 0.328
        rbox(part, (x, 0.17, 1.91 + (2 - abs(index - 2)) * 0.055), (0.31, 1.25, 0.11),
             'top' if index % 2 == 0 else 'wall', radius=0.024)
    return part


def build_park_parts():
    return (*[build_tile(variant) for variant in 'abc'], *[build_tree(variant) for variant in 'ab'],
            *[build_planting(variant) for variant in 'ab'], build_seat(), build_lamp(), build_gate(),
            build_fountain(), build_playground())

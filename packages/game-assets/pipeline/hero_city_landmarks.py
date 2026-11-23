from math import cos, pi, sin

from hero_kit import HeroPart, smooth_table

CRESCENT_FLOORS = 58
CRESCENT_FLOOR_HEIGHT = 3
BUNDLED_FLOOR_HEIGHT = 4
CRESCENT_PROFILE = (
    (0, -2, 0, 13, 10), (18, -2, 0, 13.8, 10.4), (42, -1, 0, 13.6, 10.1),
    (68, 0.5, 0, 12.8, 9.2), (98, 2.5, 0, 11.4, 8.4), (126, 4, 0, 9.9, 7.5),
    (152, 4.8, 0, 8.6, 6.8), (171, 4.2, 0, 7.5, 6.3), (174, 3.9, 0, 6.8, 5.8),
)


def ellipse(z, cx, cy, rx, ry, segments):
    return [
        (cx + rx * cos(2 * pi * i / segments), cy + ry * sin(2 * pi * i / segments), z)
        for i in range(segments)
    ]


def crescent_ring(z, segments, inset=0, framed=False):
    columns = [tuple((ring[0], ring[i]) for ring in CRESCENT_PROFILE) for i in range(1, 5)]
    cx, cy, rx, ry = (smooth_table(column, z) for column in columns)
    if not framed:
        return ellipse(z, cx, cy, rx, ry, segments)
    angles = [2 * pi * (index + (0.80 if index % 2 else 0)) / segments for index in range(segments)]
    return [(cx + (rx - inset) * cos(angle), cy + (ry - inset) * sin(angle), z)
            for angle in angles]


def crescent_facade_row(row, column):
    floor, course = divmod(row, 3)
    if course == 0:
        return 'strip' if floor in (0, 39, 57) else 'metal'
    if course == 1 or column % 2 == 0:
        return 'metal'
    return 'screen' if (floor * 13 + column * 7) % 19 < 4 else 'wall'


def build_crescent_shaft(low=False):
    part = HeroPart('crescent_shaft_a_low' if low else 'crescent_shaft_a')
    segments = 12 if low else 32
    total = CRESCENT_FLOORS * CRESCENT_FLOOR_HEIGHT
    if low:
        rings = [crescent_ring(z, segments) for z in range(0, total + 1, 29)]
        part.loft(rings, lambda _r, _c: 'wall', levels=0)
    else:
        rings = []
        for floor in range(CRESCENT_FLOORS):
            z = floor * CRESCENT_FLOOR_HEIGHT
            rings.extend((crescent_ring(z, segments, framed=True),
                          crescent_ring(z + 0.16, segments, framed=True),
                          crescent_ring(z + 0.34, segments, inset=0.22, framed=True)))
        rings.append(crescent_ring(total, segments, framed=True))
        part.loft(rings, crescent_facade_row, levels=0, smooth=False)
    deck = [
        (120.0, 9, -7, 7.6, 6.6),
        (121.2, 13.5, -8.5, 12.5, 10.3),
        (124.2, 13.5, -8.5, 13.2, 10.9),
        (125.0, 13.5, -8.5, 12.7, 10.4),
    ]
    if not low:
        deck[2:2] = [(121.55, 13.5, -8.5, 13.08, 10.72),
                     (123.90, 13.5, -8.5, 12.84, 10.48)]
    part.loft([ellipse(*ring, segments) for ring in deck],
              lambda row, column: ('strip' if row == len(deck) - 2 else
                                    'screen' if not low and row == 2 and column % 4 else 'metal'),
              levels=0)
    if not low:
        for x in (9.5, 16.5):
            part.tube([(6, -6, 115), (x, -13, 122)], 0.32, 'metal', sides=6)
        for index in range(0, segments, 4):
            angle = 2 * pi * index / segments
            x, y = cos(angle), sin(angle)
            part.tube([(13.5 + x * 12.73, -8.5 + y * 10.35, 121.48),
                       (13.5 + x * 12.88, -8.5 + y * 10.49, 124.1)], 0.075, 'metal', sides=5)
    return part


def build_bundled_shaft(low=False):
    part = HeroPart('bundled_shaft_a_low' if low else 'bundled_shaft_a')
    towers = [
        (-10.2, -10.2, 11.4, 13.6, 124),
        (2.4, -8.9, 12.6, 11.4, 164),
        (13.5, -9.5, 9.2, 12.8, 104),
        (-10.8, 6.8, 12.4, 14.6, 148),
        (3.1, 5.4, 14.0, 15.4, 208),
        (15.4, 7.6, 10.0, 12.8, 180),
    ]
    for index, (x, y, width, depth, height) in enumerate(towers):
        layers = [(0, 0, 'wall')]
        if not low:
            for floor in range(BUNDLED_FLOOR_HEIGHT, height, BUNDLED_FLOOR_HEIGHT):
                layers.extend(((floor - 0.23, 0.13, 'screen' if (floor // BUNDLED_FLOOR_HEIGHT + index) % 7 == 0 else 'wall'),
                               (floor, -0.10, 'metal')))
            for side in (-1, 1):
                part.tube([(x + side * width * 0.31, y - depth / 2 - 0.03, 3),
                           (x + side * width * 0.31, y - depth / 2 - 0.03, height - 2)],
                          0.10, 'strip', sides=4)
        layers.extend([(height - 1.5, 0, 'strip'), (height, 0.5, 'top')])
        part.slab(x, y, width / 2, depth / 2, 1.1, layers, corner=1)
    crown = [ellipse(z, 3.1, 5.4, rx, ry, 8) for z, rx, ry in [
        (205.5, 3.8, 3.2), (209.5, 2.9, 2.5), (229, 0.06, 0.06),
    ]]
    part.loft(crown, lambda _r, _c: 'trim', levels=0, smooth=False)
    part.revolve((3.1, 5.4, 0), 'z', [(0.10, 229, 'accent'), (0.10, 229.4, 'accent')], segments=8)
    return part


def build_podium(name, width, depth, door_width, corner_radius):
    part = HeroPart(name)
    part.rounded_box((0, -4, 0.18), (width + 14, depth + 16, 0.36), 'floor', radius=0.15)
    part.slab(0, 0, width / 2, depth / 2, corner_radius, [
        (0.34, 0, 'wall'), (4.28, 0, 'wall'), (4.5, 0.2, 'top'),
    ])
    entrance_y = -depth / 2
    part.rounded_box((0, entrance_y + 0.15, 2.39), (door_width, 0.5, 3.1), 'metal', radius=0.12)
    part.rounded_box((0, entrance_y - 1.98, 3.46), (door_width + 2.4, 4.6, 0.54), 'trim', radius=0.12)
    stairs = [(entrance_y - 2.4, 0.35), (entrance_y + 0.1, 0.35), (entrance_y + 0.1, 0.84)]
    for index in reversed(range(3)):
        edge = entrance_y - 2.4 + index * 0.8
        stairs.extend([(edge, 0.52 + index * 0.16), (edge, 0.36 + index * 0.16)])
    stairs.pop()
    stair_half_width = door_width / 2 + 0.8
    part.prism_x(stairs, -stair_half_width, stair_half_width, 'top')
    for x in (-door_width / 2, door_width / 2):
        part.rounded_box((x, entrance_y - 0.12, 2.11), (0.3, 0.35, 2.54), 'metal', radius=0.06)
    part.rounded_box((0, entrance_y - 4.29, 3.48), (door_width + 1.8, 0.09, 0.11), 'strip', radius=0.02)
    return part


def build_landmark_parts():
    return (
        build_crescent_shaft(),
        build_podium('crescent_podium_a', 34, 28, 8, 3.2),
        build_bundled_shaft(),
        build_podium('bundled_podium_a', 46, 34, 10, 0.6),
        build_crescent_shaft(low=True),
        build_bundled_shaft(low=True),
    )

import math

from mathutils import Vector

from hero_kit import HeroPart, smooth_table

FLOAT = 0.008

TOWER_RADII = [
    (0.0, 6.2),
    (6.0, 5.9),
    (12.0, 5.5),
    (20.0, 5.0),
    (28.0, 4.5),
    (36.0, 4.0),
    (42.0, 3.7),
    (46.0, 3.5),
    (50.0, 3.0),
    (54.0, 2.4),
    (58.0, 1.6),
    (62.0, 0.7),
    (65.0, 0.15),
]


def pilaster_y(part, x, y, z0, z1, width, depth, side_sign, row='metal'):
    hw = width / 2.0
    yi = y - side_sign * 0.04
    yo = y + side_sign * depth
    part.poly([(x - hw, yi, z0), (x + hw, yi, z0), (x + hw, yo, z0), (x - hw, yo, z0)], row)
    part.poly([(x - hw, yo, z1), (x + hw, yo, z1), (x + hw, yi, z1), (x - hw, yi, z1)], row)
    part.poly([(x - hw, yi, z0), (x - hw, yo, z0), (x - hw, yo, z1), (x - hw, yi, z1)], row)
    part.poly([(x + hw, yo, z0), (x + hw, yi, z0), (x + hw, yi, z1), (x + hw, yo, z1)], row)
    part.poly([(x - hw, yo, z0), (x + hw, yo, z0), (x + hw, yo, z1), (x - hw, yo, z1)], row)


def pilaster_x(part, x, y, z0, z1, width, depth, side_sign, row='metal'):
    hd = width / 2.0
    xi = x - side_sign * 0.04
    xo = x + side_sign * depth
    part.poly([(xi, y - hd, z0), (xo, y - hd, z0), (xo, y + hd, z0), (xi, y + hd, z0)], row)
    part.poly([(xo, y - hd, z1), (xi, y - hd, z1), (xi, y + hd, z1), (xo, y + hd, z1)], row)
    part.poly([(xi, y - hd, z0), (xi, y - hd, z1), (xo, y - hd, z1), (xo, y - hd, z0)], row)
    part.poly([(xo, y + hd, z0), (xo, y + hd, z1), (xi, y + hd, z1), (xi, y + hd, z0)], row)
    part.poly([(xo, y - hd, z0), (xo, y + hd, z0), (xo, y + hd, z1), (xo, y - hd, z1)], row)


def tower_ring_points(z, segments=16):
    r = smooth_table(TOWER_RADII, z)
    points = []
    for i in range(segments):
        theta = 2.0 * math.pi * i / segments + math.pi / 4.0
        flare = 1.0 + 0.12 * math.cos(4.0 * theta)
        x = r * flare * math.cos(theta)
        y = r * flare * math.sin(theta)
        points.append(Vector((x, y, z)))
    return points


def tower_row_selector(ring_index, col_index):
    if ring_index in (0, 4, 8, 11):
        return 'top'
    if col_index % 4 == 0:
        return 'metal'
    if col_index % 2 == 0:
        return 'strip' if ring_index % 2 == 1 else 'metal'
    return 'screen' if (ring_index + col_index) % 2 == 0 else 'wall'


def build_tower(name='tower_a'):
    tower = HeroPart(name)
    z_stations = [0.0, 4.0, 8.0, 14.0, 20.0, 26.0, 32.0, 38.0, 44.0, 48.0, 52.0, 55.0]
    rings = [tower_ring_points(z) for z in z_stations]
    tower.loft(rings, tower_row_selector, levels=0, closed=True, cap=True, smooth=True)

    for i in range(8):
        theta = 2.0 * math.pi * i / 8.0
        x0 = 5.9 * math.cos(theta)
        y0 = 5.9 * math.sin(theta)
        tower.tube([(x0, y0, 0.08), (x0 * 0.92, y0 * 0.92, 7.8)], 0.3, 'metal', sides=6)

    tower.rounded_box((0, 0, 7.95), (12.8, 12.8, 0.3), 'top', radius=0.06, segments=1)

    deck_z = 44.8
    deck_cx = 0.0
    deck_cy = 3.4
    deck_radius = 3.0
    deck_thick = 0.5
    deck_rings = []
    for dz, dr in [
        (-0.25, deck_radius * 0.75),
        (0.0, deck_radius),
        (deck_thick, deck_radius),
    ]:
        ring = []
        for i in range(16):
            a = 2.0 * math.pi * i / 16.0
            ring.append(Vector((deck_cx + dr * math.cos(a), deck_cy + dr * math.sin(a), deck_z + dz)))
        deck_rings.append(ring)
    tower.loft(deck_rings, lambda r, c: 'top' if r == 1 else 'metal', levels=0, closed=True, cap=True, smooth=True)

    rail_pts = [
        Vector((deck_cx + (deck_radius - 0.08) * math.cos(2.0 * math.pi * i / 16.0),
                deck_cy + (deck_radius - 0.08) * math.sin(2.0 * math.pi * i / 16.0),
                deck_z + deck_thick + 0.35))
        for i in range(16)
    ]
    tower.tube(rail_pts, 0.04, 'strip', sides=4, closed=True)

    for sx in (-1.8, 1.8):
        tower.tube([(sx, 1.2, deck_z - 3.8), (sx * 0.8, deck_cy + 1.2, deck_z - 0.2)], 0.12, 'metal', sides=4)
    tower.tube([(0.0, 1.2, deck_z - 4.2), (0.0, deck_cy + 2.0, deck_z - 0.2)], 0.14, 'metal', sides=4)

    crown_z0 = 54.8
    for i in range(4):
        a = math.pi / 4.0 + i * math.pi / 2.0
        cos_a = math.cos(a)
        sin_a = math.sin(a)
        fin_path = [
            Vector((2.2 * cos_a, 2.2 * sin_a, crown_z0)),
            Vector((1.7 * cos_a, 1.7 * sin_a, crown_z0 + 3.2)),
            Vector((1.0 * cos_a, 1.0 * sin_a, crown_z0 + 6.0)),
            Vector((0.4 * cos_a, 0.4 * sin_a, crown_z0 + 8.2)),
        ]
        tower.tube(fin_path, 0.16, 'metal', sides=4)
        tower.tube(fin_path, 0.05, 'strip', sides=4)

    tower.tube([(0, 0, crown_z0), (0, 0, crown_z0 + 3.0)], 0.38, 'metal', sides=6)
    tower.tube([(0, 0, crown_z0 + 2.8), (0, 0, crown_z0 + 7.5)], 0.22, 'metal', sides=6)
    tower.tube([(0, 0, crown_z0 + 7.3), (0, 0, crown_z0 + 9.4)], 0.12, 'metal', sides=6)
    tower.tube([(0, 0, crown_z0 + 9.3), (0, 0, crown_z0 + 10.0)], 0.16, 'accent', sides=6)
    return tower


def build_bridge(name='bridge_a'):
    bridge = HeroPart(name)
    deck_len = 32.0

    deck_profile = [
        (-4.2, 5.92),
        (4.2, 5.92),
        (3.2, 4.8),
        (-3.2, 4.8),
    ]
    bridge.prism_x(deck_profile, -deck_len / 2.0, deck_len / 2.0, 'body')

    road_profile = [
        (-3.6, 5.96),
        (3.6, 5.96),
        (3.6, 6.04),
        (-3.6, 6.04),
    ]
    bridge.prism_x(road_profile, -deck_len / 2.0 + 0.06, deck_len / 2.0 - 0.06, 'floor')

    barrier_profile = [
        (-0.16, 6.03),
        (0.16, 6.03),
        (0.12, 6.45),
        (-0.12, 6.45),
    ]
    bridge.prism_x(barrier_profile, -deck_len / 2.0 + 0.12, deck_len / 2.0 - 0.12, 'top')

    for side_y in (-4.05, 4.05):
        bridge.rounded_box((0, side_y, 6.45), (deck_len - 0.08, 0.24, 0.72), 'metal', radius=0.03, segments=1)
        bridge.tube([(-deck_len / 2.0 + 0.1, side_y, 6.78), (deck_len / 2.0 - 0.1, side_y, 6.78)], 0.045, 'strip', sides=4)

    for pier_y in (-4.2, 4.2):
        bridge.rounded_box((-3.8, pier_y, 0.8), (2.4, 2.0, 1.6), 'body', radius=0.15, segments=1)

    pylon_left = [
        Vector((-3.8, -4.0, 1.5)),
        Vector((-3.5, -3.3, 5.8)),
        Vector((-3.0, -2.2, 10.5)),
        Vector((-2.2, -1.1, 15.0)),
        Vector((-1.4, 0.0, 18.5)),
    ]
    pylon_right = [
        Vector((-3.8, 4.0, 1.5)),
        Vector((-3.5, 3.3, 5.8)),
        Vector((-3.0, 2.2, 10.5)),
        Vector((-2.2, 1.1, 15.0)),
        Vector((-1.4, 0.0, 18.5)),
    ]
    pylon_upper = [
        Vector((-1.4, 0.0, 18.5)),
        Vector((-0.6, 0.0, 22.0)),
        Vector((0.3, 0.0, 25.4)),
        Vector((1.2, 0.0, 28.5)),
    ]

    bridge.tube(pylon_left, 0.44, 'metal', sides=6)
    bridge.tube(pylon_right, 0.44, 'metal', sides=6)
    bridge.tube(pylon_upper, 0.52, 'metal', sides=6)

    bridge.tube(pylon_left, 0.12, 'strip', sides=4)
    bridge.tube(pylon_right, 0.12, 'strip', sides=4)
    bridge.tube(pylon_upper, 0.14, 'strip', sides=4)

    bridge.rounded_box((1.3, 0.0, 28.7), (1.4, 1.2, 0.5), 'top', radius=0.08, segments=1)

    cables_count = 10
    for i in range(cables_count):
        t = i / (cables_count - 1)
        pyl_pt = Vector((-1.2 + 2.3 * t, 0.0, 19.2 + 8.8 * t))
        x_deck = -13.5 + 27.0 * t
        for side in (-1, 1):
            deck_pt = Vector((x_deck, side * 3.85, 6.25))
            bridge.tube([pyl_pt, deck_pt], 0.032, 'strip', sides=4)

    return bridge


def build_highrise_a(name='highrise_a'):
    highrise = HeroPart(name)

    t1_h = 15.5
    highrise.rounded_box((0, 0, t1_h / 2.0), (13.6, 11.6, t1_h), 'body', radius=0.15, segments=1)
    for x in (-5.4, -2.7, 0.0, 2.7, 5.4):
        for y_side in (-5.8, 5.8):
            pilaster_y(highrise, x, y_side, 0.1, t1_h - 0.2, 0.45, 0.16, 1 if y_side > 0 else -1, 'metal')
    for y in (-3.6, 0.0, 3.6):
        for x_side in (-6.8, 6.8):
            pilaster_x(highrise, x_side, y, 0.1, t1_h - 0.2, 0.45, 0.16, 1 if x_side > 0 else -1, 'metal')

    for floor in range(5):
        zf = 2.0 + floor * 2.6
        for y_side in (-5.82, 5.82):
            for x_bay in (-4.0, -1.35, 1.35, 4.0):
                highrise.oriented_poly(
                    [(x_bay - 0.75, y_side, zf), (x_bay + 0.75, y_side, zf),
                     (x_bay + 0.75, y_side, zf + 1.6), (x_bay - 0.75, y_side, zf + 1.6)],
                    (0, 1 if y_side > 0 else -1, 0),
                    'screen' if floor % 2 == 0 else 'wall'
                )

    highrise.rounded_box((0, 0, 15.65), (14.2, 12.2, 0.32), 'top', radius=0.06, segments=1)

    t2_h = 11.5
    t2_z0 = 15.75
    highrise.rounded_box((0, 0, t2_z0 + t2_h / 2.0), (10.6, 9.0, t2_h), 'body', radius=0.12, segments=1)
    for x in (-4.0, -1.35, 1.35, 4.0):
        for y_side in (-4.5, 4.5):
            pilaster_y(highrise, x, y_side, t2_z0 + 0.1, t2_z0 + t2_h - 0.2, 0.4, 0.15, 1 if y_side > 0 else -1, 'metal')
    for floor in range(4):
        zf = t2_z0 + 1.2 + floor * 2.5
        for y_side in (-4.52, 4.52):
            for x_bay in (-2.7, 0.0, 2.7):
                highrise.oriented_poly(
                    [(x_bay - 0.75, y_side, zf), (x_bay + 0.75, y_side, zf),
                     (x_bay + 0.75, y_side, zf + 1.5), (x_bay - 0.75, y_side, zf + 1.5)],
                    (0, 1 if y_side > 0 else -1, 0),
                    'screen'
                )

    highrise.rounded_box((0, 0, t2_z0 + t2_h + 0.1), (11.2, 9.6, 0.3), 'top', radius=0.05, segments=1)

    t3_h = 8.5
    t3_z0 = t2_z0 + t2_h + 0.2
    highrise.rounded_box((0, 0, t3_z0 + t3_h / 2.0), (7.8, 6.6, t3_h), 'body', radius=0.1, segments=1)
    for x in (-2.6, 0.0, 2.6):
        for y_side in (-3.3, 3.3):
            pilaster_y(highrise, x, y_side, t3_z0 + 0.1, t3_z0 + t3_h - 0.2, 0.36, 0.14, 1 if y_side > 0 else -1, 'metal')
    for floor in range(3):
        zf = t3_z0 + 1.0 + floor * 2.4
        for y_side in (-3.32, 3.32):
            for x_bay in (-1.3, 1.3):
                highrise.oriented_poly(
                    [(x_bay - 0.65, y_side, zf), (x_bay + 0.65, y_side, zf),
                     (x_bay + 0.65, y_side, zf + 1.4), (x_bay - 0.65, y_side, zf + 1.4)],
                    (0, 1 if y_side > 0 else -1, 0),
                    'screen'
                )

    highrise.rounded_box((0, 0, t3_z0 + t3_h + 0.1), (8.3, 7.1, 0.26), 'top', radius=0.04, segments=1)

    crown_z0 = t3_z0 + t3_h + 0.2
    crown_h = 4.2
    highrise.rounded_box((0, 0, crown_z0 + crown_h / 2.0), (5.2, 4.4, crown_h), 'metal', radius=0.08, segments=1)
    highrise.tube([(0, 0, crown_z0 + crown_h), (0, 0, crown_z0 + crown_h + 3.2)], 0.14, 'metal', sides=6)
    highrise.tube([(0, 0, crown_z0 + crown_h + 3.1), (0, 0, crown_z0 + crown_h + 3.6)], 0.18, 'accent', sides=6)
    highrise.tube([(-2.6, -2.2, crown_z0 + crown_h - 0.05), (2.6, -2.2, crown_z0 + crown_h - 0.05),
                   (2.6, 2.2, crown_z0 + crown_h - 0.05), (-2.6, 2.2, crown_z0 + crown_h - 0.05)],
                  0.05, 'strip', sides=4, closed=True)

    return highrise


def build_highrise_b(name='highrise_b'):
    highrise = HeroPart(name)
    base_h = 30.0

    hw = 5.8
    hd = 5.8
    ch = 1.8
    oct_pts = [
        (-hw + ch, -hd), (hw - ch, -hd),
        (hw, -hd + ch), (hw, hd - ch),
        (hw - ch, hd), (-hw + ch, hd),
        (-hw, hd - ch), (-hw, -hd + ch),
    ]

    rings = [
        [Vector((x, y, 0.0)) for x, y in oct_pts],
        [Vector((x, y, base_h)) for x, y in oct_pts],
    ]
    highrise.loft(rings, lambda r, c: 'body' if c % 2 == 0 else 'wall', levels=0, closed=True, cap=True, smooth=False)

    for i, (x, y) in enumerate(oct_pts):
        highrise.tube([(x, y, 0.1), (x, y, base_h - 0.1)], 0.18, 'metal', sides=4)

    for floor in range(9):
        zf = 2.2 + floor * 3.0
        for side_sign in (-1, 1):
            highrise.oriented_poly(
                [(-3.0, side_sign * (hd + FLOAT), zf), (3.0, side_sign * (hd + FLOAT), zf),
                 (3.0, side_sign * (hd + FLOAT), zf + 1.7), (-3.0, side_sign * (hd + FLOAT), zf + 1.7)],
                (0, side_sign, 0),
                'screen'
            )
            highrise.oriented_poly(
                [(side_sign * (hw + FLOAT), -3.0, zf), (side_sign * (hw + FLOAT), 3.0, zf),
                 (side_sign * (hw + FLOAT), 3.0, zf + 1.7), (side_sign * (hw + FLOAT), -3.0, zf + 1.7)],
                (side_sign, 0, 0),
                'screen'
            )

    highrise.rounded_box((0, 0, base_h + 0.12), (12.0, 12.0, 0.3), 'top', radius=0.06, segments=1)

    crown_z0 = base_h + 0.22
    crown_pts_low = [Vector((x * 0.94, y * 0.94, crown_z0)) for x, y in oct_pts]
    crown_pts_high = []
    for x, y in oct_pts:
        slope_z = crown_z0 + 2.5 + (y / hd) * 7.5
        crown_pts_high.append(Vector((x * 0.94, y * 0.94, slope_z)))

    highrise.loft([crown_pts_low, crown_pts_high], lambda r, c: 'screen' if (r, c) == (0, 3) or c in (2, 3, 4) else 'metal',
                  levels=0, closed=True, cap=True, smooth=False)

    rake_line = [
        Vector((-hw * 0.94 + ch, -hd * 0.94, crown_z0 + 2.5 - 7.5 * 0.94)),
        Vector((-hw * 0.94, -hd * 0.94 + ch, crown_z0 + 2.5 - 7.5 * 0.6)),
        Vector((-hw * 0.94, hd * 0.94 - ch, crown_z0 + 2.5 + 7.5 * 0.6)),
        Vector((-hw * 0.94 + ch, hd * 0.94, crown_z0 + 2.5 + 7.5 * 0.94)),
        Vector((hw * 0.94 - ch, hd * 0.94, crown_z0 + 2.5 + 7.5 * 0.94)),
        Vector((hw * 0.94, hd * 0.94 - ch, crown_z0 + 2.5 + 7.5 * 0.6)),
        Vector((hw * 0.94, -hd * 0.94 + ch, crown_z0 + 2.5 - 7.5 * 0.6)),
        Vector((hw * 0.94 - ch, -hd * 0.94, crown_z0 + 2.5 - 7.5 * 0.94)),
    ]
    highrise.tube(rake_line, 0.08, 'strip', sides=4, closed=True)

    return highrise


def build_highrise_c(name='highrise_c'):
    highrise = HeroPart(name)

    v1_h = 15.0
    highrise.rounded_box((0, 0, v1_h / 2.0), (12.0, 10.0, v1_h), 'body', radius=0.14, segments=1)
    for floor in range(4):
        zf = 1.8 + floor * 3.2
        for y_side in (-5.02, 5.02):
            for x_bay in (-3.4, 0.0, 3.4):
                highrise.oriented_poly(
                    [(x_bay - 1.1, y_side, zf), (x_bay + 1.1, y_side, zf),
                     (x_bay + 1.1, y_side, zf + 1.8), (x_bay - 1.1, y_side, zf + 1.8)],
                    (0, 1 if y_side > 0 else -1, 0),
                    'screen'
                )

    void_floor_z = v1_h + 0.12
    highrise.rounded_box((0, 0, void_floor_z), (12.4, 10.4, 0.3), 'top', radius=0.05, segments=1)

    for x_col in (-4.6, 4.6):
        for y_col in (-3.6, 3.6):
            highrise.tube([(x_col, y_col, void_floor_z + 0.1), (x_col, y_col, void_floor_z + 5.2)], 0.36, 'metal', sides=6)
    highrise.tube([(-4.6, -3.6, void_floor_z + 0.2), (4.6, 3.6, void_floor_z + 5.1)], 0.12, 'metal', sides=4)
    highrise.tube([(4.6, -3.6, void_floor_z + 0.2), (-4.6, 3.6, void_floor_z + 5.1)], 0.12, 'metal', sides=4)

    highrise.rounded_box((0, 0, void_floor_z + 0.38), (6.8, 5.0, 0.46), 'soft', radius=0.08, segments=1)
    highrise.tube([(-5.6, -4.6, void_floor_z + 5.1), (5.6, -4.6, void_floor_z + 5.1),
                   (5.6, 4.6, void_floor_z + 5.1), (-5.6, 4.6, void_floor_z + 5.1)],
                  0.06, 'accent', sides=4, closed=True)

    v2_z0 = void_floor_z + 5.3
    v2_h = 14.0
    highrise.rounded_box((0, 0, v2_z0 + v2_h / 2.0), (12.0, 10.0, v2_h), 'body', radius=0.14, segments=1)
    for floor in range(4):
        zf = v2_z0 + 1.6 + floor * 3.1
        for y_side in (-5.02, 5.02):
            for x_bay in (-3.4, 0.0, 3.4):
                highrise.oriented_poly(
                    [(x_bay - 1.1, y_side, zf), (x_bay + 1.1, y_side, zf),
                     (x_bay + 1.1, y_side, zf + 1.8), (x_bay - 1.1, y_side, zf + 1.8)],
                    (0, 1 if y_side > 0 else -1, 0),
                    'screen'
                )

    roof_z = v2_z0 + v2_h + 0.12
    highrise.rounded_box((0, 0, roof_z), (12.4, 10.4, 0.3), 'top', radius=0.05, segments=1)

    trellis_z = roof_z + 0.28
    for x in (-4.2, -1.4, 1.4, 4.2):
        highrise.tube([(x, -4.4, trellis_z), (x, 4.4, trellis_z)], 0.09, 'metal', sides=4)
        highrise.tube([(x, -4.4, roof_z), (x, -4.4, trellis_z)], 0.08, 'metal', sides=4)
        highrise.tube([(x, 4.4, roof_z), (x, 4.4, trellis_z)], 0.08, 'metal', sides=4)
    for y in (-3.4, 0.0, 3.4):
        highrise.tube([(-5.0, y, trellis_z + 0.14), (5.0, y, trellis_z + 0.14)], 0.07, 'top', sides=4)

    return highrise

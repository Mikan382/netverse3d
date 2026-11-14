import math

from mathutils import Vector

from hero_kit import HeroPart

FLOAT = 0.008


def window_band(part, cx, cy, z0, z1, width, depth, axis, lit_pattern):
    half_w = width / 2
    half_d = depth / 2
    if axis == 'y_pos':
        y = cy + half_d + FLOAT
        count = len(lit_pattern)
        dx = (width - 0.2) / count
        for i, is_lit in enumerate(lit_pattern):
            x0 = cx - half_w + 0.1 + i * dx + 0.04
            x1 = x0 + dx - 0.08
            row = 'screen' if is_lit else 'wall'
            part.oriented_poly([(x0, y, z0), (x1, y, z0), (x1, y, z1), (x0, y, z1)], (0, 1, 0), row)
    elif axis == 'y_neg':
        y = cy - half_d - FLOAT
        count = len(lit_pattern)
        dx = (width - 0.2) / count
        for i, is_lit in enumerate(lit_pattern):
            x0 = cx - half_w + 0.1 + i * dx + 0.04
            x1 = x0 + dx - 0.08
            row = 'screen' if is_lit else 'wall'
            part.oriented_poly([(x0, y, z0), (x1, y, z0), (x1, y, z1), (x0, y, z1)], (0, -1, 0), row)
    elif axis == 'x_pos':
        x = cx + half_w + FLOAT
        count = len(lit_pattern)
        dy = (depth - 0.2) / count
        for i, is_lit in enumerate(lit_pattern):
            y0 = cy - half_d + 0.1 + i * dy + 0.04
            y1 = y0 + dy - 0.08
            row = 'screen' if is_lit else 'wall'
            part.oriented_poly([(x, y0, z0), (x, y1, z0), (x, y1, z1), (x, y0, z1)], (1, 0, 0), row)
    elif axis == 'x_neg':
        x = cx - half_w - FLOAT
        count = len(lit_pattern)
        dy = (depth - 0.2) / count
        for i, is_lit in enumerate(lit_pattern):
            y0 = cy - half_d + 0.1 + i * dy + 0.04
            y1 = y0 + dy - 0.08
            row = 'screen' if is_lit else 'wall'
            part.oriented_poly([(x, y0, z0), (x, y1, z0), (x, y1, z1), (x, y0, z1)], (-1, 0, 0), row)


def build_tower(name='tower_a'):
    tower = HeroPart(name)
    tower.rounded_box((0, 0, 6.0), (14.0, 14.0, 12.0), 'body', radius=0.2, segments=1)
    for x in (-6.8, 6.8):
        for y in (-6.8, 6.8):
            tower.rounded_box((x, y, 5.95), (0.8, 0.8, 11.6), 'metal', radius=0.08, segments=1)
    tower.rounded_box((0, 0, 12.1), (14.4, 14.4, 0.36), 'top', radius=0.05, segments=1)

    patterns = [
        [1, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0, 1],
    ]

    shaft_z0 = 12.18
    shaft_height = 16.0
    tower.rounded_box((0, 0, shaft_z0 + shaft_height / 2), (11.6, 11.6, shaft_height), 'wall', radius=0.15, segments=1)
    for floor in range(5):
        z0 = shaft_z0 + 0.7 + floor * 3.0
        z1 = z0 + 1.8
        pattern = patterns[floor % len(patterns)]
        for axis in ('y_pos', 'y_neg', 'x_pos', 'x_neg'):
            window_band(tower, 0, 0, z0, z1, 11.4, 11.4, axis, pattern)
    ledge2_z = shaft_z0 + shaft_height + 0.08
    tower.rounded_box((0, 0, ledge2_z), (12.0, 12.0, 0.36), 'top', radius=0.05, segments=1)

    upper_z0 = ledge2_z + 0.08
    upper_height = 16.0
    tower.rounded_box((0, 0, upper_z0 + upper_height / 2), (9.0, 9.0, upper_height), 'wall', radius=0.12, segments=1)
    for floor in range(5):
        z0 = upper_z0 + 0.7 + floor * 3.0
        z1 = z0 + 1.8
        pattern = patterns[(floor + 2) % len(patterns)][:5]
        for axis in ('y_pos', 'y_neg', 'x_pos', 'x_neg'):
            window_band(tower, 0, 0, z0, z1, 8.8, 8.8, axis, pattern)
    ledge3_z = upper_z0 + upper_height + 0.08
    tower.rounded_box((0, 0, ledge3_z), (9.4, 9.4, 0.36), 'top', radius=0.04, segments=1)

    for x in (-4.4, 4.4):
        for y in (-4.4, 4.4):
            tower.tube([(x, y, 12.35), (x, y, upper_z0 + upper_height - 0.1)], 0.08, 'strip', sides=4)

    neck_z0 = ledge3_z + 0.08
    neck_height = 8.0
    tower.rounded_box((0, 0, neck_z0 + neck_height / 2), (6.6, 6.6, neck_height), 'body', radius=0.1, segments=1)
    for floor in range(2):
        z0 = neck_z0 + 0.9 + floor * 3.4
        z1 = z0 + 2.0
        pattern = [1, 0, 1, 0]
        for axis in ('y_pos', 'y_neg', 'x_pos', 'x_neg'):
            window_band(tower, 0, 0, z0, z1, 6.4, 6.4, axis, pattern)
    ledge4_z = neck_z0 + neck_height + 0.08
    tower.rounded_box((0, 0, ledge4_z), (7.0, 7.0, 0.36), 'top', radius=0.04, segments=1)

    crown_z0 = ledge4_z + 0.18
    fin_height = 9.5
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        p0 = (sx * 3.2, sy * 3.2, crown_z0)
        p1 = (sx * 3.2, sy * 1.8, crown_z0)
        p2 = (sx * 2.0, sy * 1.0, crown_z0 + fin_height)
        p3 = (sx * 2.8, sy * 2.8, crown_z0 + fin_height * 0.9)
        tower.poly([p0, p1, p2, p3], 'metal')
        q0 = (sx * 3.2, sy * 3.2, crown_z0)
        q1 = (sx * 1.8, sy * 3.2, crown_z0)
        q2 = (sx * 1.0, sy * 2.0, crown_z0 + fin_height)
        q3 = (sx * 2.8, sy * 2.8, crown_z0 + fin_height * 0.9)
        tower.poly([q0, q1, q2, q3], 'metal')
        tower.tube([(sx * 3.2, sy * 3.2, crown_z0), (sx * 2.0, sy * 2.0, crown_z0 + fin_height)], 0.05, 'strip', sides=4)

    tower.rounded_box((0, 0, crown_z0 + 1.95), (3.6, 3.6, 4.0), 'metal', radius=0.06, segments=1)
    tower.tube([(0, 0, crown_z0 + 3.9), (0, 0, crown_z0 + 11.5)], 0.12, 'metal', sides=6)
    tower.tube([(0, 0, crown_z0 + 11.5), (0, 0, crown_z0 + 12.0)], 0.16, 'accent', sides=6)
    return tower


def build_bridge(name='bridge_a'):
    bridge = HeroPart(name)
    deck_length = 32.0
    deck_width = 8.4
    deck_z = 6.0
    deck_thick = 1.0
    bridge.rounded_box((0, 0, deck_z - deck_thick / 2), (deck_length, deck_width, deck_thick), 'body', radius=0.08, segments=1)
    bridge.rounded_box((0, 0, deck_z + 0.03), (deck_length, deck_width - 1.2, 0.06), 'wall', radius=0.02, segments=1)
    for y in (-deck_width / 2 + 0.15, deck_width / 2 - 0.15):
        bridge.rounded_box((0, y, deck_z + 0.42), (deck_length, 0.26, 0.8), 'top', radius=0.04, segments=1)

    pylon_x = -3.5
    pylon_top_z = 28.5
    for sign_y in (-1, 1):
        leg = [
            Vector((pylon_x + 0.8, sign_y * 4.6, 0.2)),
            Vector((pylon_x + 0.3, sign_y * 3.2, deck_z + 0.5)),
            Vector((pylon_x - 0.8, sign_y * 1.4, 20.0)),
            Vector((pylon_x - 1.4, sign_y * 0.4, pylon_top_z)),
        ]
        bridge.tube(leg, 0.48, 'metal', sides=6)
        bridge.tube(leg, 0.52, 'strip', sides=3)

    bridge.rounded_box((pylon_x - 1.4, 0, pylon_top_z + 0.32), (1.6, 2.2, 0.9), 'metal', radius=0.06, segments=1)
    bridge.rounded_box((pylon_x - 1.4, 0, pylon_top_z + 0.92), (0.4, 0.4, 0.4), 'accent', radius=0.02, segments=1)

    cable_anchor_z = [21.5, 23.5, 25.5, 27.2]
    cable_deck_x = [-14.5, -10.5, -6.8, -0.5, 3.5, 7.5, 11.5, 14.5]
    for i, anchor_z in enumerate(cable_anchor_z):
        pylon_pt_neg = Vector((pylon_x - 0.9 - i * 0.15, -0.6, anchor_z))
        pylon_pt_pos = Vector((pylon_x - 0.9 - i * 0.15, 0.6, anchor_z))
        back_x = cable_deck_x[i]
        bridge.tube([pylon_pt_neg, Vector((back_x, -3.9, deck_z + 0.4))], 0.032, 'metal', sides=4)
        bridge.tube([pylon_pt_pos, Vector((back_x, 3.9, deck_z + 0.4))], 0.032, 'metal', sides=4)
        front_x = cable_deck_x[len(cable_deck_x) - 1 - i]
        bridge.tube([pylon_pt_neg, Vector((front_x, -3.9, deck_z + 0.4))], 0.032, 'metal', sides=4)
        bridge.tube([pylon_pt_pos, Vector((front_x, 3.9, deck_z + 0.4))], 0.032, 'metal', sides=4)

    for pier_x in (-12.0, 8.0):
        bridge.rounded_box((pier_x, 0, deck_z / 2 - 0.45), (2.2, 5.0, deck_z - 0.9), 'body', radius=0.1, segments=1)
    return bridge


def build_highrise_a(name='highrise_a'):
    building = HeroPart(name)
    tier1_h = 16.0
    building.rounded_box((0, 0, tier1_h / 2), (14.0, 14.0, tier1_h), 'wall', radius=0.15, segments=1)
    building.rounded_box((0, 0, tier1_h + 0.12), (14.3, 14.3, 0.36), 'top', radius=0.04, segments=1)

    patterns = [
        [1, 0, 1, 0, 1, 0, 0, 1],
        [0, 1, 0, 0, 1, 0, 1, 0],
        [1, 0, 0, 1, 0, 1, 0, 1],
        [0, 1, 1, 0, 0, 1, 0, 0],
    ]
    for floor in range(5):
        z0 = 1.0 + floor * 2.9
        z1 = z0 + 1.8
        pattern = patterns[floor % len(patterns)]
        for axis in ('y_pos', 'y_neg', 'x_pos', 'x_neg'):
            window_band(building, 0, 0, z0, z1, 13.8, 13.8, axis, pattern)

    tier2_h = 14.0
    tier2_z0 = tier1_h + 0.22
    building.rounded_box((0, 0, tier2_z0 + tier2_h / 2), (11.0, 11.0, tier2_h), 'wall', radius=0.12, segments=1)
    building.rounded_box((0, 0, tier2_z0 + tier2_h + 0.12), (11.3, 11.3, 0.36), 'top', radius=0.04, segments=1)
    for floor in range(4):
        z0 = tier2_z0 + 0.8 + floor * 3.1
        z1 = z0 + 1.8
        pattern = patterns[(floor + 1) % len(patterns)][:6]
        for axis in ('y_pos', 'y_neg', 'x_pos', 'x_neg'):
            window_band(building, 0, 0, z0, z1, 10.8, 10.8, axis, pattern)

    tier3_h = 10.0
    tier3_z0 = tier2_z0 + tier2_h + 0.22
    building.rounded_box((0, 0, tier3_z0 + tier3_h / 2), (8.0, 8.0, tier3_h), 'wall', radius=0.1, segments=1)
    building.rounded_box((0, 0, tier3_z0 + tier3_h + 0.12), (8.3, 8.3, 0.36), 'top', radius=0.04, segments=1)
    for floor in range(3):
        z0 = tier3_z0 + 0.8 + floor * 2.9
        z1 = z0 + 1.7
        pattern = patterns[(floor + 2) % len(patterns)][:4]
        for axis in ('y_pos', 'y_neg', 'x_pos', 'x_neg'):
            window_band(building, 0, 0, z0, z1, 7.8, 7.8, axis, pattern)

    roof_z0 = tier3_z0 + tier3_h + 0.18
    building.rounded_box((0, 0, roof_z0 + 1.45), (4.8, 4.8, 3.0), 'body', radius=0.08, segments=1)
    building.tube([(0, 0, roof_z0 + 2.9), (0, 0, roof_z0 + 4.8)], 0.08, 'metal', sides=4)
    building.rounded_box((0, 0, roof_z0 + 4.9), (0.24, 0.24, 0.24), 'accent', radius=0.02, segments=1)
    return building


def build_highrise_b(name='highrise_b'):
    building = HeroPart(name)
    height = 42.0
    hw = 6.4
    hd = 6.4
    chamfer = 2.2
    rings = []
    levels = [0.0, 2.0, 14.0, 26.0, 38.0, height]
    for z in levels:
        profile = [
            Vector((-hw + chamfer, -hd, z)),
            Vector((hw - chamfer, -hd, z)),
            Vector((hw, -hd + chamfer, z)),
            Vector((hw, hd - chamfer, z)),
            Vector((hw - chamfer, hd, z)),
            Vector((-hw + chamfer, hd, z)),
            Vector((-hw, hd - chamfer, z)),
            Vector((-hw, -hd + chamfer, z)),
        ]
        rings.append(profile)
    building.loft(rings, lambda r, c: 'wall', levels=0, closed=True, cap=True, smooth=False)

    patterns = [
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
        [1, 1, 0, 0, 1],
    ]
    for floor in range(12):
        z0 = 2.5 + floor * 3.1
        z1 = z0 + 1.8
        pattern = patterns[floor % len(patterns)]
        for axis in ('y_pos', 'y_neg', 'x_pos', 'x_neg'):
            window_band(building, 0, 0, z0, z1, hw * 2 - chamfer * 2, hd * 2 - chamfer * 2, axis, pattern)

    for angle in (45, 135, 225, 315):
        rad = math.radians(angle)
        x = math.cos(rad) * (hw - chamfer * 0.5)
        y = math.sin(rad) * (hd - chamfer * 0.5)
        building.tube([(x, y, 1.0), (x, y, height - 0.2)], 0.08, 'strip', sides=4)

    roof_z = height + 0.12
    building.rounded_box((0, 0, roof_z + 1.55), (6.0, 6.0, 3.2), 'metal', radius=0.08, segments=1)
    building.tube([(0, 0, roof_z + 3.1), (0, 0, roof_z + 6.0)], 0.09, 'metal', sides=6)
    building.rounded_box((0, 0, roof_z + 6.1), (0.22, 0.22, 0.22), 'accent', radius=0.02, segments=1)
    return building


def build_highrise_c(name='highrise_c'):
    building = HeroPart(name)
    tower_w = 5.6
    tower_d = 10.4
    tower_h = 36.0
    gap = 4.0
    x_centers = (-(tower_w + gap) / 2, (tower_w + gap) / 2)

    patterns = [
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 0, 1],
    ]
    patterns_d = [
        [1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1],
        [1, 1, 0, 0, 1, 0],
    ]

    for xc in x_centers:
        building.rounded_box((xc, 0, tower_h / 2), (tower_w, tower_d, tower_h), 'wall', radius=0.12, segments=1)
        building.rounded_box((xc, 0, tower_h + 0.12), (tower_w + 0.3, tower_d + 0.3, 0.36), 'top', radius=0.04, segments=1)
        for floor in range(10):
            z0 = 1.8 + floor * 3.3
            z1 = z0 + 1.9
            pat_w = patterns[floor % len(patterns)]
            pat_d = patterns_d[floor % len(patterns_d)]
            window_band(building, xc, 0, z0, z1, tower_w, tower_d, 'y_pos', pat_w)
            window_band(building, xc, 0, z0, z1, tower_w, tower_d, 'y_neg', pat_w)
            window_band(building, xc, 0, z0, z1, tower_w, tower_d, 'x_pos', pat_d)
            window_band(building, xc, 0, z0, z1, tower_w, tower_d, 'x_neg', pat_d)

    bridge_z0 = 23.0
    bridge_h = 3.6
    bridge_w = gap + 0.8
    bridge_d = 4.8
    building.rounded_box((0, 0, bridge_z0 + bridge_h / 2), (bridge_w, bridge_d, bridge_h), 'metal', radius=0.08, segments=1)
    for y_sign in (-1, 1):
        y = y_sign * (bridge_d / 2 + FLOAT)
        norm = (0, y_sign, 0)
        building.oriented_poly([(-bridge_w / 2 + 0.2, y, bridge_z0 + 0.6), (bridge_w / 2 - 0.2, y, bridge_z0 + 0.6), (bridge_w / 2 - 0.2, y, bridge_z0 + bridge_h - 0.6), (-bridge_w / 2 + 0.2, y, bridge_z0 + bridge_h - 0.6)], norm, 'screen')

    for xc in x_centers:
        building.rounded_box((xc, 0, tower_h + 1.15), (3.2, 3.2, 2.0), 'body', radius=0.06, segments=1)
    building.tube([(x_centers[0], 0, tower_h + 2.1), (x_centers[0], 0, tower_h + 4.5)], 0.08, 'metal', sides=4)
    building.rounded_box((x_centers[0], 0, tower_h + 4.6), (0.2, 0.2, 0.2), 'accent', radius=0.02, segments=1)
    return building

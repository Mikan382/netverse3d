import math

from hero_kit import HeroPart, rounded_rect

TEXT_HALF_WIDTH = 0.6
TEXT_HALF_HEIGHT = 0.15
BLADE_TEXT_HALF_LENGTH = 0.52
BLADE_TEXT_HALF_WIDTH = 0.13


def ring_xz(half_width, half_height, radius, y):
    return [(x, y, z) for x, z in rounded_rect(0, 0, half_width, half_height, radius, 3)]


def ring_xz_at(cx, cz, half_width, half_height, radius, y):
    return [(x, y, z) for x, z in rounded_rect(cx, cz, half_width, half_height, radius, 3)]


def circle_xz(cx, cz, radius, y, steps=14, start=0.0, sweep=2 * math.pi):
    return [(cx + radius * math.cos(start + sweep * i / steps), y, cz + radius * math.sin(start + sweep * i / steps)) for i in range(steps + 1)]


def text_panel(part, y):
    part.image_rect([
        (TEXT_HALF_WIDTH, y, -TEXT_HALF_HEIGHT),
        (-TEXT_HALF_WIDTH, y, -TEXT_HALF_HEIGHT),
        (-TEXT_HALF_WIDTH, y, TEXT_HALF_HEIGHT),
        (TEXT_HALF_WIDTH, y, TEXT_HALF_HEIGHT),
    ], 'decal', (0.0, 0.0, 1.0, 1.0))


def power_icon(part, cx, y, radius, row):
    part.tube(circle_xz(cx, 0, radius, y, steps=12, start=math.radians(120), sweep=math.radians(300)), 0.006, row, sides=4)
    part.tube([(cx, y, radius * 0.25), (cx, y, radius * 1.25)], 0.006, row, sides=4)


def build_sign_neon(name='sign_a'):
    sign = HeroPart(name)
    sign.slab_y(0, 0, 0.95, 0.26, 0.05, [
        (0.0, 0.014, 'body'),
        (0.014, 0.0, 'body'),
        (0.095, 0.0, 'body'),
        (0.11, 0.014, 'top'),
        (0.112, 0.034, 'top'),
    ])
    sign.rounded_box((0, 0.115, 0), (1.78, 0.006, 0.4), 'soft', radius=0.002, segments=1)
    text_panel(sign, 0.121)
    sign.tube(ring_xz(0.905, 0.215, 0.04, 0.124), 0.009, 'strip', sides=5, closed=True)
    sign.tube(ring_xz(0.855, 0.172, 0.022, 0.124), 0.005, 'screen', sides=4, closed=True)
    for side in (-1, 1):
        power_icon(sign, side * 0.735, 0.124, 0.062, 'accent')
        sign.rounded_box((side * 0.965, 0.055, 0), (0.03, 0.11, 0.4), 'metal', radius=0.008, segments=1)
    return sign


def build_sign_matrix(name='sign_b'):
    sign = HeroPart(name)
    sign.slab_y(0, 0, 0.93, 0.23, 0.012, [
        (0.0, 0.004, 'metal'),
        (0.006, 0.0, 'metal'),
        (0.062, 0.0, 'metal'),
        (0.07, 0.012, 'body'),
        (0.071, 0.03, 'body'),
    ])
    sign.rounded_box((0, 0.074, 0.02), (1.76, 0.006, 0.34), 'soft', radius=0.002, segments=1)
    text_panel(sign, 0.08)
    for z in (0.2, -0.165):
        sign.tube([(-0.87, 0.079, z), (0.87, 0.079, z)], 0.004, 'strip', sides=4)
    for i in range(14):
        x = -0.845 + i * 0.13
        row = 'accent' if i % 3 == 0 else 'screen'
        sign.rounded_box((x, 0.076, -0.197), (0.07, 0.006, 0.022), row, radius=0.002, segments=1)
    for side in (-1, 1):
        sign.rounded_box((side * 0.8, 0.085, 0.3), (0.05, 0.03, 0.14), 'metal', radius=0.006, segments=1)
        sign.tube([(side * 0.8, 0.0, 0.36), (side * 0.8, 0.085, 0.36)], 0.012, 'metal', sides=4)
    return sign


def build_sign_painted(name='sign_c'):
    sign = HeroPart(name)
    for z in (0.156, 0.0, -0.156):
        sign.rounded_box((0, 0.024, z), (1.84, 0.048, 0.148), 'top', radius=0.008, segments=1)
    for x in (-0.8, 0.8):
        sign.rounded_box((x, 0.052, 0), (0.05, 0.008, 0.46), 'metal', radius=0.003, segments=1)
        for z in (0.156, -0.156):
            sign.revolve((x, 0.056, z), 'y', [(0.011, 0.0, 'metal'), (0.011, 0.004, 'metal'), (0.001, 0.004, 'metal')], segments=8, smooth=False)
    text_panel(sign, 0.051)
    for x in (-0.45, 0.45):
        sign.tube([(x, 0.02, 0.23), (x, 0.03, 0.34), (x, 0.13, 0.39), (x, 0.2, 0.345)], 0.008, 'metal', sides=5)
        sign.revolve((x, 0.2, 0.3), 'z', [(0.001, 0.05, 'body'), (0.03, 0.05, 'body'), (0.062, 0.0, 'body'), (0.05, 0.0, 'strip'), (0.001, 0.012, 'strip')], segments=12)
    return sign


def blade_text(part, x, facing):
    near, far = 0.42 - BLADE_TEXT_HALF_WIDTH, 0.42 + BLADE_TEXT_HALF_WIDTH
    left, right = (near, far) if facing > 0 else (far, near)
    part.image_rect([
        (x, left, BLADE_TEXT_HALF_LENGTH),
        (x, left, -BLADE_TEXT_HALF_LENGTH),
        (x, right, -BLADE_TEXT_HALF_LENGTH),
        (x, right, BLADE_TEXT_HALF_LENGTH),
    ], 'decal', (0.0, 0.0, 1.0, 1.0))


def build_blade(name='blade_a'):
    blade = HeroPart(name)
    blade.rounded_box((0, 0.42, 0), (0.1, 0.46, 1.3), 'body', radius=0.02, segments=1)
    for facing in (1, -1):
        x = facing * 0.052
        blade.rounded_box((facing * 0.0515, 0.42, 0), (0.004, 0.36, 1.18), 'soft', radius=0.001, segments=1)
        blade_text(blade, facing * 0.0565, facing)
        ring = [(facing * 0.058, 0.42 + y, z) for y, z in rounded_rect(0, 0, 0.2, 0.615, 0.03, 3)]
        blade.tube(ring if facing > 0 else ring[::-1], 0.007, 'strip', sides=4, closed=True)
        stud = [(0.02, 0.0, 'accent'), (0.02, 0.008, 'accent'), (0.001, 0.008, 'accent')]
        if facing > 0:
            blade.revolve((x, 0.42, 0.59), 'x', stud, segments=10, smooth=False)
        else:
            blade.revolve((x - 0.008, 0.42, 0.59), 'x', [(radius, 0.008 - along, row) for radius, along, row in reversed(stud)], segments=10, smooth=False)
    blade.rounded_box((0, 0.012, 0), (0.16, 0.024, 1.08), 'metal', radius=0.006, segments=1)
    for z in (0.44, -0.44):
        blade.tube([(0, 0.02, z), (0, 0.2, z)], 0.016, 'metal', sides=5)
    return blade


def build_tower_sign(name='tower_a'):
    sign = HeroPart(name)
    for z in (-2.4, -0.8, 0.8, 2.4):
        sign.rounded_box((0, 0.015, z), (0.68, 0.03, 0.12), 'metal', radius=0.01, segments=1)
        for x in (-0.24, 0.24):
            sign.tube([(x, 0.03, z), (x, 0.12, z)], 0.024, 'metal', sides=6)

    sign.rounded_box((0, 0.24, 0), (0.84, 0.24, 5.5), 'metal', radius=0.03, segments=1)
    sign.rounded_box((0, 0.24, 2.77), (0.88, 0.26, 0.06), 'top', radius=0.02, segments=1)
    sign.rounded_box((0, 0.24, -2.77), (0.88, 0.26, 0.06), 'top', radius=0.02, segments=1)

    sign.rounded_box((0, 0.362, 0), (0.74, 0.008, 5.3), 'body', radius=0.01, segments=1)

    sign.image_rect([
        (0.32, 0.369, -2.4),
        (-0.32, 0.369, -2.4),
        (-0.32, 0.369, 2.4),
        (0.32, 0.369, 2.4),
    ], 'decal', (0.0, 0.0, 1.0, 1.0))

    sign.tube(ring_xz(0.355, 2.58, 0.035, 0.376), 0.008, 'strip', sides=5, closed=True)
    sign.tube(ring_xz(0.325, 2.42, 0.025, 0.376), 0.005, 'accent', sides=4, closed=True)

    for side_x in (-0.37, 0.37):
        for z in (-2.4, -0.8, 0.8, 2.4):
            sign.rounded_box((side_x, 0.368, z), (0.04, 0.015, 0.14), 'metal', radius=0.004, segments=1)

    return sign


def build_rooftop_sign(name='rooftop_a'):
    sign = HeroPart(name)

    for x in (-1.2, 1.2):
        sign.rounded_box((x, -0.36, 0.04), (0.16, 0.8, 0.08), 'metal', radius=0.01, segments=1)
        sign.tube([(x, 0.0, 0.08), (x, 0.0, 1.82)], 0.035, 'metal', sides=4)
        sign.tube([(x, -0.72, 0.08), (x, 0.0, 1.78)], 0.032, 'metal', sides=4)
        sign.tube([(x, -0.36, 0.92), (x, 0.0, 0.92)], 0.024, 'metal', sides=4)

    sign.tube([(-1.2, -0.36, 0.2), (1.2, -0.36, 1.5)], 0.018, 'metal', sides=4)
    sign.tube([(1.2, -0.36, 0.2), (-1.2, -0.36, 1.5)], 0.018, 'metal', sides=4)

    sign.rounded_box((0, 0.1, 1.15), (3.4, 0.18, 1.35), 'metal', radius=0.025, segments=1)
    sign.rounded_box((0, 0.194, 1.15), (3.44, 0.02, 1.39), 'top', radius=0.015, segments=1)
    sign.rounded_box((0, 0.202, 1.15), (3.24, 0.008, 1.19), 'body', radius=0.01, segments=1)

    sign.image_rect([
        (1.5, 0.208, 0.65),
        (-1.5, 0.208, 0.65),
        (-1.5, 0.208, 1.65),
        (1.5, 0.208, 1.65),
    ], 'decal', (0.0, 0.0, 1.0, 1.0))

    sign.tube(ring_xz_at(0, 1.15, 1.58, 0.56, 0.04, 0.216), 0.01, 'strip', sides=5, closed=True)
    sign.tube(ring_xz_at(0, 1.15, 1.51, 0.50, 0.025, 0.216), 0.006, 'accent', sides=4, closed=True)

    for x in (-1.2, -0.4, 0.4, 1.2):
        lamp_path = [
            (x, 0.08, 1.83),
            (x, 0.18, 1.94),
            (x, 0.32, 1.94),
            (x, 0.32, 1.88),
        ]
        sign.tube(lamp_path, 0.012, 'metal', sides=5)
        sign.revolve((x, 0.32, 1.86), 'z', [
            (0.001, 0.04, 'body'),
            (0.035, 0.04, 'body'),
            (0.065, 0.0, 'body'),
            (0.055, 0.0, 'strip'),
            (0.001, 0.015, 'strip'),
        ], segments=12)

    return sign

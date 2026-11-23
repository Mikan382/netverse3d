from hero_kit import HeroPart
from hero_solid import rbox
from hero_vegetation import build_woody_tree


def build_street_tree(variant):
    part = HeroPart(f'tree_{variant}')
    if variant == 'a':
        build_woody_tree(part, 6.5, 1.19, 21, branch_start=0.38)
    else:
        build_woody_tree(part, 3.5, 0.67, 79, branch_count=4)
    return part


def build_tree_pit():
    part = HeroPart('pit_a')
    for x in (-0.44, 0.44):
        rbox(part, (x, 0, 0.075), (0.12, 1, 0.15), 'wall', radius=0.015)
    for y in (-0.44, 0.44):
        rbox(part, (0, y, 0.075), (0.756, 0.12, 0.15), 'wall', radius=0.014)
    rbox(part, (0, 0, 0.057), (0.74, 0.74, 0.105), 'body')
    for x in (-0.315, -0.245, 0.245, 0.315):
        rbox(part, (x, 0, 0.133), (0.024, 0.745, 0.025), 'metal')
    for x in (-0.09, 0.09):
        for y in (-0.291, 0.291):
            rbox(part, (x, y, 0.131), (0.021, 0.16, 0.025), 'metal')
    return part


def build_alley_parts():
    return (build_street_tree('a'), build_street_tree('b'), build_tree_pit(),
            build_vacant_plot(), build_fence(), build_notice(),
            build_crates(), build_gas_cylinder(), build_corner_mirror())


def build_vacant_plot():
    part = HeroPart('plot_a')
    rbox(part, (0, 0, 0.057), (4, 4, 0.114), 'body')
    for x in (-1, 1):
        for y in (-1, 1):
            rbox(part, (x, y, 0.131), (1.84, 1.84, 0.038),
                 'wall' if x == y else 'floor', radius=0.008)
    for x, y, dx, dy in ((-1.68, 0.01, 0.53, 0.119), (0.01, 1.51, 0.12, 0.78),
                        (1.46, -0.01, 0.77, 0.12), (-0.01, -1.48, 0.12, 0.79)):
        rbox(part, (x, y, 0.119), (dx, dy, 0.035), 'grass', radius=0.007)
    return part


def build_fence():
    part = HeroPart('fence_a')
    for x in (-1.92, 0, 1.92):
        rbox(part, (x, 0, 0.067), (0.15, 0.22, 0.134), 'wall')
        rbox(part, (x, 0, 1.017), (0.074, 0.09, 1.974), 'metal', radius=0.008)
    for z in (0.15, 1.93):
        rbox(part, (0, 0, z), (4, 0.075, 0.086), 'metal', radius=0.006)
    for x in (-0.96, 0.96):
        rbox(part, (x, 0.001, 1.043), (1.83, 0.038, 1.622), 'wall', radius=0.008)
        for dx in (-0.67, -0.33, 0.001, 0.33, 0.67):
            rbox(part, (x + dx, -0.023, 1.045), (0.024, 0.024, 1.59), 'metal')
    return part


def build_notice():
    part = HeroPart('notice_a')
    for x in (-0.63, 0.63):
        rbox(part, (x, 0, 0.045), (0.19, 0.26, 0.09), 'wall', radius=0.014)
        rbox(part, (x, 0, 0.91), (0.072, 0.087, 1.73), 'metal', radius=0.009)
    rbox(part, (0, 0.012, 1.753), (1.79, 0.177, 0.56), 'metal', radius=0.026, segments=2)
    rbox(part, (0, -0.080, 1.753), (1.65, 0.06, 0.463), 'soft', radius=0.015)
    for x in (-0.833, 0.833):
        part.tube([(x, -0.116, 1.55), (x, -0.116, 1.956)], 0.012, 'accent', sides=8)
    for z in (1.522, 1.985):
        part.tube([(-0.806, -0.118, z), (0.806, -0.118, z)], 0.012, 'accent', sides=8)
    part.image_rect([(-0.8, -0.114, 1.553), (0.8, -0.114, 1.553),
                     (0.8, -0.114, 1.953), (-0.8, -0.114, 1.953)], 'decal', (0, 0, 1, 1))
    return part


def build_crates():
    part = HeroPart('crate_a')
    for index, (x, y, color) in enumerate(((0, 0, 'top'), (-0.014, 0.011, 'wall'), (0.02, -0.008, 'top'))):
        z = index * 0.3
        rbox(part, (x, y, z + 0.025), (0.48, 0.37, 0.05), color, radius=0.012)
        for dx in (-0.216, 0.216):
            for dy in (-0.159, 0.159):
                rbox(part, (x + dx, y + dy, z + 0.145), (0.039, 0.039, 0.208), color)
        for dy in (-0.167, 0.167):
            rbox(part, (x, y + dy, z + 0.269), (0.48, 0.044, 0.058), color)
        for dx in (-0.208, 0.208):
            rbox(part, (x + dx, y, z + 0.27), (0.047, 0.303, 0.051), 'metal')
        for dx in (-0.12, 0.12):
            rbox(part, (x + dx, y - 0.164, z + 0.13), (0.039, 0.038, 0.16), color)
    return part


def build_gas_cylinder():
    part = HeroPart('gas_a')
    vessel = [(0.112, 0, 'metal'), (0.125, 0.031, 'metal'), (0.13, 0.069, 'body'),
              (0.163, 0.102, 'body'), (0.176, 0.14, 'top'), (0.176, 0.49, 'top'),
              (0.165, 0.536, 'top'), (0.119, 0.579, 'body'), (0.075, 0.601, 'metal')]
    part.revolve((0, 0, 0), 'z', vessel, segments=20)
    part.revolve((0, 0, 0), 'z', [(0.028, 0.589, 'metal'), (0.033, 0.629, 'metal'),
                                  (0.027, 0.659, 'wall'), (0.023, 0.678, 'wall')], segments=12)
    for x in (-0.106, 0.106):
        part.tube([(x, 0, 0.575), (x, 0, 0.648), (x * 0.78, 0, 0.695),
                   (x * 0.28, 0, 0.703)], 0.016, 'metal', sides=7)
    rbox(part, (0, -0.047, 0.636), (0.045, 0.079, 0.051), 'metal', radius=0.006)
    return part


def build_corner_mirror():
    part = HeroPart('mirror_a')
    part.revolve((0, 0, 0), 'z', [(0.118, 0, 'wall'), (0.125, 0.043, 'wall'),
                                  (0.067, 0.076, 'metal'), (0.042, 0.125, 'metal'),
                                  (0.033, 2.33, 'metal')], segments=16)
    part.tube([(0, 0, 2.08), (0, -0.10, 2.25), (0, -0.182, 2.31)], 0.047, 'metal', sides=10)
    part.revolve((0, 0, 2.30), 'y', [(0.055, -0.085, 'body'), (0.26, -0.108, 'wall'),
                                      (0.32, -0.141, 'top'), (0.326, -0.176, 'metal'),
                                      (0.311, -0.184, 'metal'), (0.286, -0.194, 'screen'),
                                      (0.176, -0.243, 'screen'), (0.006, -0.269, 'screen')], segments=22)
    return part

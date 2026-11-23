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
            build_vacant_plot(), build_fence(), build_notice())


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

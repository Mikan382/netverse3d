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
    return build_street_tree('a'), build_street_tree('b'), build_tree_pit()

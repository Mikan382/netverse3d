from math import cos, pi, sin
from random import Random

from hero_solid import tag


def foliage(part, center, radius, height, seed, segments=15):
    rng = Random(seed)
    x, y, z = center
    scales = [(0.18, 0.0), (0.7, 0.15), (1.0, 0.39), (0.88, 0.67), (0.56, 0.89), (0.12, 1.0)]
    phases = [rng.uniform(0.83, 1.12) for _ in range(segments)]
    rings = []
    for ring, (scale, level) in enumerate(scales):
        points = []
        for index, phase in enumerate(phases):
            angle = 2 * pi * (index + 0.18 * (ring % 2)) / segments
            reach = radius * scale * phase
            lift = rng.uniform(-0.035, 0.035) * height
            points.append((x + reach * cos(angle), y + reach * sin(angle), z + height * level + lift))
        rings.append(points)
    first = set(part.bm.faces)
    part.loft(rings, lambda _row, _column: 'foliage', levels=0, closed=True, cap=True, smooth=True)
    for face in part.bm.faces:
        if face not in first:
            key = 0.3 + 0.65 * (sum(v.co.z for v in face.verts) / len(face.verts) - z) / height
            tag(part, [face], 'foliage', key, smooth=True)


def build_woody_tree(part, height, spread, seed, branch_start=0.29, branch_count=6):
    rng = Random(seed)
    trunk_radius = 0.16 * height / 5.2
    part.revolve((0, 0, 0), 'z', [
        (trunk_radius * 1.65, 0, 'body'), (trunk_radius * 1.2, height * 0.09, 'body'),
        (trunk_radius, height * 0.31, 'body'), (trunk_radius * 0.68, height * 0.63, 'body'),
        (trunk_radius * 0.28, height * 0.84, 'soft'),
    ], segments=17)
    for index in range(branch_count):
        angle = (index + rng.uniform(-0.16, 0.16)) * 2 * pi / branch_count
        end = (spread * rng.uniform(0.74, 1) * cos(angle), spread * rng.uniform(0.73, 1) * sin(angle),
               height * rng.uniform(0.58, 0.73))
        x, y, z = end
        branch_radius = trunk_radius * 0.42
        part.tube([(0, 0, height * (branch_start + index * 0.027)), (x * 0.56, y * 0.56, z - height * 0.11), end],
                  branch_radius, 'body', sides=9)
        part.tube([(x * 0.43, y * 0.43, z - height * 0.14), (x * 0.67 - y * 0.20, y * 0.66 + x * 0.21, z + height * 0.08)],
                  branch_radius * 0.53, 'soft', sides=7)
        foliage(part, (x, y, z - height * 0.07), spread * rng.uniform(0.53, 0.83), height * 0.27, seed + index)
        if index % 2 == 0:
            foliage(part, (x * 0.65 - y * 0.20, y * 0.65 + x * 0.20, z + height * 0.01),
                    spread * 0.43, height * 0.23, seed + 10 + index, segments=11)
    foliage(part, (spread * 0.12, -spread * 0.08, height * 0.75), spread * 0.77, height * 0.24, seed + 20)

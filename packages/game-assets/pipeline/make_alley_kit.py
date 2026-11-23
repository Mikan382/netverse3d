import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hero_alley import build_alley_parts
from hero_kit import MATERIAL_ORDER, anchor, bake_isolated, finish_hero

OUTPUT = sys.argv[sys.argv.index('--') + 1]
COLLISIONS = {
    'tree_a': (1.22, 0.34),
    'tree_b': (0.82, 0.19),
}


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.preferences.filepaths.save_version = 0
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    collection = scene.collection
    materials = [bpy.data.materials.new(name) for name in MATERIAL_ORDER]
    for material in materials:
        material.use_nodes = True
    parts = build_alley_parts()
    built = {part.name: finish_hero(part, collection, materials) for part in parts}
    for name, (half_height, radius) in COLLISIONS.items():
        anchor(built[name], 'collision_main', collection, (0, 0, half_height), (radius, radius, half_height))
    bake_isolated(scene, collection, built, materials[0], 'alley-parts-lightmap', 0.65)
    bpy.ops.wm.save_as_mainfile(filepath=OUTPUT, compress=True)


main()

import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hero_alley import build_alley_parts
from hero_kit import MATERIAL_ORDER, anchor, bake_isolated, finish_hero

OUTPUT = sys.argv[sys.argv.index('--') + 1]
COLLISIONS = {
    'tree_a': (0.34, 0.34, 1.22),
    'tree_b': (0.19, 0.19, 0.82),
    'fence_a': (2, 0.11, 1.01),
    'notice_a': (0.90, 0.13, 1.02),
    'crate_a': (0.263, 0.22, 0.45),
    'gas_a': (0.18, 0.18, 0.35),
    'mirror_a': (0.13, 0.13, 1.06),
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
    for name, scale in COLLISIONS.items():
        anchor(built[name], 'collision_main', collection, (0, 0, scale[2]), scale)
    bake_isolated(scene, collection, built, materials[0], 'alley-parts-lightmap', 0.65)
    bpy.ops.wm.save_as_mainfile(filepath=OUTPUT, compress=True)


main()

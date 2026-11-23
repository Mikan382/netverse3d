import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hero_city_landmarks import build_landmark_parts
from hero_kit import MATERIAL_ORDER, anchor, bake_isolated, finish_hero

OUTPUT = sys.argv[sys.argv.index('--') + 1]
COLLISIONS = {
    'crescent_podium_a': ((0, 0, 2.25), (17, 14, 2.25)),
    'bundled_podium_a': ((0, 0, 2.25), (23, 17, 2.25)),
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
    parts = build_landmark_parts()
    built = {part.name: finish_hero(part, collection, materials) for part in parts}
    for name, (location, scale) in COLLISIONS.items():
        anchor(built[name], 'collision_main', collection, location, scale)
    bake_isolated(scene, collection, built, materials[0], 'landmark-parts-lightmap', 1.2,
                  ground_for=lambda name: name in COLLISIONS)
    bpy.ops.wm.save_as_mainfile(filepath=OUTPUT, compress=True)


main()

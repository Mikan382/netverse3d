import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hero_kit import MATERIAL_ORDER, anchor, bake_isolated, finish_hero
from hero_park import build_park_parts

OUTPUT = sys.argv[sys.argv.index('--') + 1]
COLLISIONS = {
    'park_tree_a': (('collision_main', (0, 0, 1), (0.2, 0.2, 1)),),
    'park_tree_b': (('collision_main', (0, 0, 0.7), (0.2, 0.2, 0.7)),),
    'park_planting_a': (('collision_main', (0, 0, 0.3), (0.94, 0.4, 0.3)),),
    'park_planting_b': (('collision_main', (0, 0, 0.3), (0.94, 0.4, 0.3)),),
    'park_seat_a': (('collision_main', (0, 0, 0.38), (0.96, 0.29, 0.38)),),
    'park_lamp_a': (('collision_main', (0, 0, 0.6), (0.19, 0.19, 0.6)),),
    'park_gate_a': (
        ('collision_main', (-1.64, 0, 1.25), (0.22, 0.26, 1.25)),
        ('collision_right', (1.64, 0, 1.25), (0.22, 0.26, 1.25)),
    ),
    'park_fountain_a': (('collision_main', (0, 0, 0.44), (1.78, 1.78, 0.44)),),
    'park_play_a': (('collision_main', (0, -0.46, 1), (0.85, 1.8, 1)),),
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
    parts = build_park_parts()
    built = {part.name: finish_hero(part, collection, materials) for part in parts}
    for name, boxes in COLLISIONS.items():
        for label, location, scale in boxes:
            anchor(built[name], label, collection, location, scale)
    bake_isolated(scene, collection, built, materials[0], 'park-parts-lightmap', 0.65)
    bpy.ops.wm.save_as_mainfile(filepath=OUTPUT, compress=True)


main()

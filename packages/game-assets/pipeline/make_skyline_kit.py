import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hero_kit import bake_isolated, finish_hero
from hero_skyline import build_bridge, build_highrise_a, build_highrise_b, build_highrise_c, build_tower

OUTPUT = sys.argv[sys.argv.index('--') + 1]


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0
    collection = scene.collection
    materials = [bpy.data.materials.new(name) for name in ('surface', 'glow', 'display', 'decal', 'legend')]
    for material in materials:
        material.use_nodes = True
    built = {}
    for builder in (build_tower, build_bridge, build_highrise_a, build_highrise_b, build_highrise_c):
        part = builder()
        built[part.name] = finish_hero(part, collection, materials)
    bake_isolated(scene, collection, built, materials[0], 'skyline-parts-lightmap', 2.0)
    for ob in bpy.data.objects:
        if ob.type == 'MESH':
            print('PART', ob.name, sum(len(p.vertices) - 2 for p in ob.data.polygons))
    bpy.ops.wm.save_as_mainfile(filepath=OUTPUT, compress=True)


main()

import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';
import { createAlleyTrack } from '../runtime/alley-showcase.mjs';
import { streetPlan } from '../runtime/street-look.mjs';
import { connectedComponents, partTriangles, placeTriangles } from './coplanar.mjs';
import { hasGlbHeader, readGlb, readGlbBinary } from './lib.mjs';

const block = JSON.parse(readFileSync(new URL('../blocks/hem-mau.json', import.meta.url), 'utf8'));
const streetKit = readFileSync(new URL('../exported/street-parts.glb', import.meta.url));
const showcase = readFileSync(new URL('../exported/showcase-hem-mau.glb', import.meta.url));
const structures = streetPlan(block).filter(({ slot }) => slot === 'pole' || slot === 'lamp');

test('camera đi cong dọc hẻm ở tầm mắt và dừng tại điểm cuối', () => {
  const track = createAlleyTrack(block);
  const points = Array.from({ length: 73 }, (_, index) => track.sample(index / 4));
  for (const [index, shot] of points.entries()) {
    assert.ok(shot.position[1] >= 1.35 && shot.position[1] <= 1.8);
    assert.ok(shot.position[2] > 3 && shot.position[2] < 6);
    assert.ok(shot.direction[0] > 0.75);
    if (index > 0) assert.ok(shot.position[0] > points[index - 1].position[0]);
  }
  assert.ok(Math.abs(points[0].position[2] - points[36].position[2]) > 0.25);
  assert.equal(points.at(-1).done, true);
  assert.deepEqual(track.sample(19).position, points.at(-1).position);
  assert.deepEqual(track.sample(19).direction, points.at(-1).direction);
});

test('cột và đèn nằm sát bó vỉa trong dữ liệu hẻm', () => {
  assert.equal(structures.length, 4);
  assert.ok(structures.every(({ position }) => position[2] >= 2.8 && position[2] < 3));
});

function componentBounds(triangles) {
  const bounds = new Map();
  const components = connectedComponents(triangles);
  triangles.forEach((triangle, index) => {
    const component = components[index];
    if (!bounds.has(component))
      bounds.set(component, {
        min: [Infinity, Infinity, Infinity],
        max: [-Infinity, -Infinity, -Infinity],
      });
    const { min, max } = bounds.get(component);
    for (const vertex of triangle) {
      vertex.forEach((value, axis) => {
        min[axis] = Math.min(min[axis], value);
        max[axis] = Math.max(max[axis], value);
      });
    }
  });
  return [...bounds.values()];
}

test('hình học cột và đèn không chạm mặt tiền, bản nướng giữ đúng vị trí', (context) => {
  if (!hasGlbHeader(streetKit) || !hasGlbHeader(showcase)) {
    context.skip('Cần mô hình Git LFS thật');
    return;
  }
  const kit = readGlb(streetKit);
  const bin = readGlbBinary(streetKit);
  const plan = streetPlan(block);
  const bounds = (item) => {
    const triangles = partTriangles(kit, bin, item.part);
    assert.ok(triangles.length > 0, item.part);
    return componentBounds(placeTriangles(triangles, item.position, item.yaw));
  };
  const facades = plan
    .filter(({ slot }) => ['shopfront', 'storey', 'roof'].includes(slot))
    .flatMap(bounds);
  for (const structure of structures) {
    for (const part of bounds(structure)) {
      assert.ok(
        facades.every((facade) =>
          part.min.some(
            (value, axis) => value > facade.max[axis] || part.max[axis] < facade.min[axis],
          ),
        ),
        `${structure.part} tại ${structure.position} chạm mặt tiền`,
      );
    }
  }
  const baked = readGlb(showcase);
  for (const { part, position } of structures) {
    assert.ok(
      baked.nodes.some(
        (node) =>
          node.name.startsWith(part + '_') &&
          node.translation?.every((value, axis) => Math.abs(value - position[axis]) < 0.001),
      ),
      `${part} tại ${position} thiếu trong cảnh nướng`,
    );
  }
});

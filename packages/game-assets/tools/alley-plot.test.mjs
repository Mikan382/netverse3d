import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';
import { VACANT_PLOT_EXHIBIT } from '../runtime/alley-look.mjs';
import { coplanarOverlaps, partTriangles, placeTriangles } from './coplanar.mjs';
import { hasGlbHeader, readGlb, readGlbBinary } from './lib.mjs';

test('lô trống ghép bốn ô lưới, có hàng rào ba cạnh và lối mở trước bảng', () => {
  const plot = VACANT_PLOT_EXHIBIT.filter(([name]) => name === 'plot_a');
  assert.deepEqual(
    plot.map(([, position]) => position),
    [
      [-2, 0, -2],
      [-2, 0, 2],
      [2, 0, -2],
      [2, 0, 2],
    ],
  );
  assert.equal(VACANT_PLOT_EXHIBIT.filter(([name]) => name === 'fence_a').length, 6);
  assert.ok(VACANT_PLOT_EXHIBIT.some(([name]) => name === 'notice_a'));
});

test('các tấm nền và hàng rào của lô trống không chồng mặt trong bản xuất', (context) => {
  const data = readFileSync(new URL('../exported/alley-parts.glb', import.meta.url));
  if (!hasGlbHeader(data)) {
    context.skip('Cần mô hình Git LFS thật');
    return;
  }
  const gltf = readGlb(data);
  const bin = readGlbBinary(data);
  const fixtures = VACANT_PLOT_EXHIBIT.filter(([name]) => name === 'plot_a' || name === 'fence_a');
  const placements = fixtures.map(([name, position, yaw], index) => {
    const triangles = partTriangles(gltf, bin, name);
    assert.ok(triangles.length > 0, name);
    return { label: `${name}:${index}`, triangles: placeTriangles(triangles, position, yaw) };
  });
  assert.deepEqual(coplanarOverlaps(placements, { acrossOnly: true }), []);
});

import assert from 'node:assert/strict';
import test from 'node:test';
import { PARK_EXHIBIT, parkGroundPlan } from './park-look.mjs';

test('lô từ 8 đến 16 m có đủ ô ghép và khớp biên theo lưới 4 m', () => {
  for (const size of [8, 12, 16]) {
    const tiles = parkGroundPlan(size);
    assert.equal(tiles.length, (size / 4) ** 2);
    assert.equal(new Set(tiles.map(([, position]) => position.join(','))).size, tiles.length);
    const xs = tiles.map(([, [x]]) => x);
    const zs = tiles.map(([, [, , z]]) => z);
    assert.equal(Math.max(...xs) - Math.min(...xs) + 4, size);
    assert.equal(Math.max(...zs) - Math.min(...zs) + 4, size);
    assert.ok(tiles.some(([name]) => name === 'park_tile_a'));
    assert.ok(tiles.some(([name]) => name === 'park_tile_b'));
  }
  assert.throws(() => parkGroundPlan(10), RangeError);
});

test('bộ ghép công viên có cửa vào, nước, sân chơi và người để so tỉ lệ', () => {
  const names = new Set(PARK_EXHIBIT.map(([name]) => name));
  for (const name of ['park_gate_a', 'park_fountain_a', 'park_play_a', 'bin_a', 'player']) {
    assert.ok(names.has(name), name);
  }
});

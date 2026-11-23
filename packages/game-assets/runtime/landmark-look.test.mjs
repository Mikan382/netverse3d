import assert from 'node:assert/strict';
import { test } from 'node:test';
import { EMISSIVE_SCALE } from './lighting.mjs';
import { LANDMARK_VIEWS, kitGlowBoost } from './landmark-look.mjs';

test('đèn tháp dùng đúng khoảng phát sáng neon ở lab và danh mục', () => {
  const scale = EMISSIVE_SCALE.neon;
  assert.equal(kitGlowBoost('landmark-parts.glb'), scale.default);
  assert.equal(kitGlowBoost('landmark-parts.glb', 0.1), scale.min);
  assert.equal(kitGlowBoost('landmark-parts.glb', 10), scale.max);
  assert.equal(kitGlowBoost('street-parts.glb', 0.7), 0.7);
});

test('mỗi tháp có góc tầm mắt và tầm trung nằm trong khoảng hiển thị bản chi tiết', () => {
  assert.equal(Object.keys(LANDMARK_VIEWS).length, 4);
  for (const [name, { position, target }] of Object.entries(LANDMARK_VIEWS)) {
    assert.ok(Math.hypot(...position) < 190, name);
    assert.ok(Math.hypot(...target) < 190, name);
    if (name.startsWith('Chân tháp')) assert.equal(position[1], 1.65, name);
    else assert.ok(position[1] > 50, name);
  }
});

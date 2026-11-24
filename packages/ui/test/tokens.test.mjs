import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import {
  colors,
  contrastRatio,
  indicators,
  motion,
  scales,
  surfaces,
  text,
} from '../library/token-catalog.mjs';

const tokens = (file) => readFileSync(new URL(`../tokens/${file}.css`, import.meta.url), 'utf8');
const primitive = tokens('primitive');
const semantic = tokens('semantic');
const timing = tokens('motion');
const files = [primitive, semantic, timing];
const parse = (css) =>
  Object.fromEntries([...css.matchAll(/(--ui-[\w-]+):\s*([^;]+);/g)].map((m) => m.slice(1)));
const firstRule = (css) => css.split('}')[0];
const defaults = Object.assign({}, ...files.map((css) => parse(firstRule(css))));

function value(name, properties = defaults) {
  const current = properties[name];
  const reference = /^var\((--ui-[\w-]+)\)$/.exec(current ?? '');
  return reference ? value(reference[1], properties) : current;
}

function verifyPairs(foregrounds, backgrounds, minimum) {
  for (const foreground of foregrounds) {
    for (const background of backgrounds) {
      assert.ok(
        contrastRatio(value(foreground), value(background)) >= minimum,
        `${foreground} / ${background}`,
      );
    }
  }
}

test('chữ chính trên mọi mặt nền đạt tương phản 4.5:1', () => {
  verifyPairs(text, surfaces, 4.5);
  verifyPairs(['--ui-on-action'], ['--ui-action-primary', '--ui-action-danger'], 4.5);
});

test('viền focus và màu trạng thái đạt 3:1 trên mặt nền', () => {
  verifyPairs(indicators, surfaces, 3);
});

test('đổi accent tiệm không đổi màu trạng thái lỗi', () => {
  const changed = { ...defaults, '--ui-accent': '#330000' };
  for (const token of indicators) assert.equal(value(token, changed), value(token));
});

test('khi người dùng chọn giảm chuyển động, mọi thời lượng về 0', () => {
  const override = {
    ...defaults,
    ...parse(timing.match(/@media \(prefers-reduced-motion: reduce\)[\s\S]+/)?.[0] ?? ''),
  };
  for (const token of motion) assert.equal(value(token, override), '0ms', token);
});

test('mức chất lượng thấp dùng nền đặc thay kính', () => {
  const low = semantic.match(/:root\[data-ui-quality='low'\][^{]+\{([^}]+)\}/)?.[1] ?? '';
  const override = { ...defaults, ...parse(low) };
  assert.equal(value('--ui-panel', override), value('--ui-surface'));
  assert.equal(value('--ui-panel-filter', override), 'none');
  assert.notEqual(value('--ui-panel', override), value('--ui-panel'));
});

test('component không ghi mã màu và chỉ dùng biến đã khai', () => {
  const root = fileURLToPath(new URL('../../../apps/web-3d/', import.meta.url));
  for (const area of ['app', 'src/ui']) {
    for (const file of readdirSync(join(root, area), { recursive: true }).filter((name) =>
      name.endsWith('.module.css'),
    )) {
      const path = join(root, area, file);
      const css = readFileSync(path, 'utf8');
      assert.doesNotMatch(css, /#[\da-f]{3,8}\b|\b(?:rgb|hsl)a?\(/i, path);
      for (const [, variable] of css.matchAll(/var\((--[\w-]+)/g)) {
        assert.ok(Object.hasOwn(defaults, variable), `${path}: ${variable}`);
      }
    }
  }
});

test('mọi token ngữ nghĩa có mặt trong thư viện', () => {
  assert.deepEqual(
    [...new Set([...colors, ...scales, ...motion])].sort(),
    Object.keys(defaults).sort(),
  );
});

import './library.css';
import {
  colors,
  motion,
  scales,
  surfaces,
  indicators,
  text,
  contrastRatio,
} from './token-catalog.mjs';

const { document, getComputedStyle } = globalThis;
const root = document.documentElement;
const element = (id) => document.getElementById(id);
const controls = {
  accent: element('accent'),
  quality: element('quality'),
  motion: element('motion'),
  transparency: element('transparency'),
};

function card(name, value, kind) {
  const article = document.createElement('article');
  article.className = 'token';
  article.dataset.token = name;
  if (kind === 'color') {
    const swatch = document.createElement('span');
    swatch.className = 'swatch';
    swatch.style.background = `var(${name})`;
    article.append(swatch);
  }
  const label = document.createElement('code');
  label.textContent = name;
  const current = document.createElement('p');
  current.textContent = value;
  article.append(label, current);
  if (kind === 'motion') {
    const track = document.createElement('button');
    track.type = 'button';
    track.className = 'track';
    track.setAttribute('aria-label', `Thử ${name}`);
    track.style.setProperty('--sample-duration', `var(${name})`);
    const dot = document.createElement('span');
    dot.className = 'dot';
    track.append(dot);
    track.addEventListener('click', () => track.toggleAttribute('data-active'));
    article.append(track);
  }
  return article;
}

function render() {
  root.style.setProperty('--ui-accent', controls.accent.value);
  root.dataset.uiQuality = controls.quality.value;
  root.dataset.uiMotion = controls.motion.checked ? 'reduced' : 'default';
  root.dataset.uiTransparency = controls.transparency.checked ? 'reduced' : 'default';
  const style = getComputedStyle(root);
  const get = (name) => style.getPropertyValue(name).trim();
  element('colors').replaceChildren(...colors.map((name) => card(name, get(name), 'color')));
  element('scales').replaceChildren(...scales.map((name) => card(name, get(name), 'scale')));
  element('motion-samples').replaceChildren(
    ...motion.map((name) => card(name, get(name), 'motion')),
  );

  const matches = [
    ...text.flatMap((color) => surfaces.map((surface) => [color, surface, 4.5])),
    ...indicators.flatMap((color) => surfaces.map((surface) => [color, surface, 3])),
    ...['--ui-action-primary', '--ui-action-danger'].map((surface) => [
      '--ui-on-action',
      surface,
      4.5,
    ]),
  ];
  const rows = matches.map(([color, surface, minimum]) => {
    const ratio = contrastRatio(get(color), get(surface));
    const tr = document.createElement('tr');
    for (const value of [color, surface, ratio.toFixed(2) + ':1', minimum + ':1']) {
      const td = document.createElement('td');
      td.textContent = value;
      tr.append(td);
    }
    tr.dataset.contrast = ratio >= minimum ? 'pass' : 'fail';
    return tr;
  });
  element('contrast').replaceChildren(...rows);
}

element('theme-controls').addEventListener('input', render);
for (const query of [
  '(prefers-reduced-motion: reduce)',
  '(prefers-reduced-transparency: reduce)',
]) {
  globalThis.matchMedia(query).addEventListener('change', render);
}
render();

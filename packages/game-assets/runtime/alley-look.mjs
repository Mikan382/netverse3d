import { SIDEWALK_TOP, STREET_CELL } from './street-look.mjs';

const tileCentre = STREET_CELL / 2;
const border = STREET_CELL - 0.13;

export const VACANT_PLOT_EXHIBIT = [
  ...[-tileCentre, tileCentre].flatMap((x) =>
    [-tileCentre, tileCentre].map((z) => ['plot_a', [x, 0, z], 0]),
  ),
  ...[-tileCentre, tileCentre].flatMap((offset) => [
    ['fence_a', [offset, SIDEWALK_TOP, -STREET_CELL - 0.09], 0],
    ['fence_a', [-border, SIDEWALK_TOP, offset + 0.12], Math.PI / 2],
    ['fence_a', [border, SIDEWALK_TOP, offset + 0.12], Math.PI / 2],
    ['sidewalk_a', [offset, 0, STREET_CELL + 0.5], 0],
  ]),
  ['notice_a', [0.82, SIDEWALK_TOP, 3.65], 0],
  ['player', [-1.4, SIDEWALK_TOP, 4.47], 0],
];

export const ALLEY_PROPS_EXHIBIT = [
  ['road_a', [0, 0, 2], 0],
  ['sidewalk_a', [0, 0, 0], 0],
  ['shopfront_a', [0, 0, -0.65], 0],
  ['crate_a', [-0.79, SIDEWALK_TOP, -0.12], 0],
  ['gas_a', [0.1, SIDEWALK_TOP, 0.05], 0],
  ['mirror_a', [1.29, SIDEWALK_TOP, 0.26], -Math.PI / 9],
  ['hydrant_a', [-1.73, SIDEWALK_TOP, 0.13], 0],
  ['bollard_a', [1.83, SIDEWALK_TOP, 0.34], 0],
  ['player', [0.54, SIDEWALK_TOP, 1.05], 0],
];

export function vacancyNoticeMaterial(
  THREE,
  createCanvas = () => globalThis.document.createElement('canvas'),
) {
  const canvas = createCanvas();
  canvas.width = 512;
  canvas.height = 128;
  const context = canvas.getContext('2d');
  context.fillStyle = '#14151c';
  context.fillRect(0, 0, canvas.width, canvas.height);
  context.font = '700 56px sans-serif';
  context.textAlign = 'center';
  context.textBaseline = 'middle';
  context.fillStyle = '#f2ede1';
  context.fillText('LÔ TRỐNG', canvas.width / 2, canvas.height / 2 + 2);
  const map = new THREE.CanvasTexture(canvas);
  map.colorSpace = THREE.SRGBColorSpace;
  map.flipY = false;
  return new THREE.MeshStandardMaterial({ map, roughness: 0.72 });
}

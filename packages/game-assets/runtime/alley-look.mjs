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

export function vacancyNoticeMaterial(
  THREE,
  createCanvas = () => document.createElement('canvas'),
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

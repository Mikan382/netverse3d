export const PARK_TILE_SIZE = 4;

export function parkRecipe(THREE, recipe) {
  const tint = (base, colors) =>
    colors.map(
      (color) => `#${new THREE.Color(base).lerp(new THREE.Color(color), 0.12).getHexString()}`,
    );
  const emissive = { ...recipe.emissive };
  delete emissive.trim;
  return {
    ...recipe,
    palette: {
      ...recipe.palette,
      trim: tint('#306447', recipe.palette.trim),
      strip: tint('#ffb45c', recipe.palette.strip),
    },
    emissive,
  };
}

const PARK_PROPS = [
  ['park_gate_a', [0, 0.16, 7.7], 0],
  ['park_fountain_a', [2.1, 0.16, -2], 0],
  ['park_play_a', [-5.8, 0.14, -3.8], 0],
  ['park_tree_a', [6.1, 0.14, -5.8], 0],
  ['park_tree_b', [-6.0, 0.14, 5.1], 0],
  ['park_planting_a', [6.6, 0.14, 3.1], Math.PI / 2],
  ['park_planting_b', [-3.8, 0.14, -6.5], 0],
  ['park_seat_a', [-4.3, 0.14, 3.85], 0],
  ['park_seat_a', [5.25, 0.14, -2.7], Math.PI / 2],
  ['park_bin_a', [-5.55, 0.14, 3.85], 0],
  ['park_lamp_a', [-3.85, 0.14, 6.0], 0],
  ['park_lamp_a', [4.3, 0.14, 5.6], 0],
  ['park_lamp_a', [-2.9, 0.14, -4.9], 0],
];

export function parkGroundPlan(size) {
  if (!Number.isInteger(size) || size < 8 || size > 16 || size % PARK_TILE_SIZE !== 0) {
    throw new RangeError('park size must be 8, 12 or 16 metres');
  }
  const count = size / PARK_TILE_SIZE;
  const centre = (count - 1) / 2;
  return Array.from({ length: count * count }, (_, index) => {
    const column = index % count;
    const row = Math.floor(index / count);
    const x = (column - centre) * PARK_TILE_SIZE;
    const z = (row - centre) * PARK_TILE_SIZE;
    const path = column === Math.floor(centre) || (count === 4 && column === Math.ceil(centre));
    const plaza = count > 2 && row === Math.floor(centre);
    const paved = path || plaza;
    const curb = plaza && !path;
    return [`park_tile_${curb ? 'c' : paved ? 'b' : 'a'}`, [x, 0, z], x > 0 ? Math.PI : 0];
  });
}

export const PARK_EXHIBIT = [...parkGroundPlan(16), ...PARK_PROPS, ['player', [1, 0.16, 4.6], 0]];

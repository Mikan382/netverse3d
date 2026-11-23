import { EMISSIVE_SCALE, clampEmissiveIntensity } from './lighting.mjs';

export function kitGlowBoost(file, previewBoost = 1.1) {
  if (file !== 'landmark-parts.glb') return previewBoost;
  return clampEmissiveIntensity('neon', (EMISSIVE_SCALE.neon.default * previewBoost) / 1.1);
}

export function applyLandmarkGlow(glow, rows) {
  if (!glow) return;
  const windowRow = (rows.indexOf('screen') + 0.5) / rows.length;
  const tolerance = 0.5 / rows.length;
  const windowScale = EMISSIVE_SCALE.window.default / EMISSIVE_SCALE.neon.default;
  glow.onBeforeCompile = (shader) => {
    shader.fragmentShader = shader.fragmentShader.replace(
      '#include <map_fragment>',
      `#include <map_fragment>
      #ifdef USE_MAP
        if (abs(vMapUv.y - ${windowRow.toFixed(8)}) < ${tolerance.toFixed(8)}) {
          diffuseColor.rgb *= ${windowScale.toFixed(8)};
        }
      #endif`,
    );
  };
  glow.customProgramCacheKey = () => `landmark-windows:${windowRow}:${tolerance}`;
}

export const LANDMARK_VIEWS = {
  'Chân tháp Vành Mây': { position: [16, 1.65, 29], target: [0, 11, 5] },
  'Vành Mây tầm trung': { position: [42, 84, 91], target: [0, 101, 0] },
  'Chân tháp Nhịp Trời': { position: [18, 1.65, 36], target: [0, 13, 8] },
  'Nhịp Trời tầm trung': { position: [52, 95, 105], target: [2, 115, 0] },
};

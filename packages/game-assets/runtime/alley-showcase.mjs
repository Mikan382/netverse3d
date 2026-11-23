import { createCameraTrack } from './camera-track.mjs';
import { roadLane } from './street-look.mjs';

export const ALLEY_LAMP_LIGHT_OFFSET = [0, 4.5, 1.15];

export function createAlleyTrack(block, duration = 18) {
  const lane = roadLane(block);
  if (lane.length < 2) throw new RangeError('Alley camera track requires at least two road cells');
  const first = lane[0];
  const last = lane.at(-1);
  const dx = last[0] - first[0];
  const dz = last[1] - first[1];
  const length = Math.hypot(dx, dz);
  const along = [dx / length, dz / length];
  const across = [-along[1], along[0]];
  const shots = [
    [0, 1.63, 0.95],
    [0.34, 1.58, 0.78],
    [0.68, 1.64, 0.28],
    [1, 1.6, 0.65],
  ];
  const points = shots.map(([progress, height, offset]) => {
    const x = first[0] + dx * progress + across[0] * offset;
    const z = first[1] + dz * progress + across[1] * offset;
    return {
      position: [x, height, z],
      target: [
        x + 2.8 * along[0] - 1.15 * across[0],
        height - 0.24,
        z + 2.8 * along[1] - 1.15 * across[1],
      ],
    };
  });
  const track = createCameraTrack(points, { duration, loop: false });
  return {
    sample(time) {
      const progress = Math.min(1, Math.max(0, time / duration));
      const eased = progress * progress * (3 - 2 * progress);
      return track.sample(eased * duration);
    },
  };
}

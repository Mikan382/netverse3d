const tokens = (names) => names.split(' ').map((name) => `--ui-${name}`);

export const colors = tokens(
  'core-night core-plum core-raised core-glass core-white core-silver core-border core-lavender core-focus core-mint core-amber core-rose core-sky core-scrim core-shadow canvas surface surface-raised surface-glass panel text text-muted border focus action-primary action-neutral action-danger on-action success warning error info accent scrim shadow',
);

export const scales = tokens(
  'panel-filter font-family text-xs text-sm text-base text-lg text-xl weight-normal weight-medium weight-bold line-tight line-normal space-1 space-2 space-3 space-4 space-6 space-8 radius-1 radius-2 radius-3 radius-pill layer-canvas layer-world layer-hud layer-toast layer-dialog layer-recovery',
);

export const motion = tokens('motion-instant motion-fast motion-base motion-panel motion-scene');
export const surfaces = tokens('canvas surface surface-raised surface-glass panel');
export const indicators = tokens('focus border success warning error info');
export const text = tokens('text text-muted');

function rgb(hex) {
  const bytes =
    hex
      .slice(1)
      .match(/../g)
      ?.map((part) => Number.parseInt(part, 16)) ?? [];
  const opacity = (bytes[3] ?? 255) / 255;
  return bytes.slice(0, 3).map((channel) => channel * opacity + 255 * (1 - opacity));
}

function luminance(hex) {
  return rgb(hex).reduce((sum, channel, index) => {
    const value = channel / 255;
    const linear = value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
    return sum + linear * [0.2126, 0.7152, 0.0722][index];
  }, 0);
}

export function contrastRatio(foreground, background) {
  const first = luminance(foreground);
  const second = luminance(background);
  return (Math.max(first, second) + 0.05) / (Math.min(first, second) + 0.05);
}

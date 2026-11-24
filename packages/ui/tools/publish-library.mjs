import { build } from 'esbuild';
import { copyFile, mkdir } from 'node:fs/promises';
import { createRequire } from 'node:module';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const require = createRequire(import.meta.url);

export async function publishLibrary(target) {
  const outdir = resolve(target);
  await mkdir(outdir, { recursive: true });
  await build({
    entryPoints: [resolve(root, 'library/library.mjs')],
    bundle: true,
    format: 'esm',
    outdir,
    assetNames: 'fonts/[name]-[hash]',
    loader: { '.woff2': 'file', '.woff': 'file' },
  });
  const fontPackage = require.resolve('@fontsource/be-vietnam-pro/package.json');
  await Promise.all([
    copyFile(resolve(root, 'library/index.html'), resolve(outdir, 'index.html')),
    copyFile(resolve(dirname(fontPackage), 'LICENSE'), resolve(outdir, 'font-license.txt')),
  ]);
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  if (!process.argv[2]) throw new Error('Usage: node tools/publish-library.mjs <target folder>');
  await publishLibrary(process.argv[2]);
}

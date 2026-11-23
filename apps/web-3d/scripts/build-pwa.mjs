import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';

const out = new URL('../out/', import.meta.url);
const [index, worker, offline] = await Promise.all([
  readFile(new URL('index.html', out)),
  readFile(new URL('./pwa-worker.mjs', import.meta.url), 'utf8'),
  readFile(new URL('./pwa-offline.html', import.meta.url), 'utf8'),
]);
const version = createHash('sha256').update(index).digest('hex');
await writeFile(
  new URL('sw.js', out),
  `/* web-3d ${version} */\nconst OFFLINE_HTML = ${JSON.stringify(offline)};\n${worker}`,
);

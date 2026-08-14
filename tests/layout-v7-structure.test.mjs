import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const html = await readFile(new URL('../layout-v7.html', import.meta.url), 'utf8');

const pipeIds = [...html.matchAll(/id=["'](pipe-[^"']+)["']/g)].map((match) => match[1]);
assert.deepEqual(pipeIds.sort(), ['pipe-left', 'pipe-right', 'pipe-stem'], 'the distributor must expose exactly three glass pipe paths');

for (const id of ['jelly-top-mass', 'jelly-bottom-mass', 'jelly-neck', 'jelly-top-wave', 'jelly-bottom-wave', 'hourglass-shell', 'background-pipe-left', 'background-pipe-right', 'ribbon-orange', 'ribbon-yellow']) {
  assert.match(html, new RegExp(`id=["']${id}["']`), `missing visual layer: ${id}`);
}

assert.match(html, /requestAnimationFrame/, 'the jelly component must run a frame loop');
assert.match(html, /(?:this\.)?remaining\s*=/, 'missing remaining state');
assert.match(html, /(?:this\.)?total\s*=/, 'missing total state');
assert.match(html, /(?:this\.)?used\s*=/, 'missing used state');
assert.match(html, /Math\.sin/, 'liquid surface must be computed from sine waves');
assert.match(html, /remaining\s*\/\s*(?:this\.)?total|(?:this\.)?remaining\s*\/\s*(?:this\.)?total/, 'missing remaining-to-total liquid level mapping');
assert.match(html, /prefers-reduced-motion/, 'missing reduced-motion handling');
assert.match(html, /Number\.isFinite/, 'setProgress must reject non-finite progress inputs');
assert.match(html, /addEventListener\(['"]change['"]/, 'reduced-motion preference changes must be observed');
assert.match(html, /cancelAnimationFrame/, 'reduced-motion changes must cancel active animation frames');
assert.match(html, /setProgress[\s\S]*?this\.used\s*=\s*safeTotal\s*-\s*this\.remaining;\s*if\s*\(this\.reduced\)[\s\S]*?this\.displayRatio\s*=\s*this\.remaining\s*\/\s*this\.total;[\s\S]*?this\.tick\(0\)/, 'reduced-motion progress updates must render a static liquid state');

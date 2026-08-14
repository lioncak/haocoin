import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const html = await readFile(new URL('../layout-v7.html', import.meta.url), 'utf8');

const pipeIds = [...html.matchAll(/id=["'](pipe-[^"']+)["']/g)].map((match) => match[1]);
assert.deepEqual(pipeIds.sort(), ['pipe-berry', 'pipe-cream', 'pipe-mint'], 'the distributor must expose exactly three named personal glass pipe paths');

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
assert.match(html, /id=["']hourglass-remaining["']/, 'missing shared hourglass remaining value');
assert.match(html, />57</, 'the shared remaining value must be 57');
assert.match(html, /共享剩餘課程/, 'missing shared remaining caption');
assert.match(html, /hourglass-remaining[\s\S]*?font-size=["'](?:5[0-9]|[6-9][0-9])["']/, 'the hero remaining value must be the largest numeric label');

for (const reservoir of ['reservoir-berry', 'reservoir-cream', 'reservoir-mint']) {
  assert.match(html, new RegExp(`id=["']${reservoir}["']`), `missing terminal jelly reservoir: ${reservoir}`);
}

for (const [name, remaining, completed, consumed] of [
  ['莓果重拳', '16', '4\\s*\\/\\s*14', '42\\s*\\/\\s*58'],
  ['奶油鐵手', '18', '4\\s*\\/\\s*14', '40\\s*\\/\\s*58'],
  ['薄荷軟骨', '23', '5\\s*\\/\\s*14', '35\\s*\\/\\s*58'],
]) {
  assert.match(html, new RegExp(name), `missing person name: ${name}`);
  assert.match(html, new RegExp(remaining), `missing remaining value: ${remaining}`);
  assert.match(html, new RegExp(completed), `missing completed value: ${completed}`);
  assert.match(html, new RegExp(consumed), `missing consumed value: ${consumed}`);
}

for (const module of ['module-yoga-berry', 'module-yoga-cream', 'module-boxing-mint', 'module-pilates-cream']) {
  assert.match(html, new RegExp(`id=["']${module}["']`), `missing course valve: ${module}`);
}
for (const icon of ['icon-yoga', 'icon-boxing', 'icon-pilates']) {
  assert.match(html, new RegExp(`id=["']${icon}["']`), `missing activity icon: ${icon}`);
}
assert.match(html, /id=["']bridge-yoga["']/, 'the shared yoga modules need their own bridge');
assert.match(html, /stroke-dasharray/, 'the shared yoga bridge must be visibly dashed');

for (const material of ['specular-dual', 'cyan-reservoir-glow', 'bubble-field', 'compression-seal', 'energy-particle']) {
  assert.match(html, new RegExp(`(?:id|class)=["'][^"']*${material}[^"']*["']`), `missing material layer: ${material}`);
}

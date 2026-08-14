import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const html = await readFile(new URL('../layout-v7.html', import.meta.url), 'utf8');

for (const id of ['pipe-berry', 'pipe-cream', 'pipe-mint']) {
  assert.match(html, new RegExp(`id=["']${id}["']`), `missing ${id}`);
}

for (const id of ['summary-berry', 'summary-cream', 'summary-mint']) {
  assert.match(html, new RegExp(`id=["']${id}["']`), `missing ${id}`);
}

for (const text of ['57', '瑜伽輪', '8-14', '拳擊有氧', '8-18', '皮拉提斯', '8-20']) {
  assert.match(html, new RegExp(text), `missing course content: ${text}`);
}

for (const text of ['莓果重拳', '奶油鐵手', '薄荷軟骨', '16', '18', '23', '4/14', '5/14', '42/58', '40/58', '35/58']) {
  assert.match(html, new RegExp(text), `missing personal summary content: ${text}`);
}

assert.match(html, /prefers-reduced-motion/, 'missing reduced-motion handling');
assert.match(html, /<svg[\s>]/, 'missing inline SVG pipeline');

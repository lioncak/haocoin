# Three-person pipeline redesign

## Goal

Rebuild `layout-v7.html` so it uses the supplied Jelly Fuel Pipeline reference as
the composition model. The page should read as a single neon-glass machine, not
a flowchart: one large shared hourglass feeds three permanent individual
pipelines; classes are attached modules and each pipe terminates in a compact
personal summary.

## Visual direction

- **Canvas:** a narrow mobile scene on `#081B38`, with cropped background pipes,
  orange/yellow wave ribbons and sparse bubbles as atmosphere only.
- **Hero:** a dominant blue transparent hourglass in the upper half, with a
  bright liquid mass, orange gasket bands and `57` as the largest numeral.
- **Split:** a soft transparent distributor below the hourglass. Its brief
  jelly split is organic; after this point, the three individual pipelines run
  as mostly vertical, parallel main pipes. This replaces the current wide,
  competing curved branches.
- **Pipes:** identical blue-glass exterior and electric-lemon inner flow. They
  are three readable vertical main pipes, not an even three-column grid: their
  split points, x positions, slight S/offset movement, visible lengths and
  terminal-capsule prominence are deliberately irregular. A person's identity
  comes from those positional/path differences, rather than red/yellow/green
  person coding.
- **Class modules:** small air-cushion glass modules attach left or right of
  their owner's pipe using short valve stubs. Modules contain class icon, date
  and label. A shared class uses a thin, temporary lemon bridge between its two
  appropriate modules; main pipes never merge.
- **Personal summaries:** each pipe ends in a larger vertically oriented glass
  capsule. The capsule contains the person's name, remaining-points numeral,
  completed classes over total, and consumed points. These terminal capsules
  replace the current round numbered endpoints.

## Information architecture

```
shared hourglass (57)
        |
   soft splitter
    |   |   |
 personal main pipes
    |   |   |
 class modules attached to their owner
    |   |   |
 personal summary capsules
```

The proposed content is:

| Person | Remaining | Completed | Consumed |
| --- | ---: | ---: | ---: |
| 莓果重拳 | 16 | 4 / 14 | 42 / 58 |
| 奶油鐵手 | 18 | 4 / 14 | 40 / 58 |
| 薄荷軟骨 | 23 | 5 / 14 | 35 / 58 |

## Implementation boundaries

- Keep the page dependency-free: HTML, CSS and inline SVG only.
- Reuse the existing glass gradients, glowing pipe layers, liquid and reduced-
  motion support where they still fit; replace the page-level SVG topology and
  endpoint components.
- Preserve the existing class examples (瑜伽輪, 拳擊有氧, 皮拉提斯), but relocate
  them as attached modules.
- Do not add a card-list layout, external assets or a build step.

## Acceptance checks

1. The hero hourglass is visibly the shared source and contains the dominant
   `57` value.
2. Three distinct transparent vertical pipes originate from one splitter and
   remain independent through the bottom of the scene. They must not read as
   three evenly spaced identical columns: at least one pipe has a visible
   offset/S-curve and the three terminal positions or scales are uneven.
3. Each class clearly attaches to exactly one pipe; a shared class is bridged,
   never merged.
4. The only terminal elements are three personal summary capsules, not circular
   values.
5. The visual language matches the reference's central-machine composition:
   transparent blue glass, orange seals, lemon energy, soft rounded modules,
   deep navy background.
6. The layout remains legible at the current narrow mobile width and respects
   `prefers-reduced-motion`.

## Reference responsibilities used

- `jelly-flow-structure.md`: permanent ownership of the three personal streams.
- `visual-composition-pass.md`: hero hierarchy and deliberately non-uniform
  module placement (adapted to the user's newer three-main-pipe requirement).
- `jelly-hourglass.md`: source/liquid semantics.
- `gooey-popover.md`: the source-to-three-pipe separation treatment.
- `einui.md`: glass-panel highlight and translucency recipe for the class and
  summary modules.

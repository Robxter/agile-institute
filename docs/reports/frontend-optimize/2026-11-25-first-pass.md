# frontend-optimize report 2026-11-25 (first pass)
Model/effort: Opus 5.5 (main session)   Task IDs: T-005   Branch: worktree-changes-md

## Measurements (`npm run build`, gzip)
| Asset | Size | Budget |
| --- | --- | --- |
| JS (`index-*.js`) | 53.4 KB gz | ≤ 70 KB ✅ |
| CSS (`index-*.css`) | 4.5 KB gz | ≤ 15 KB ✅ |
| Font downloaded at runtime (latin WOFF2) | 37 KB | ≤ 60 KB ✅ |

## Findings fixed
- `<head>`: brand with ™ in title and description; Open Graph tags (type, locale, site name, title, description).
- Landing: "Una vista para cada dimensión" cards are now links to each dashboard with hover and `:focus-visible` states.

## Findings left (with reason)
- Build emits 5 Montserrat subsets (cyrillic, vietnamese, latin-ext…). Browsers only download the latin one thanks to
  `unicode-range`, so runtime cost is nil; `@fontsource-variable/montserrat` ships no latin-only stylesheet, and a
  hand-written `@font-face` is not worth the maintenance.
- No `og:image`: needs a brand image from product-designer.
- Lighthouse not run in this pass (Chrome DevTools MCP not attached): T-010 for qa-engineer.

## Checks
- `npm run typecheck` → ok · `npm test` → 8 passed · `npm run build` → ok.
- `useReveal`: content visible with `prefers-reduced-motion` and without IntersectionObserver.

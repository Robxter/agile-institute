---
name: frontend-optimize
description: Measure and optimize the Agile Institute landing (front-end/) — bundle size budget, fonts, images, render cost, accessibility and Web Interface Guidelines — then fix the cheapest high-impact findings. Use when asked to optimize, speed up, audit or polish the frontend, or before a release.
---

# Frontend optimize (Agile Institute landing)

Goal: a landing that loads fast on a mid-range phone and passes accessibility checks, with the smallest diff.
Owners: frontend-engineer (TSX, content, config) and product-designer (CSS, fonts, illustrations).

## 1. Gates (run from `front-end/`, stop if any fails)
```powershell
npm run typecheck
npm test
npm run build
```

## 2. Measure the bundle against the budget
```powershell
node -e "const fs=require('fs'),z=require('zlib'),p='dist/assets/';let t={js:0,css:0};for(const f of fs.readdirSync(p)){const e=f.split('.').pop();const g=z.gzipSync(fs.readFileSync(p+f)).length;if(t[e]!==undefined)t[e]+=g;console.log(f.padEnd(40),(g/1024).toFixed(1)+' KB gz')}console.log('TOTAL js',(t.js/1024).toFixed(1),'KB gz · css',(t.css/1024).toFixed(1),'KB gz')"
```
Budget: initial JS ≤ 70 KB gz, CSS ≤ 15 KB gz, fonts ≤ 60 KB (WOFF2, latin subset only). Record the numbers.

## 3. Checklist (fix what fails, cheapest first)
1. **Fonts** — only the latin subset of Montserrat Variable is loaded (`@fontsource-variable/montserrat/wght.css`
   pulls every subset; prefer the latin-only file); `font-display: swap`; preload the one WOFF2 used above the fold.
2. **Images** — illustrations are inline SVG; any raster has `width`/`height`, `loading="lazy"` below the fold,
   and is WebP/AVIF.
3. **Render** — no layout shift from the header or reveal animation (`useReveal` must not hide content when JS fails or
   with `prefers-reduced-motion`); no work in render that can live in module scope.
4. **HTML head** — `<html lang="es">`, meta description, `theme-color`, favicon, Open Graph title/description.
5. **Accessibility** — run the `web-design-guidelines` skill on `front-end/src/components/*.tsx`; keyboard path through
   header, hero CTA, dimension links, view cards and pilot modal; focus visible; contrast AA in light and dark.
6. **Lighthouse** (optional, needs Chrome DevTools MCP) — `npm start`, open `http://127.0.0.1:5174`, run
   `lighthouse_audit` for mobile; record Performance, Accessibility, Best Practices, SEO.

## 4. Report
Write `docs/reports/frontend-optimize/<YYYY-MM-DD-HHmm>.md`: before/after sizes, findings fixed, findings left with
reason. Never add a dependency to optimize (class A); never change copy meaning or brand (™).

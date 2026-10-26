/* Gráficos sin dependencias para los cuadros de mando. Cada función devuelve HTML/SVG como texto.
   Los elementos con data-tip muestran un tooltip (ver app.js). Escala 1–5 salvo que se indique. */
(function () {
  "use strict";

  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const fmt = (v, d = 2) => (v === null || v === undefined || Number.isNaN(v)) ? "—"
    : Number(v).toLocaleString("es-ES", { minimumFractionDigits: d, maximumFractionDigits: d });
  const signed = (v, d = 0) => v === null || v === undefined ? "—" : (v > 0 ? "+" : v < 0 ? "−" : "") + fmt(Math.abs(v), d);
  const pct = (v) => v === null || v === undefined ? "—" : Math.round(v * 100) + " %";
  const scaleX = (v, lo, hi) => Math.max(0, Math.min(1, (v - lo) / (hi - lo)));

  /* Barras horizontales. rows: [{label, sub, value, ref, note}] · opts: {min, max, color, refLabel, valueLabel} */
  function bars(rows, opts = {}) {
    const lo = opts.min ?? 1, hi = opts.max ?? 5;
    const color = opts.color || "var(--bar)";
    const html = rows.map((r) => {
      const has = r.value !== null && r.value !== undefined;
      const w = has ? scaleX(r.value, lo, hi) * 100 : 0;
      const tip = `<b>${esc(r.full || r.label)}</b><br>${has ? "Media " + fmt(r.value) : esc(r.note || "Sin datos suficientes")}` +
        (r.n !== undefined ? ` · n = ${r.n}` : "") +
        (r.ref !== null && r.ref !== undefined ? `<br>${esc(opts.refLabel || "Referencia")}: ${fmt(r.ref)}` : "");
      const mark = r.ref !== null && r.ref !== undefined
        ? `<span class="mark" style="left:calc(${scaleX(r.ref, lo, hi) * 100}% - 1.5px)"></span>` : "";
      return `<div class="bar-row${has ? "" : " na"}" data-tip="${esc(tip)}" tabindex="0">
        <div class="lab">${esc(r.label)}${r.sub ? `<small>${esc(r.sub)}</small>` : ""}</div>
        <div class="track${opts.thin ? " thin" : ""}"><span class="fill" style="width:${w}%;background:${color}"></span>${mark}</div>
        <div class="val">${has ? (opts.valueFmt ? opts.valueFmt(r.value) : fmt(r.value)) : "—"}</div></div>`;
    }).join("");
    return `<div class="bars" role="list">${html}</div>`;
  }

  /* Radar. labels: [..] · series: [{name, values, color}] */
  function radar(labels, series, opts = {}) {
    const lo = opts.min ?? 1, hi = opts.max ?? 5;
    const W = 460, H = 300, cx = W / 2, cy = H / 2 + 2, R = 100, n = labels.length;
    const ang = (i) => -Math.PI / 2 + (2 * Math.PI * i) / n;
    const pt = (i, v) => { const r = R * scaleX(v, lo, hi); return [cx + r * Math.cos(ang(i)), cy + r * Math.sin(ang(i))]; };
    let g = "";
    for (let k = lo; k <= hi; k++) {
      const ring = labels.map((_, i) => pt(i, k).map((x) => x.toFixed(1)).join(",")).join(" ");
      g += `<polygon points="${ring}" fill="none" class="gridline"/>`;
      g += `<text x="${cx + 3}" y="${(cy - R * scaleX(k, lo, hi) + 11).toFixed(1)}" font-size="9">${k}</text>`;
    }
    labels.forEach((l, i) => {
      const [x, y] = pt(i, hi);
      g += `<line x1="${cx}" y1="${cy}" x2="${x.toFixed(1)}" y2="${y.toFixed(1)}" class="gridline"/>`;
      const [lx, ly] = [cx + (R + 16) * Math.cos(ang(i)), cy + (R + 16) * Math.sin(ang(i))];
      const anchor = Math.abs(lx - cx) < 8 ? "middle" : lx > cx ? "start" : "end";
      g += `<text x="${lx.toFixed(1)}" y="${(ly + 4).toFixed(1)}" text-anchor="${anchor}" font-weight="600">${esc(l)}</text>`;
    });
    series.forEach((s) => {
      const pts = s.values.map((v, i) => (v === null || v === undefined ? null : pt(i, v)));
      const valid = pts.filter(Boolean);
      if (valid.length >= 3) {
        g += `<polygon points="${pts.map((p, i) => (p || pt(i, lo)).map((x) => x.toFixed(1)).join(",")).join(" ")}"
          fill="${s.color}" fill-opacity="${series.length > 1 ? 0.12 : 0.18}" stroke="${s.color}" stroke-width="2" stroke-linejoin="round"/>`;
      }
      pts.forEach((p, i) => {
        if (!p) return;
        g += `<circle cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="4.5" fill="${s.color}" stroke="var(--surface)" stroke-width="2"
          data-tip="${esc(`<b>${labels[i]}</b><br>${s.name}: ${fmt(s.values[i])}`)}"/>`;
      });
    });
    return `<svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(opts.aria || "Perfil descriptivo")}">${g}</svg>`;
  }

  /* Tira por competencia: cada círculo es un ítem, el rombo es la media de la competencia. */
  function dotStrip(blocks, opts = {}) {
    const W = 560, rowH = 38, top = 24, left = 168, right = 48, H = top + rowH * blocks.length + 6;
    const x = (v) => left + scaleX(v, 1, 5) * (W - left - right);
    let g = "";
    for (let k = 1; k <= 5; k++) g += `<text x="${x(k)}" y="12" text-anchor="middle" font-weight="700">${k}</text>`;
    blocks.forEach((b, i) => {
      const y = top + i * rowH + rowH / 2;
      g += `<text x="0" y="${y + 4}" font-weight="600" fill="var(--ink)">${esc(b.short)}</text>`;
      g += `<line x1="${x(1)}" x2="${x(5)}" y1="${y}" y2="${y}" class="gridline" stroke-width="2"/>`;
      const counts = {};
      b.items.forEach((it) => {
        if (it.value === null) return;
        counts[it.value] = (counts[it.value] || 0) + 1;
        const off = (counts[it.value] - 1) * 9;
        g += `<circle cx="${x(it.value) + off}" cy="${y}" r="6" fill="var(--surface)" stroke="${opts.color || "var(--ref)"}" stroke-width="2.2"
          data-tip="${esc(`<b>${it.item_id}</b> · ${it.value}<br>${it.text}`)}"/>`;
      });
      const nv = b.items.filter((it) => it.nv || it.omitted).length;
      if (b.score !== null) {
        const cx = x(b.score);
        g += `<rect x="${cx - 6}" y="${y - 6}" width="12" height="12" transform="rotate(45 ${cx} ${y})" fill="var(--mark)" stroke="var(--surface)" stroke-width="1.5"
          data-tip="${esc(`<b>${b.short}</b><br>Media de la competencia: ${fmt(b.score)}`)}"/>`;
        g += `<text x="${W}" y="${y + 4}" text-anchor="end" font-weight="800" fill="var(--ink)">${fmt(b.score)}</text>`;
      } else {
        g += `<text x="${W}" y="${y + 4}" text-anchor="end" fill="var(--muted)">—</text>`;
      }
      if (nv) g += `<text x="0" y="${y + 15}" font-size="9.5" fill="var(--muted)">${nv} sin respuesta válida (NV u omitido)</text>`;
    });
    return `<svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="Respuestas por ítem y media de cada competencia">${g}</svg>`;
  }

  const SEQ = ["var(--seq-0)", "var(--seq-1)", "var(--seq-2)", "var(--seq-3)", "var(--seq-4)", "var(--seq-5)"];
  const inkFor = (i) => (i >= 3 ? "#fff" : "var(--ink)");

  /* Mapa de calor de distribución: personas por media redondeada (1–5) en cada competencia. */
  function heatDistribution(dist) {
    const head = dist.labels.map((l, i) => `<th scope="col" title="${esc(l)}">${i + 1}</th>`).join("");
    const body = dist.rows.map((r) => {
      if (!r.counts) return `<tr><th class="rowh" scope="row">${esc(r.short)}</th><td class="na" colspan="5">Oculto · n = ${r.n}</td></tr>`;
      const max = Math.max(1, ...r.counts);
      return `<tr><th class="rowh" scope="row">${esc(r.short)}</th>${r.counts.map((c, i) => {
        const lvl = c === 0 ? 0 : Math.min(5, 1 + Math.round((c / max) * 4));
        return `<td style="background:${SEQ[lvl]};color:${inkFor(lvl)}" data-tip="${esc(`<b>${r.short}</b><br>${c} de ${r.n} personas con media ≈ ${i + 1} (${dist.labels[i]})`)}">${c}</td>`;
      }).join("")}</tr>`;
    }).join("");
    return `<div class="scroll-x"><table class="heat"><thead><tr><th class="rowh" scope="col">Competencia</th>${head}</tr></thead><tbody>${body}</tbody></table></div>
      <div class="heat-legend">${dist.labels.map((l, i) => `<span><b>${i + 1}</b> ${esc(l)}</span>`).join("")}<span>· más oscuro = más personas</span></div>`;
  }

  /* Tabla de equipos × competencias coloreada en tres tramos (≤3,3 · 3,4–3,7 · ≥3,8), como el panel organizativo. */
  function heatTeams(blocks, rows) {
    const tone = (v) => v === null || v === undefined ? null : v >= 3.8 ? 5 : v >= 3.4 ? 2 : 1;
    const head = blocks.map((b, i) => `<th scope="col">${i + 1}<br>${esc(b)}</th>`).join("");
    const body = rows.map((t) => {
      if (!t.visible) return `<tr><th class="rowh" scope="row">${esc(t.team)}</th><td class="num">${t.n}</td><td class="na" colspan="${blocks.length + 1}">Oculto · por debajo del umbral de anonimato</td></tr>`;
      const cells = t.blocks.map((v, i) => {
        const lv = tone(v);
        return lv === null ? `<td class="na">—</td>` : `<td style="background:${SEQ[lv]};color:${inkFor(lv)}" data-tip="${esc(`<b>${t.team}</b> · ${blocks[i]}<br>Media ${fmt(v)} · n = ${t.n}`)}">${fmt(v, 1)}</td>`;
      }).join("");
      const lg = tone(t.media);
      return `<tr><th class="rowh" scope="row">${esc(t.team)}</th><td class="num">${t.n}</td>${cells}<td style="background:${SEQ[lg ?? 0]};color:${inkFor(lg ?? 0)}">${fmt(t.media, 1)}</td></tr>`;
    }).join("");
    return `<div class="scroll-x"><table class="heat"><thead><tr><th class="rowh" scope="col">Equipo</th><th scope="col">n</th>${head}<th scope="col">Media</th></tr></thead><tbody>${body}</tbody></table></div>
      <div class="heat-legend"><span><i style="background:var(--seq-1)"></i>3,3 o menos</span><span><i style="background:var(--seq-2)"></i>3,4 a 3,7</span><span><i style="background:var(--seq-5)"></i>3,8 o más</span></div>`;
  }

  /* Dispersión media (x) frente a desviación típica (y, invertida: arriba = más acuerdo). Marcas numeradas. */
  function agreement(points) {
    if (!points.length) return "";
    const W = 440, H = 280, L = 44, R = 16, T = 18, B = 38;
    const xs = points.map((p) => p.mean), ys = points.map((p) => p.sd);
    const x0 = Math.floor((Math.min(...xs) - 0.15) * 10) / 10, x1 = Math.ceil((Math.max(...xs) + 0.15) * 10) / 10;
    const y0 = 0, y1 = Math.max(1.2, Math.ceil((Math.max(...ys) + 0.1) * 10) / 10);
    const px = (v) => L + scaleX(v, x0, x1) * (W - L - R);
    const py = (v) => T + scaleX(v, y0, y1) * (H - T - B);
    const xm = points.reduce((a, p) => a + p.mean, 0) / points.length;
    let g = `<line x1="${L}" x2="${W - R}" y1="${py(0.8)}" y2="${py(0.8)}" class="axis" stroke-dasharray="4 4"/>
      <line x1="${px(xm)}" x2="${px(xm)}" y1="${T}" y2="${H - B}" class="axis" stroke-dasharray="4 4"/>`;
    for (let v = Math.ceil(x0 * 2) / 2; v <= x1 + 1e-9; v += 0.5) g += `<text x="${px(v)}" y="${H - B + 16}" text-anchor="middle">${fmt(v, 1)}</text>`;
    for (let v = 0; v <= y1 + 1e-9; v += 0.4) g += `<text x="${L - 8}" y="${py(v) + 4}" text-anchor="end">${fmt(v, 1)}</text>`;
    g += `<text x="${(L + W - R) / 2}" y="${H - 4}" text-anchor="middle">Media de la competencia →</text>`;
    g += `<text x="12" y="${(T + H - B) / 2}" transform="rotate(-90 12 ${(T + H - B) / 2})" text-anchor="middle">← más acuerdo · desviación típica</text>`;
    g += `<text x="${W - R}" y="${T + 10}" text-anchor="end" font-weight="700">Fortaleza compartida</text>`;
    g += `<text x="${W - R}" y="${H - B - 6}" text-anchor="end" font-weight="700">Opiniones divididas</text>`;
    points.forEach((p, i) => {
      g += `<g data-tip="${esc(`<b>${i + 1} · ${p.short}</b><br>Media ${fmt(p.mean)} · desviación ${fmt(p.sd)}`)}">
        <circle cx="${px(p.mean)}" cy="${py(p.sd)}" r="11" fill="var(--mark)" stroke="var(--surface)" stroke-width="2"/>
        <text x="${px(p.mean)}" y="${py(p.sd) + 4}" text-anchor="middle" font-weight="800" style="fill:var(--surface)">${i + 1}</text></g>`;
    });
    const key = points.map((p, i) => `<span><b>${i + 1}</b> ${esc(p.short)}</span>`).join(" · ");
    return `<svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="Media y acuerdo por competencia">${g}</svg><p class="panel-foot">${key}</p>`;
  }

  /* Donut eNPS: promotores, pasivos y detractores. */
  function donut(e) {
    const tot = e.promoters + e.passives + e.detractors;
    const parts = [["Promotores (9–10)", e.promoters, "var(--seq-5)"], ["Pasivos (7–8)", e.passives, "var(--seq-3)"], ["Detractores (0–6)", e.detractors, "var(--axis)"]];
    const R = 62, C = 2 * Math.PI * R;
    let off = 0, g = "";
    parts.forEach(([name, v, color]) => {
      const len = tot ? (v / tot) * C : 0;
      if (len > 0) g += `<circle r="${R}" cx="80" cy="80" fill="none" stroke="${color}" stroke-width="24" stroke-dasharray="${Math.max(0, len - 2)} ${C}"
        stroke-dashoffset="${-off}" transform="rotate(-90 80 80)" data-tip="${esc(`<b>${name}</b><br>${v} de ${tot} · ${pct(v / tot)}`)}"/>`;
      off += len;
    });
    g += `<text x="80" y="88" text-anchor="middle" font-size="26" font-weight="800" style="fill:var(--ink)">${signed(e.score)}</text>`;
    const legend = parts.map(([name, v, color]) => `<span><i style="background:${color}"></i>${name} · ${pct(v / tot)}</span>`).join("");
    return `<div style="display:flex;gap:18px;align-items:center;flex-wrap:wrap"><svg class="chart" viewBox="0 0 160 160" style="max-width:160px" role="img" aria-label="eNPS ${signed(e.score)}">${g}</svg>
      <div class="legend" style="flex-direction:column;gap:6px;margin:0">${legend}</div></div>`;
  }

  /* Línea de evolución: una o dos series (mismo eje 1–5, zoom al rango de datos). */
  function line(series) {
    const periods = [...new Set(series.flatMap((s) => s.points.map((p) => p.periodo)))].sort();
    const vals = series.flatMap((s) => s.points.map((p) => p.mean)).filter((v) => v !== null);
    if (!vals.length) return "";
    const W = 520, H = 220, L = 40, R = 34, T = 14, B = 30;
    const y0 = Math.max(1, Math.floor((Math.min(...vals) - 0.2) * 5) / 5), y1 = Math.min(5, Math.ceil((Math.max(...vals) + 0.2) * 5) / 5);
    const px = (i) => periods.length === 1 ? (L + W - R) / 2 : L + (i / (periods.length - 1)) * (W - L - R);
    const py = (v) => H - B - scaleX(v, y0, y1) * (H - T - B);
    let g = "";
    const step = (y1 - y0) / 4;
    for (let k = 0; k <= 4; k++) { const v = y0 + k * step; g += `<line x1="${L}" x2="${W - R}" y1="${py(v)}" y2="${py(v)}" class="gridline"/><text x="${L - 6}" y="${py(v) + 4}" text-anchor="end">${fmt(v, 1)}</text>`; }
    periods.forEach((p, i) => { g += `<text x="${px(i)}" y="${H - 8}" text-anchor="middle">${esc(p)}</text>`; });
    series.forEach((s) => {
      const pts = s.points.filter((p) => p.mean !== null).map((p) => [px(periods.indexOf(p.periodo)), py(p.mean), p]);
      if (pts.length > 1) g += `<polyline fill="none" stroke="${s.color}" stroke-width="2" points="${pts.map((p) => p[0] + "," + p[1]).join(" ")}"/>`;
      pts.forEach(([x, y, p]) => { g += `<circle cx="${x}" cy="${y}" r="5" fill="${s.color}" stroke="var(--surface)" stroke-width="2" data-tip="${esc(`<b>${s.name}</b> · ${p.periodo}<br>Media ${fmt(p.mean)} · n = ${p.n}`)}"/>`; });
      const last = pts[pts.length - 1];
      if (last && series.length > 1) g += `<text x="${last[0] + 8}" y="${last[1] + 4}" font-weight="700">${fmt(last[2].mean)}</text>`;
    });
    return `<svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="Evolución de la media descriptiva">${g}</svg>`;
  }

  /* Puentes de lectura: dos competencias de cuestionarios distintos sobre el mismo eje 1–5. */
  function dumbbell(bridges, labels) {
    const W = 980, rowH = 50, L = 400, R = 80, T = 24, H = T + rowH * bridges.length;
    const x = (v) => L + scaleX(v, 1, 5) * (W - L - R);
    let g = "";
    for (let k = 1; k <= 5; k++) g += `<line x1="${x(k)}" x2="${x(k)}" y1="${T - 8}" y2="${H - 6}" class="gridline"/><text x="${x(k)}" y="10" text-anchor="middle" font-weight="700">${k}</text>`;
    bridges.forEach((b, i) => {
      const y = T + i * rowH + 20;
      g += `<text x="0" y="${y - 4}" font-weight="700" fill="var(--ink)">${esc(b.a.short)} · ${esc(b.b.short)}</text>`;
      g += `<text x="0" y="${y + 12}" font-size="10.5">${esc(b.prompt)}</text>`;
      const a = b.a.mean, c = b.b.mean;
      if (a !== null && c !== null) g += `<line x1="${x(a)}" x2="${x(c)}" y1="${y}" y2="${y}" stroke="var(--axis)" stroke-width="3"/>`;
      if (a !== null) g += `<circle cx="${x(a)}" cy="${y}" r="7" fill="var(--s1)" stroke="var(--surface)" stroke-width="2" data-tip="${esc(`<b>${b.a.test} · ${b.a.name}</b><br>${fmt(a)}`)}"/>`;
      if (c !== null) g += `<rect x="${x(c) - 6.5}" y="${y - 6.5}" width="13" height="13" rx="2" fill="var(--s2)" stroke="var(--surface)" stroke-width="2" data-tip="${esc(`<b>${b.b.test} · ${b.b.name}</b><br>${fmt(c)}`)}"/>`;
      g += `<text x="${W}" y="${y + 4}" text-anchor="end" font-weight="700">${fmt(a, 1)} · ${fmt(c, 1)}</text>`;
    });
    const legend = `<div class="legend"><span><i style="background:var(--s1);border-radius:50%"></i>${esc(labels[0])}</span><span><i style="background:var(--s2)"></i>${esc(labels[1])}</span></div>`;
    return `<svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="Puentes de lectura entre cuestionarios">${g}</svg>${legend}`;
  }

  window.Charts = { esc, fmt, signed, pct, bars, radar, dotStrip, heatDistribution, heatTeams, agreement, donut, line, dumbbell };
})();

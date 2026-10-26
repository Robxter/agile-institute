/* Centro de mando · Centro de Test (menú 5: Informes y cuadros de mando). Vanilla JS, no build step. */
(() => {
  "use strict";

  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const nf = new Intl.NumberFormat("es-ES");
  const nf1 = new Intl.NumberFormat("es-ES", { minimumFractionDigits: 1, maximumFractionDigits: 1 });
  const nf2 = new Intl.NumberFormat("es-ES", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const pct = new Intl.NumberFormat("es-ES", { style: "percent", maximumFractionDigits: 1 });
  const MONTHS = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"];
  const ROLE_LABEL = { admin: "Administrador Agile Institute", gestor: "Gestor de test", consultor: "Consultor", visor: "Visor" };
  const ROLE_DESC = {
    admin: "Todas las empresas, resultados individuales y exportación administrativa.",
    gestor: "Usuarios, envíos, informes y estados. Sin cuadros de mando.",
    consultor: "Solo las empresas asignadas.",
    visor: "Solo cuadros de mando compartidos y datos agregados.",
  };
  const STATUS = [
    { key: "completed", label: "Realizados", color: "var(--status-good)", icon: "good" },
    { key: "pending", label: "Pendientes", color: "var(--status-warn)", icon: "warn" },
    { key: "expired", label: "Caducados", color: "var(--status-crit)", icon: "crit" },
  ];
  const STATUS_ONE = { completed: ["Realizado", "good"], pending: ["Pendiente", "warn"], expired: ["Caducado", "crit"] };

  const state = { me: null, options: null, data: null, results: null, sort: { key: "sent_at", dir: -1 }, page: 0, showTable: {} };

  const esc = (v) => String(v ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const fmtDate = (iso) => (iso ? `${iso.slice(8, 10)}/${iso.slice(5, 7)}/${iso.slice(0, 4)}` : "—");
  const fmtMonth = (p) => `${MONTHS[+p.slice(5, 7) - 1]} ${p.slice(2, 4)}`;
  const isoDay = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  const cssVar = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

  async function api(path, opts = {}) {
    const res = await fetch(path, { credentials: "same-origin", headers: { "Content-Type": "application/json" }, ...opts });
    if (!res.ok) {
      let msg = `Error ${res.status}`;
      try { msg = (await res.json()).detail || msg; } catch (_) { /* not json */ }
      const err = new Error(typeof msg === "string" ? msg : JSON.stringify(msg));
      err.status = res.status;
      throw err;
    }
    return res;
  }

  /* ------------------------------------------------------------------ session */
  async function boot() {
    try {
      state.me = await (await api("/api/auth/me")).json();
      showApp();
    } catch (e) {
      showLogin();
    }
  }

  async function showLogin() {
    $("#app-view").hidden = true;
    $("#login-view").hidden = false;
    const list = $("#accounts");
    try {
      const accounts = await (await api("/api/auth/demo-accounts")).json();
      list.innerHTML = accounts.map((a) => `
        <li><button type="button" data-email="${esc(a.email)}">
          <strong>${esc(ROLE_LABEL[a.role] || a.role)}</strong>
          <span class="role">${esc(a.name)} · ${esc(ROLE_DESC[a.role] || "")}</span>
        </button></li>`).join("");
    } catch (e) {
      list.innerHTML = "";
      showError($("#login-error"), "El acceso de demostración no está disponible.");
    }
  }

  $("#accounts").addEventListener("click", async (ev) => {
    const btn = ev.target.closest("button[data-email]");
    if (!btn) return;
    try {
      await api("/api/auth/login", { method: "POST", body: JSON.stringify({ email: btn.dataset.email }) });
      state.me = await (await api("/api/auth/me")).json();
      showApp();
    } catch (e) {
      showError($("#login-error"), e.message);
    }
  });

  $("#logout").addEventListener("click", async () => {
    await api("/api/auth/logout", { method: "POST" }).catch(() => {});
    state.me = state.options = state.data = state.results = null;
    showLogin();
  });

  function showError(el, msg) {
    el.textContent = msg;
    el.hidden = !msg;
  }

  async function showApp() {
    $("#login-view").hidden = true;
    $("#app-view").hidden = false;
    $("#user-chip").textContent = `${state.me.name} · ${ROLE_LABEL[state.me.role] || state.me.role}`;
    $("#no-access").hidden = state.me.dashboard_access;
    $("#dashboard").hidden = !state.me.dashboard_access;
    if (!state.me.dashboard_access) return;
    state.options = await (await api("/api/filters")).json();
    fillFilters();
    await load();
  }

  /* ------------------------------------------------------------------ filters */
  function fillFilters() {
    const { companies, tests } = state.options;
    $("#f-company").innerHTML = `<option value="">${companies.length > 1 ? "Todas las autorizadas" : "Todas"}</option>` +
      companies.map((c) => `<option value="${c.id}">${esc(c.name)}</option>`).join("");
    $("#f-test").innerHTML = `<option value="">Todos los test</option>` +
      tests.map((t) => `<option value="${esc(t.test_code)}">${esc(t.name)} · v${esc(t.version)}${t.has_indicators ? "" : " (sin indicadores)"}</option>`).join("");
    const firstScored = tests.find((t) => t.has_indicators);
    if (firstScored) $("#f-test").value = firstScored.test_code;
    $("#f-from").value = "";
    $("#f-to").value = "";
    setPreset("all");
  }

  function currentFilters() {
    const p = new URLSearchParams();
    const c = $("#f-company").value, t = $("#f-test").value, f = $("#f-from").value, to = $("#f-to").value;
    if (c) p.set("company_id", c);
    if (t) p.set("test_code", t);
    if (f) p.set("date_from", f);
    if (to) p.set("date_to", to);
    return p;
  }

  function setPreset(key) {
    $$(".seg button").forEach((b) => b.classList.toggle("on", b.dataset.preset === key));
  }

  $(".seg").addEventListener("click", (ev) => {
    const b = ev.target.closest("button[data-preset]");
    if (!b) return;
    const today = new Date();
    const key = b.dataset.preset;
    if (key === "all") { $("#f-from").value = ""; $("#f-to").value = ""; }
    else if (key === "year") { $("#f-from").value = `${today.getFullYear()}-01-01`; $("#f-to").value = isoDay(today); }
    else { const d = new Date(today); d.setDate(d.getDate() - Number(key)); $("#f-from").value = isoDay(d); $("#f-to").value = isoDay(today); }
    setPreset(key);
    load();
  });

  $("#filters").addEventListener("change", (ev) => {
    if (ev.target.type === "date") setPreset(null);
    load();
  });
  $("#filters").addEventListener("submit", (ev) => ev.preventDefault());

  /* ------------------------------------------------------------------ data */
  let loadSeq = 0;
  async function load() {
    const seq = ++loadSeq;
    const q = currentFilters().toString();
    showError($("#load-error"), "");
    try {
      const [data, results] = await Promise.all([
        api(`/api/dashboard?${q}`).then((r) => r.json()),
        state.me.can_see_individuals ? api(`/api/results?${q}`).then((r) => r.json()) : Promise.resolve(null),
      ]);
      if (seq !== loadSeq) return;
      state.data = data;
      state.results = results;
      state.page = 0;
      render();
    } catch (e) {
      if (e.status === 401) return showLogin();
      showError($("#load-error"), e.message);
    }
  }

  function render() {
    const d = state.data, k = d.kpis;
    const scopeTxt = { admin: "Todas las empresas", consultor: "Empresas asignadas", visor: "Cuadros compartidos · solo agregados" }[d.scope.role] || "";
    $("#scope-line").textContent = `${scopeTxt} · Datos ficticios de demostración · Actualizado ${fmtDate(d.generated_at)} ${d.generated_at.slice(11, 16)}`;

    $("#k-sent").textContent = nf.format(k.sent);
    $("#k-sent-foot").textContent = `${d.filters.Empresa} · ${d.filters.Test}`;
    $("#k-completed").textContent = nf.format(k.completed);
    $("#k-pending").textContent = nf.format(k.pending);
    $("#k-expired").textContent = nf.format(k.expired);
    $("#k-rate").textContent = k.completion_rate == null ? "—" : pct.format(k.completion_rate);
    const bar = $("#k-rate-bar");
    bar.style.width = `${Math.round((k.completion_rate || 0) * 100)}%`;
    bar.classList.toggle("below", (k.completion_rate || 0) < 0.8);
    $("#k-time").textContent = k.avg_response_days == null ? "—" : `${nf1.format(k.avg_response_days)} días`;
    $("#k-time-foot").textContent = k.median_response_days == null ? "Desde el envío hasta la finalización" : `Mediana ${nf1.format(k.median_response_days)} días · desde el envío`;
    $("#k-rem").textContent = nf.format(k.reminders);

    drawAll();
    renderResults();
  }

  function drawAll() {
    if (!state.data) return;
    const d = state.data, r = d.results;
    card("status", () => chartStatus(d.status_by_company), () => tableStatus(d.status_by_company));
    card("activity", () => chartActivity(d.activity), () => tableActivity(d.activity));

    const unavailable = !r.available || r.suppressed;
    const msg = `<div class="empty">${esc(r.reason || "")}</div>`;
    $("#means-sub").textContent = unavailable ? "" :
      `n = ${nf.format(r.n)} resultados · escala ${r.scale.min}-${r.scale.max} · test v${r.test_version} · puntuación v${r.scoring_version}`;
    card("means", () => (unavailable ? msg : chartMeans(r)), () => (unavailable ? msg : tableMeans(r)));
    card("dist", () => (unavailable ? msg : chartDist(r)), () => (unavailable ? msg : tableDist(r)));
    const evoMsg = unavailable ? msg : `<div class="empty">${esc(r.evolution.reason || "")}</div>`;
    const evoOk = !unavailable && r.evolution.available;
    $("#evo-sub").textContent = evoOk
      ? `Media mensual de mediciones comparables (mismo test y versión). Se ocultan los meses con menos de ${r.min_sample} resultados.`
      : "Media mensual de mediciones comparables";
    card("evo", () => (evoOk ? chartEvo(r) : evoMsg), () => (evoOk ? tableEvo(r) : evoMsg));
  }

  function card(id, chartFn, tableFn) {
    const el = $(`#ch-${id}`);
    const btn = $(`#card-${id} [data-toggle-table]`);
    const asTable = !!state.showTable[id];
    btn.textContent = asTable ? "Ver gráfico" : "Ver tabla";
    el.innerHTML = asTable ? tableFn() : chartFn();
    bindTips(el);
  }

  $$("[data-toggle-table]").forEach((b) => b.addEventListener("click", () => {
    const id = b.closest(".chart-card").id.replace("card-", "");
    state.showTable[id] = !state.showTable[id];
    drawAll();
  }));

  let resizeTimer;
  window.addEventListener("resize", () => { clearTimeout(resizeTimer); resizeTimer = setTimeout(drawAll, 120); });
  matchMedia("(prefers-color-scheme: dark)").addEventListener?.("change", drawAll);

  /* ------------------------------------------------------------------ chart primitives */
  const tipStore = new Map();
  let tipSeq = 0;
  function tip(html) { const id = `t${++tipSeq}`; tipStore.set(id, html); return id; }

  function bindTips(root) {
    const svg = $("svg", root);
    if (!svg) return;
    const tt = $("#tooltip");
    svg.addEventListener("pointermove", (ev) => {
      const hit = ev.target.closest("[data-tip]");
      if (!hit) { hide(); return; }
      tt.innerHTML = tipStore.get(hit.dataset.tip) || "";
      tt.hidden = false;
      const pad = 14, w = tt.offsetWidth, h = tt.offsetHeight;
      let x = ev.clientX + pad, y = ev.clientY + pad;
      if (x + w > innerWidth - 8) x = ev.clientX - w - pad;
      if (y + h > innerHeight - 8) y = ev.clientY - h - pad;
      tt.style.left = `${x}px`; tt.style.top = `${y}px`;
      svg.classList.add("hovering");
      $$(".mark.hot", svg).forEach((m) => m.classList.remove("hot"));
      const group = hit.dataset.group;
      if (group) $$(`.mark[data-group="${group}"]`, svg).forEach((m) => m.classList.add("hot"));
      const cross = $(".crosshair", svg);
      if (cross && hit.dataset.x) { cross.setAttribute("x1", hit.dataset.x); cross.setAttribute("x2", hit.dataset.x); cross.style.display = ""; }
    });
    const hide = () => {
      tt.hidden = true;
      svg.classList.remove("hovering");
      $$(".mark.hot", svg).forEach((m) => m.classList.remove("hot"));
      const cross = $(".crosshair", svg);
      if (cross) cross.style.display = "none";
    };
    svg.addEventListener("pointerleave", hide);
  }

  const width = (id) => Math.max(280, $(`#ch-${id}`).clientWidth || 480);

  /** Horizontal bar with a 4px rounded data-end, square at the baseline. */
  function hbarPath(x0, x1, y, h, round = true) {
    const w = x1 - x0;
    if (w <= 0) return "";
    const r = round ? Math.min(4, w, h / 2) : 0;
    return `M${x0},${y}H${x1 - r}Q${x1},${y} ${x1},${y + r}V${y + h - r}Q${x1},${y + h} ${x1 - r},${y + h}H${x0}Z`;
  }
  /** Vertical column with a 4px rounded top. */
  function colPath(x, w, y0, y1) {
    const h = y0 - y1;
    if (h <= 0) return "";
    const r = Math.min(4, h, w / 2);
    return `M${x},${y0}V${y1 + r}Q${x},${y1} ${x + r},${y1}H${x + w - r}Q${x + w},${y1} ${x + w},${y1 + r}V${y0}Z`;
  }
  function niceMax(v) {
    if (v <= 5) return 5;
    const p = 10 ** Math.floor(Math.log10(v));
    for (const m of [1, 2, 2.5, 5, 10]) if (m * p >= v) return m * p;
    return v;
  }
  function ticks(max, n = 4) { const s = max / n; return Array.from({ length: n + 1 }, (_, i) => +(i * s).toFixed(6)); }
  const tipRow = (label, value, color) =>
    `<div class="row"><span>${color ? `<i class="swatch" style="background:${color}"></i>` : ""}${esc(label)}</span><span>${value}</span></div>`;
  const legend = (items) => `<ul class="legend">${items.map((i) =>
    `<li>${i.icon ? `<span class="status-icon ${i.icon}" aria-hidden="true"></span>` : `<i class="swatch" style="background:${i.color}"></i>`}${esc(i.label)}</li>`).join("")}</ul>`;
  const empty = (msg) => `<div class="empty">${esc(msg)}</div>`;
  const truncate = (s, n) => (s.length > n ? `${s.slice(0, n - 1)}…` : s);

  function svgText(widthPx, text, size = 12) { return Math.min(widthPx, text.length * size * 0.56); }

  /* 1-2: Estado por empresa — stacked horizontal bars (status colors + icon legend) */
  function chartStatus(rows) {
    if (!rows.length) return empty("Sin envíos para los filtros elegidos.");
    const W = width("status");
    const labelW = Math.min(150, Math.max(...rows.map((r) => svgText(160, r.company))) + 12);
    const right = 40, top = 6, band = 34, barH = 20;
    const H = top + rows.length * band + 24;
    const max = niceMax(Math.max(...rows.map((r) => r.sent)));
    const x = (v) => labelW + (v / max) * (W - labelW - right);
    let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Estado de los envíos por empresa">`;
    for (const t of ticks(max)) s += `<line class="grid-line" x1="${x(t)}" x2="${x(t)}" y1="${top}" y2="${H - 22}"/><text class="axis-label" x="${x(t)}" y="${H - 6}" text-anchor="middle">${nf.format(t)}</text>`;
    rows.forEach((r, i) => {
      const y = top + i * band + (band - barH) / 2;
      const g = `s${i}`;
      const tid = tip(`<strong>${esc(r.company)}</strong>${STATUS.map((st) => tipRow(st.label, nf.format(r[st.key]), st.color)).join("")}${tipRow("Enviados", nf.format(r.sent))}`);
      s += `<text x="${labelW - 10}" y="${y + barH / 2 + 4}" text-anchor="end">${esc(truncate(r.company, 22))}</text>`;
      let acc = 0;
      const segs = STATUS.filter((st) => r[st.key] > 0);
      segs.forEach((st, j) => {
        const last = j === segs.length - 1;
        const x0 = x(acc), x1 = x(acc + r[st.key]) - (last ? 0 : 2);
        s += `<path class="mark" data-group="${g}" d="${hbarPath(x0, x1, y, barH, last)}" style="fill:${st.color}"/>`;
        acc += r[st.key];
      });
      s += `<text class="value-label" x="${x(r.sent) + 6}" y="${y + barH / 2 + 4}">${nf.format(r.sent)}</text>`;
      s += `<rect class="hit" data-tip="${tid}" data-group="${g}" x="0" y="${top + i * band}" width="${W}" height="${band}"/>`;
    });
    s += `<line class="baseline" x1="${labelW}" x2="${labelW}" y1="${top}" y2="${H - 22}"/></svg>`;
    return legend(STATUS) + s;
  }
  function tableStatus(rows) {
    return `<table class="data chart-table"><thead><tr><th>Empresa</th>${STATUS.map((s) => `<th class="num">${s.label}</th>`).join("")}<th class="num">Enviados</th></tr></thead><tbody>${
      rows.map((r) => `<tr><td>${esc(r.company)}</td>${STATUS.map((s) => `<td class="num">${nf.format(r[s.key])}</td>`).join("")}<td class="num">${nf.format(r.sent)}</td></tr>`).join("")}</tbody></table>`;
  }

  /* Actividad mensual — grouped columns, two series, one axis */
  function chartActivity(rows) {
    if (!rows.length) return empty("Sin actividad en el periodo.");
    const W = width("activity"), H = 230, left = 34, right = 8, top = 10, bottom = 26;
    const max = niceMax(Math.max(...rows.map((r) => Math.max(r.sent, r.completed))));
    const y = (v) => H - bottom - (v / max) * (H - top - bottom);
    const bandW = (W - left - right) / rows.length;
    const colW = Math.max(3, Math.min(20, (bandW - 10) / 2 - 1));
    const series = [{ key: "sent", label: "Enviados", color: "var(--series-1)" }, { key: "completed", label: "Realizados", color: "var(--series-2)" }];
    let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Envíos y test realizados por mes">`;
    for (const t of ticks(max)) s += `<line class="grid-line" x1="${left}" x2="${W - right}" y1="${y(t)}" y2="${y(t)}"/><text class="axis-label" x="${left - 6}" y="${y(t) + 4}" text-anchor="end">${nf.format(t)}</text>`;
    const every = Math.ceil(rows.length / Math.max(1, Math.floor((W - left) / 46)));
    rows.forEach((r, i) => {
      const cx = left + i * bandW + bandW / 2;
      const g = `a${i}`;
      series.forEach((se, j) => {
        const x0 = cx - colW - 1 + j * (colW + 2);
        s += `<path class="mark" data-group="${g}" d="${colPath(x0, colW, y(0), y(r[se.key]))}" style="fill:${se.color}"/>`;
      });
      if (i % every === 0) s += `<text class="axis-label" x="${cx}" y="${H - 8}" text-anchor="middle">${fmtMonth(r.period)}</text>`;
      const tid = tip(`<strong>${fmtMonth(r.period)}</strong>${series.map((se) => tipRow(se.label, nf.format(r[se.key]), se.color)).join("")}`);
      s += `<rect class="hit" data-tip="${tid}" data-group="${g}" x="${left + i * bandW}" y="${top}" width="${bandW}" height="${H - top - bottom}"/>`;
    });
    s += `<line class="baseline" x1="${left}" x2="${W - right}" y1="${y(0)}" y2="${y(0)}"/></svg>`;
    return legend(series) + s;
  }
  function tableActivity(rows) {
    return `<table class="data chart-table"><thead><tr><th>Mes</th><th class="num">Enviados</th><th class="num">Realizados</th></tr></thead><tbody>${
      rows.map((r) => `<tr><td>${fmtMonth(r.period)}</td><td class="num">${nf.format(r.sent)}</td><td class="num">${nf.format(r.completed)}</td></tr>`).join("")}</tbody></table>`;
  }

  /* 6: Resultado medio por indicador — single series horizontal bars on the test scale */
  function chartMeans(r) {
    const rows = r.means;
    const W = width("means");
    const labelW = Math.min(170, Math.max(...rows.map((m) => svgText(180, m.name))) + 12);
    const right = W < 520 ? 92 : 120, top = 6, band = 34, barH = 18;
    const H = top + rows.length * band + 24;
    const lo = r.scale.min, hi = r.scale.max;
    const x = (v) => labelW + ((v - lo) / (hi - lo)) * (W - labelW - right);
    let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Resultado medio por indicador">`;
    for (let t = lo; t <= hi; t += 1) s += `<line class="grid-line" x1="${x(t)}" x2="${x(t)}" y1="${top}" y2="${H - 22}"/><text class="axis-label" x="${x(t)}" y="${H - 6}" text-anchor="middle">${t}</text>`;
    rows.forEach((m, i) => {
      const y = top + i * band + (band - barH) / 2;
      const g = `m${i}`;
      const isGlobal = m.code === "GLOBAL";
      const tid = tip(`<strong>${esc(m.name)}</strong>${tipRow("Media", m.mean == null ? "—" : nf2.format(m.mean))}${tipRow("Nivel", esc(m.level || "—"))}${tipRow("Resultados", nf.format(m.n))}${m.min != null ? tipRow("Rango", `${nf2.format(m.min)} – ${nf2.format(m.max)}`) : ""}`);
      s += `<text x="${labelW - 10}" y="${y + barH / 2 + 4}" text-anchor="end" ${isGlobal ? 'style="font-weight:700;fill:var(--ink)"' : ""}>${esc(truncate(m.name, 26))}</text>`;
      if (m.mean != null) {
        s += `<path class="mark" data-group="${g}" d="${hbarPath(x(lo), x(m.mean), y, barH)}" style="fill:${isGlobal ? "var(--ord-5)" : "var(--series-1)"}"/>`;
        s += `<text class="value-label" x="${x(m.mean) + 6}" y="${y + barH / 2 + 4}">${nf2.format(m.mean)}<tspan class="axis-label" dx="6">${esc(m.level || "")}</tspan></text>`;
      }
      s += `<rect class="hit" data-tip="${tid}" data-group="${g}" x="0" y="${top + i * band}" width="${W}" height="${band}"/>`;
    });
    s += `<line class="baseline" x1="${x(lo)}" x2="${x(lo)}" y1="${top}" y2="${H - 22}"/></svg>`;
    return s;
  }
  function tableMeans(r) {
    return `<table class="data chart-table"><thead><tr><th>Indicador</th><th class="num">Media</th><th>Nivel</th><th class="num">n</th><th class="num">Mín.</th><th class="num">Máx.</th><th class="num">Desv.</th></tr></thead><tbody>${
      r.means.map((m) => `<tr><td>${esc(m.name)}</td><td class="num">${m.mean == null ? "—" : nf2.format(m.mean)}</td><td>${esc(m.level || "—")}</td><td class="num">${nf.format(m.n)}</td><td class="num">${m.min == null ? "—" : nf2.format(m.min)}</td><td class="num">${m.max == null ? "—" : nf2.format(m.max)}</td><td class="num">${m.sd == null ? "—" : nf2.format(m.sd)}</td></tr>`).join("")}</tbody></table>`;
  }

  /* 7: Distribución por niveles — 100% stacked bars, ordinal blue ramp */
  function levelColors(n) {
    const vars = ["--ord-1", "--ord-2", "--ord-3", "--ord-4", "--ord-5", "--ord-6"];
    if (n === 1) return ["var(--ord-3)"];
    return Array.from({ length: n }, (_, k) => `var(${vars[Math.round((k * (vars.length - 1)) / (n - 1))]})`);
  }
  function inkFor(varExpr) {
    const hex = cssVar(varExpr.slice(4, -1));
    const m = /^#?([0-9a-f]{6})$/i.exec(hex);
    if (!m) return "#fff";
    const n = parseInt(m[1], 16);
    const lum = (0.2126 * ((n >> 16) & 255) + 0.7152 * ((n >> 8) & 255) + 0.0722 * (n & 255)) / 255;
    return lum > 0.55 ? "#0b0b0b" : "#ffffff";
  }
  function chartDist(r) {
    const rows = r.distribution;
    const levels = r.levels.map((l) => l.name);
    const colors = levelColors(levels.length);
    const W = width("dist");
    const labelW = Math.min(170, Math.max(...rows.map((d) => svgText(180, d.name))) + 12);
    const right = 8, top = 6, band = 34, barH = 20;
    const H = top + rows.length * band + 24;
    const x = (p) => labelW + p * (W - labelW - right);
    let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Distribución de resultados por nivel">`;
    for (const t of [0, 0.25, 0.5, 0.75, 1]) s += `<line class="grid-line" x1="${x(t)}" x2="${x(t)}" y1="${top}" y2="${H - 22}"/><text class="axis-label" x="${x(t)}" y="${H - 6}" text-anchor="middle">${pct.format(t)}</text>`;
    rows.forEach((d, i) => {
      const y = top + i * band + (band - barH) / 2;
      const g = `d${i}`;
      const isGlobal = d.code === "GLOBAL";
      s += `<text x="${labelW - 10}" y="${y + barH / 2 + 4}" text-anchor="end" ${isGlobal ? 'style="font-weight:700;fill:var(--ink)"' : ""}>${esc(truncate(d.name, 26))}</text>`;
      const tid = tip(`<strong>${esc(d.name)}</strong>${d.counts.map((c, j) => tipRow(c.level, `${nf.format(c.count)} · ${d.total ? pct.format(c.count / d.total) : "—"}`, colors[j])).join("")}${tipRow("Total", nf.format(d.total))}`);
      let acc = 0;
      const segs = d.counts.map((c, j) => ({ ...c, j })).filter((c) => c.count > 0);
      segs.forEach((c, k) => {
        const last = k === segs.length - 1;
        const p0 = acc / d.total, p1 = (acc + c.count) / d.total;
        const x0 = x(p0), x1 = x(p1) - (last ? 0 : 2);
        s += `<path class="mark" data-group="${g}" d="${hbarPath(x0, x1, y, barH, last)}" style="fill:${colors[c.j]}"/>`;
        const label = pct.format(c.count / d.total);
        if (x1 - x0 > label.length * 7 + 10) s += `<text x="${(x0 + x1) / 2}" y="${y + barH / 2 + 4}" text-anchor="middle" style="fill:${inkFor(colors[c.j])};font-size:11px;font-weight:600;pointer-events:none">${label}</text>`;
        acc += c.count;
      });
      s += `<rect class="hit" data-tip="${tid}" data-group="${g}" x="0" y="${top + i * band}" width="${W}" height="${band}"/>`;
    });
    s += `</svg>`;
    return legend(levels.map((l, j) => ({ label: l, color: colors[j] }))) + s;
  }
  function tableDist(r) {
    const levels = r.levels;
    return `<table class="data chart-table"><thead><tr><th>Indicador</th>${levels.map((l) => `<th class="num">${esc(l.name)}<br><small>${nf2.format(l.min)}–${nf2.format(l.max)}</small></th>`).join("")}<th class="num">Total</th></tr></thead><tbody>${
      r.distribution.map((d) => `<tr><td>${esc(d.name)}</td>${d.counts.map((c) => `<td class="num">${nf.format(c.count)}</td>`).join("")}<td class="num">${nf.format(d.total)}</td></tr>`).join("")}</tbody></table>`;
  }

  /* 8: Evolución temporal — single line, crosshair + tooltip, gaps for suppressed months */
  function chartEvo(r) {
    const pts = r.evolution.series;
    const W = width("evo"), H = 240, left = 40, right = 24, top = 14, bottom = 28;
    const vals = pts.filter((p) => !p.suppressed).map((p) => p.mean);
    let lo = Math.max(r.scale.min, Math.floor((Math.min(...vals) - 0.3) * 2) / 2);
    let hi = Math.min(r.scale.max, Math.ceil((Math.max(...vals) + 0.3) * 2) / 2);
    if (hi - lo < 1) { hi = Math.min(r.scale.max, lo + 1); lo = hi - 1; }
    const step = (W - left - right) / Math.max(1, pts.length - 1);
    const x = (i) => left + i * step;
    const y = (v) => H - bottom - ((v - lo) / (hi - lo)) * (H - top - bottom);
    let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Evolución mensual del resultado global">`;
    for (let t = lo; t <= hi + 1e-9; t += 0.5) s += `<line class="grid-line" x1="${left}" x2="${W - right}" y1="${y(t)}" y2="${y(t)}"/><text class="axis-label" x="${left - 6}" y="${y(t) + 4}" text-anchor="end">${nf1.format(t)}</text>`;
    s += `<line class="crosshair grid-line" style="display:none;stroke:var(--axis)" x1="0" x2="0" y1="${top}" y2="${H - bottom}"/>`;
    // Suppressed months carry no value: the line joins the comparable months on either side.
    let d = "";
    pts.forEach((p, i) => {
      if (p.suppressed) return;
      d += `${d ? "L" : "M"}${x(i)},${y(p.mean)}`;
    });
    s += `<path d="${d}" fill="none" style="stroke:var(--series-1)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>`;
    const every = Math.ceil(pts.length / Math.max(1, Math.floor((W - left) / 46)));
    const lastIdx = pts.map((p) => !p.suppressed).lastIndexOf(true);
    pts.forEach((p, i) => {
      if (i % every === 0 || i === pts.length - 1) s += `<text class="axis-label" x="${x(i)}" y="${H - 8}" text-anchor="middle">${fmtMonth(p.period)}</text>`;
      if (!p.suppressed) s += `<circle class="mark" data-group="e${i}" cx="${x(i)}" cy="${y(p.mean)}" r="4.5" style="fill:var(--series-1);stroke:var(--surface)" stroke-width="2"/>`;
      if (i === lastIdx) s += `<text class="value-label" x="${x(i)}" y="${y(p.mean) - 12}" text-anchor="middle">${nf2.format(p.mean)}</text>`;
      const tid = tip(`<strong>${fmtMonth(p.period)}</strong>${p.suppressed ? tipRow("Media global", "Muestra insuficiente") : tipRow("Media global", nf2.format(p.mean), "var(--series-1)")}${tipRow("Resultados", nf.format(p.n))}`);
      s += `<rect class="hit" data-tip="${tid}" data-group="e${i}" data-x="${x(i)}" x="${x(i) - step / 2}" y="${top}" width="${Math.max(step, 12)}" height="${H - top - bottom}"/>`;
    });
    s += `</svg>`;
    return s;
  }
  function tableEvo(r) {
    return `<table class="data chart-table"><thead><tr><th>Mes</th><th class="num">Media global</th><th class="num">Resultados</th></tr></thead><tbody>${
      r.evolution.series.map((p) => `<tr><td>${fmtMonth(p.period)}</td><td class="num">${p.suppressed ? "Muestra insuficiente" : nf2.format(p.mean)}</td><td class="num">${nf.format(p.n)}</td></tr>`).join("")}</tbody></table>`;
  }

  /* ------------------------------------------------------------------ results table */
  const COLS = [
    { key: "person", label: "Persona" },
    { key: "company", label: "Empresa" },
    { key: "position", label: "Posición" },
    { key: "test_name", label: "Test" },
    { key: "status", label: "Estado" },
    { key: "sent_at", label: "Enviado" },
    { key: "completed_at", label: "Realizado" },
    { key: "response_days", label: "Días", num: true },
    { key: "global", label: "Global", num: true },
    { key: "level", label: "Nivel" },
  ];
  const PAGE = 20;

  function renderResults() {
    const panel = $("#results-panel");
    if (!state.results) { panel.hidden = true; return; }
    panel.hidden = false;
    const q = $("#r-search").value.trim().toLowerCase();
    const st = $("#r-status").value;
    let rows = state.results.rows.filter((r) =>
      (!st || r.status === st) && (!q || `${r.person} ${r.company} ${r.position}`.toLowerCase().includes(q)));
    const { key, dir } = state.sort;
    rows = rows.slice().sort((a, b) => {
      const va = a[key], vb = b[key];
      if (va == null && vb == null) return 0;
      if (va == null) return 1;
      if (vb == null) return -1;
      return (va > vb ? 1 : va < vb ? -1 : 0) * dir;
    });
    $("#results-sub").textContent = `${nf.format(rows.length)} envíos · ordenado por ${COLS.find((c) => c.key === key)?.label.toLowerCase()}`;
    const pages = Math.max(1, Math.ceil(rows.length / PAGE));
    state.page = Math.min(state.page, pages - 1);
    const slice = rows.slice(state.page * PAGE, state.page * PAGE + PAGE);
    $("#r-table thead").innerHTML = `<tr>${COLS.map((c) =>
      `<th class="${c.num ? "num" : ""}" aria-sort="${c.key === key ? (dir > 0 ? "ascending" : "descending") : "none"}"><button type="button" data-sort="${c.key}">${c.label}${c.key === key ? (dir > 0 ? " ▲" : " ▼") : ""}</button></th>`).join("")}</tr>`;
    $("#r-table tbody").innerHTML = slice.length ? slice.map((r) => {
      const [label, icon] = STATUS_ONE[r.status];
      return `<tr>
        <td>${esc(r.person)}</td><td>${esc(r.company)}</td><td>${esc(r.position)}</td>
        <td>${esc(r.test_name)} <span class="axis-label">v${esc(r.test_version)}</span></td>
        <td><span class="pill"><span class="status-icon ${icon}" aria-hidden="true"></span>${label}</span></td>
        <td>${fmtDate(r.sent_at)}</td><td>${fmtDate(r.completed_at)}</td>
        <td class="num">${r.response_days == null ? "—" : nf1.format(r.response_days)}</td>
        <td class="num">${r.global == null ? "—" : nf2.format(r.global)}</td>
        <td>${esc(r.level || "—")}</td></tr>`;
    }).join("") : `<tr><td colspan="${COLS.length}" class="muted">Sin envíos para estos filtros.</td></tr>`;
    $("#r-pager").innerHTML = `<span>Página ${state.page + 1} de ${pages}</span><div>
      <button class="btn ghost" type="button" data-page="-1" ${state.page === 0 ? "disabled" : ""}>Anterior</button>
      <button class="btn ghost" type="button" data-page="1" ${state.page >= pages - 1 ? "disabled" : ""}>Siguiente</button></div>`;
  }

  $("#r-table").addEventListener("click", (ev) => {
    const b = ev.target.closest("button[data-sort]");
    if (!b) return;
    const k = b.dataset.sort;
    state.sort = { key: k, dir: state.sort.key === k ? -state.sort.dir : 1 };
    renderResults();
  });
  $("#r-pager").addEventListener("click", (ev) => {
    const b = ev.target.closest("button[data-page]");
    if (!b) return;
    state.page += Number(b.dataset.page);
    renderResults();
  });
  $("#r-search").addEventListener("input", () => { state.page = 0; renderResults(); });
  $("#r-status").addEventListener("change", () => { state.page = 0; renderResults(); });

  /* ------------------------------------------------------------------ export */
  const dlg = $("#export-dialog");
  $("#export-btn").addEventListener("click", () => {
    const items = [
      "Resumen visual con indicadores operativos y gráficos",
      state.me.can_see_individuals ? "Tabla filtrable de resultados individuales autorizados" : "Sin datos individuales (tu rol solo permite agregados)",
      "Indicadores agregados autorizados y distribución por niveles",
      "Hoja de trazabilidad: filtros, versiones y autor de la descarga",
    ];
    $("#export-contents").innerHTML = items.map((i) => `<li>${esc(i)}</li>`).join("");
    $("#admin-export").hidden = !state.me.can_export_items;
    $("#x-items").checked = false;
    $("#x-reason").value = "";
    $("#x-reason-wrap").hidden = true;
    showError($("#export-error"), "");
    dlg.showModal();
  });
  $("#x-items").addEventListener("change", (e) => { $("#x-reason-wrap").hidden = !e.target.checked; });
  $("#export-go").addEventListener("click", async () => {
    const p = currentFilters();
    if ($("#x-items").checked) {
      p.set("include_responses", "true");
      p.set("reason", $("#x-reason").value.trim());
    }
    const btn = $("#export-go");
    btn.disabled = true;
    btn.textContent = "Generando…";
    try {
      const res = await api(`/api/export.xlsx?${p}`);
      const blob = await res.blob();
      const name = /filename="([^"]+)"/.exec(res.headers.get("Content-Disposition") || "")?.[1] || "centro_de_mando.xlsx";
      const a = Object.assign(document.createElement("a"), { href: URL.createObjectURL(blob), download: name });
      document.body.appendChild(a);
      a.click();
      setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
      dlg.close();
    } catch (e) {
      showError($("#export-error"), e.message);
    } finally {
      btn.disabled = false;
      btn.textContent = "Descargar";
    }
  });

  boot();
})();

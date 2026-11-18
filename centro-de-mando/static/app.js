/* Cuadros de mando por dimensión · interfaz sin dependencias. */
(function () {
  "use strict";
  const { esc, fmt, signed, pct } = Charts;
  const $ = (s, el = document) => el.querySelector(s);
  const view = $("#view");

  const NAV = [
    { key: "inicio", label: "Inicio", icon: "home" },
    { key: "persona", label: "Persona", icon: "user" },
    { key: "equipo", label: "Equipo", icon: "users" },
    { key: "liderazgo", label: "Liderazgo", icon: "flag" },
    { key: "organizacion", label: "Organización", icon: "grid" },
    { key: "ia", label: "IA transversal", icon: "spark" },
    { sep: true },
    { key: "persona_ia", label: "Persona + IA", icon: "user", mix: true },
    { key: "liderazgo_ia", label: "Líder + IA", icon: "flag", mix: true },
  ];
  const ICONS = {
    home: '<path d="M3 10.5 10 4l7 6.5V17a1 1 0 0 1-1 1h-3.5v-5h-5v5H4a1 1 0 0 1-1-1z"/>',
    user: '<circle cx="10" cy="7" r="3.2"/><path d="M3.5 17.5c.8-3.2 3.4-5 6.5-5s5.7 1.8 6.5 5"/>',
    users: '<circle cx="7.5" cy="7.5" r="2.8"/><circle cx="14" cy="8.5" r="2.2"/><path d="M2.5 17c.6-2.8 2.6-4.3 5-4.3s4.4 1.5 5 4.3M13 12.6c2.2 0 3.9 1.3 4.5 3.9"/>',
    flag: '<path d="M5 18V3m0 1h9l-2 3.5 2 3.5H5"/>',
    grid: '<rect x="3" y="3" width="6" height="6" rx="1"/><rect x="11" y="3" width="6" height="6" rx="1"/><rect x="3" y="11" width="6" height="6" rx="1"/><rect x="11" y="11" width="6" height="6" rx="1"/>',
    spark: '<path d="M10 2.5 11.8 8.2 17.5 10l-5.7 1.8L10 17.5l-1.8-5.7L2.5 10l5.7-1.8z"/>',
    info: '<circle cx="10" cy="10" r="7.5"/><path d="M10 9v5M10 6.2v.1"/>',
    download: '<path d="M10 3v9m0 0-3.5-3.5M10 12l3.5-3.5M4 15h12"/>',
    layout: '<rect x="3" y="3" width="14" height="14" rx="2"/><path d="M3 8h14M9 8v9"/>',
    eye: '<path d="M2 10s3-5.5 8-5.5S18 10 18 10s-3 5.5-8 5.5S2 10 2 10z"/><circle cx="10" cy="10" r="2.4"/>',
    eyeoff: '<path d="M3 3l14 14M8.3 5c.6-.2 1.1-.3 1.7-.3 5 0 8 5.3 8 5.3a14 14 0 0 1-2.4 3M5.3 6.4A13 13 0 0 0 2 10s3 5.5 8 5.5c1.3 0 2.5-.4 3.5-.9"/>',
  };
  const icon = (n, size = 18) => `<svg viewBox="0 0 20 20" width="${size}" height="${size}" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[n]}</svg>`;

  const state = { me: null, common: { tipo: "DEMO", periodo: "", organizacion: "" }, perDash: {}, data: null };

  async function api(path, opts = {}) {
    const r = await fetch(path, { credentials: "same-origin", headers: { "Content-Type": "application/json" }, ...opts });
    if (!r.ok) {
      let msg = r.statusText;
      try { msg = (await r.json()).detail || msg; } catch (_) { /* sin cuerpo */ }
      const e = new Error(msg); e.status = r.status; throw e;
    }
    return r.headers.get("content-type")?.includes("json") ? r.json() : r;
  }

  /* ---------- tooltips */
  const tip = $("#tooltip");
  function showTip(el, x, y) {
    tip.innerHTML = el.getAttribute("data-tip");
    tip.hidden = false;
    const r = tip.getBoundingClientRect();
    tip.style.left = Math.min(window.innerWidth - r.width - 8, x + 14) + "px";
    tip.style.top = Math.max(8, y - r.height - 12) + "px";
  }
  document.addEventListener("mousemove", (e) => {
    const el = e.target.closest?.("[data-tip]");
    if (el) showTip(el, e.clientX, e.clientY); else tip.hidden = true;
  });
  document.addEventListener("focusin", (e) => {
    const el = e.target.closest?.("[data-tip]");
    if (el) { const r = el.getBoundingClientRect(); showTip(el, r.left + r.width / 2, r.top); }
  });
  document.addEventListener("focusout", () => { tip.hidden = true; });

  /* ---------- login */
  async function showLogin() {
    $("#app-view").hidden = true;
    $("#login-view").hidden = false;
    const list = $("#accounts");
    try {
      const accounts = await api("/api/auth/demo-accounts");
      list.innerHTML = accounts.map((a) => `<li><button type="button" data-email="${esc(a.email)}"><span><strong>${esc(a.name)}</strong><br><span class="muted small">${esc(a.email)}</span></span><span class="role-chip">${esc(a.role_label)}</span></button></li>`).join("");
    } catch (e) {
      list.innerHTML = `<li class="muted">El acceso de demostración está desactivado.</li>`;
    }
    list.onclick = async (e) => {
      const b = e.target.closest("button[data-email]");
      if (!b) return;
      try {
        await api("/api/auth/login", { method: "POST", body: JSON.stringify({ email: b.dataset.email }) });
        // Conserva el cuadro pedido desde la landing (/app#/persona…); route() ya filtra los no autorizados.
        if (!/^#\/\w/.test(location.hash)) location.hash = "#/inicio";
        boot();
      } catch (err) {
        const p = $("#login-error"); p.textContent = err.message; p.hidden = false;
      }
    };
  }

  $("#logout").onclick = async () => {
    await api("/api/auth/logout", { method: "POST" });
    state.me = null; state.perDash = {};
    showLogin();
  };

  /* ---------- navegación */
  function renderNav(active) {
    const allowed = new Set(["inicio", ...state.me.dashboards.map((d) => d.key)]);
    const items = NAV.filter((n) => n.sep || allowed.has(n.key));
    $("#nav").innerHTML = items.map((n) => n.sep ? `<li class="sep" role="separator"></li>` :
      `<li><a href="#/${n.key}" ${n.key === active ? 'aria-current="page"' : ""}>${icon(n.icon)}<span>${n.label}</span>${n.mix ? '<span class="mix">MIX</span>' : ""}</a></li>`).join("");
  }

  function route() {
    const key = (location.hash.replace(/^#\/?/, "") || "inicio").split("?")[0];
    const allowed = state.me.dashboards.map((d) => d.key);
    if (key !== "inicio" && !allowed.includes(key)) { location.hash = "#/inicio"; return; }
    renderNav(key);
    if (key === "inicio") renderOverview(); else renderDashboard(key);
    $("#content").focus({ preventScroll: true });
  }
  window.addEventListener("hashchange", () => state.me && route());

  async function boot() {
    try {
      state.me = await api("/api/auth/me");
    } catch (e) {
      if (e.status === 401) return showLogin();
      throw e;
    }
    $("#login-view").hidden = true;
    $("#app-view").hidden = false;
    $("#user-role").textContent = state.me.role_label;
    $("#user-name").textContent = state.me.name;
    if (!state.me.dashboards.length) {
      renderNav("");
      view.innerHTML = `<div class="panel"><h2>Sin acceso a los cuadros de mando</h2><p class="psub">Tu rol (${esc(state.me.role_label)}) trabaja con usuarios, envíos, informes y estados, pero no con cuadros de mando.</p></div>`;
      return;
    }
    route();
  }

  /* ---------- piezas comunes */
  function query(filters) {
    const q = new URLSearchParams();
    Object.entries(filters).forEach(([k, v]) => { if (v) q.set(k, v); });
    return q.toString();
  }

  const kpi = (k) => {
    let v;
    if (k.fmt === "text") v = esc(k.value ?? "—");
    else if (k.fmt === "int") v = k.value ?? "—";
    else if (k.fmt === "enps") v = signed(k.value);
    else if (k.fmt === "frac8") v = `${k.value ?? 0}/8`;
    else if (k.fmt === "frac16") v = `${k.value ?? 0}/16`;
    else v = fmt(k.value);
    return `<div class="kpi"><div class="v${k.fmt === "text" ? " textv" : ""}">${v}</div><div class="l">${esc(k.label)}</div><div class="s">${esc(k.sub || "")}</div></div>`;
  };

  let uid = 0;
  function panel(title, sub, body, o = {}) {
    const id = "p" + (++uid);
    const toggle = o.table ? `<button class="linkbtn view-toggle" type="button" data-toggle="${id}">Ver tabla</button>` : "";
    return `<section class="panel ${o.cls || ""}" aria-labelledby="${id}-h">
      <div class="panel-head"><div><h2 id="${id}-h">${esc(title)}</h2>${sub ? `<p class="psub">${esc(sub)}</p>` : ""}</div>${toggle}</div>
      <div id="${id}-chart">${body}</div>${o.table ? `<div id="${id}-table" hidden>${o.table}</div>` : ""}
      ${o.foot ? `<p class="panel-foot">${o.foot}</p>` : ""}</section>`;
  }
  view.addEventListener("click", (e) => {
    const b = e.target.closest("[data-toggle]");
    if (!b) return;
    const id = b.dataset.toggle, c = $(`#${id}-chart`), t = $(`#${id}-table`);
    const showTable = t.hidden;
    t.hidden = !showTable; c.hidden = showTable;
    b.textContent = showTable ? "Ver gráfico" : "Ver tabla";
  });

  const table = (head, rows, numCols = []) => `<div class="scroll-x"><table class="data"><thead><tr>${head.map((h, i) => `<th class="${numCols.includes(i) ? "num" : ""}">${esc(h)}</th>`).join("")}</tr></thead>
    <tbody>${rows.map((r) => `<tr>${r.map((c, i) => `<td class="${numCols.includes(i) ? "num" : ""}">${c}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;

  const empty = (title, text) => `<div class="empty"><b>${esc(title)}</b>${esc(text)}</div>`;

  function statusEmpty(p, min) {
    if (p.status === "SIN DATOS") return empty("Sin datos", "No hay capturas válidas para esta selección.");
    if (p.status === "MUESTRA INSUFICIENTE") return empty("Muestra insuficiente", `Hay ${p.n} personas con datos; se necesitan al menos ${min} para publicar resultados de grupo.`);
    return null;
  }

  function blockRows(p, ref) {
    return p.blocks.map((b, i) => ({ label: b.short, value: b.mean, full: b.name, n: b.n,
      ref: ref ? ref[i] : null, note: b.suppressed ? `Oculto · n = ${b.n}` : "Sin datos suficientes" }));
  }
  const blockTable = (p) => table(["Competencia", "Media", "n válido", "Cobertura", "Desv. típica"],
    p.blocks.map((b) => [esc(b.name), fmt(b.mean), b.n, pct(b.coverage), fmt(b.sd)]), [1, 2, 3, 4]);

  function competencesPanel(d, code, o = {}) {
    const p = d.profiles[code];
    const e = statusEmpty(p, d.min_n);
    const color = o.color || "var(--bar)";
    const body = e || Charts.bars(blockRows(p, o.ref), { color, refLabel: o.refLabel }) +
      (o.ref ? `<div class="legend"><span><i style="background:${color}"></i>${esc(o.selfLabel || "Selección")}</span><span><i class="line" style="background:var(--ref)"></i>${esc(o.refLabel)}</span></div>` : "");
    const sub = o.sub || `${p.name} · media descriptiva 1–5 · ${d.individual ? "consulta individual" : `n = ${p.n}`}`;
    return panel(o.title || "Competencias", sub, body, { table: e ? null : blockTable(p), cls: o.cls,
      foot: p.media !== null ? `Media descriptiva (6 de 8 competencias): <b>${fmt(p.media)}</b>` : "La media descriptiva requiere 6 de 8 competencias calculadas." });
  }

  function radarPanel(d, codes, title = "Perfil descriptivo") {
    const ps = codes.map((c) => d.profiles[c]);
    if (ps.some((p) => p.blocks_calculated < 3)) return panel(title, "Sin baremos · escala 1–5", empty("Sin datos suficientes", "El radar necesita al menos tres competencias calculadas."));
    if (codes.length === 1) {
      const p = ps[0];
      return panel(title, "Sin baremos · escala 1–5", Charts.radar(p.blocks.map((b) => b.short), [{ name: p.name, values: p.blocks.map((b) => b.mean), color: "var(--bar)" }]));
    }
    return "";
  }

  function strengthsPanels(p, labels = ["Fortalezas relativas", "Áreas para explorar"]) {
    const list = (arr) => arr.length ? `<ul class="checks">${arr.map((b) => `<li><span><b>${esc(b.name)}.</b> Media ${fmt(b.mean)}${b.test ? ` <span class="tag ${b.test === "T05" ? "s2" : "s1"}">${b.test}</span>` : ""}</span></li>`).join("")}</ul>`
      : empty("Sin lectura relativa", "Se necesitan al menos dos competencias calculadas.");
    return [panel(labels[0], "Donde más destaca hoy el perfil · posición relativa, no diagnóstico", list(p.strengths)),
      panel(labels[1], "Oportunidades de aprendizaje, no carencias", list(p.areas))];
  }

  const PULSE_SETS = {
    condiciones: ["Condiciones de trabajo · pulso", ["F01", "F02", "F03"]],
    bienestar: ["Bienestar · indicadores", ["F05", "F06", "F07", "F08"]],
    seguridad: ["Seguridad psicológica percibida", ["F04"]],
    responsable: ["Mi responsable · percepción recibida", ["L01", "L02", "L03"]],
  };
  function pulseBlock(pulse, set) {
    const [title, ids] = PULSE_SETS[set];
    const cards = ids.map((id) => {
      const it = pulse.items[id];
      const has = it.mean !== null;
      return `<div class="pulse-card" data-tip="${esc(`<b>${id}</b> · ${it.text}`)}" tabindex="0"><div class="t"><span>${esc(it.short)}</span><b>${has ? fmt(it.mean, 1) : "—"}</b></div>
        <div class="track thin"><span class="fill" style="width:${has ? ((it.mean - 1) / 4) * 100 : 0}%"></span></div>
        <div class="n">${has ? `n = ${it.n}` : it.suppressed ? `Oculto · n = ${it.n}` : "Sin datos suficientes"}</div></div>`;
    }).join("");
    return `<div class="section-title">${esc(title)}</div><div class="pulse-grid">${cards}</div>`;
  }
  function pulsePanel(d, sets, title = "Experiencia de trabajo y bienestar", o = {}) {
    const body = sets.map((s) => pulseBlock(d.pulse, s)).join("");
    return panel(title, d.pulse.source, body, { cls: o.cls, foot: "Indicadores independientes: no forman una escala global de Flow ni de bienestar." });
  }
  function enpsPanel(d, title = "eNPS", o = {}) {
    const e = d.pulse.enps;
    const body = e.score === null ? empty("Sin respuestas suficientes de eNPS", `Se necesitan al menos ${e.min_n} respuestas (hay ${e.n}).`) : Charts.donut(e);
    return panel(title, "«¿Qué probabilidad hay de que recomiendes esta organización como lugar para trabajar?» · 0 a 10", body,
      { cls: o.cls || "blue-top", foot: `n = ${e.n}. Indicador independiente: no forma parte de las puntuaciones de los cuestionarios.` });
  }

  function evolutionPanel(d, codes, o = {}) {
    const evs = codes.map((c) => d.evolution[c]);
    const anyAvail = evs.some((e) => e.available);
    const colors = codes.length > 1 ? ["var(--s1)", "var(--s2)"] : ["var(--bar)"];
    let body;
    if (!anyAvail) {
      const base = evs.map((e) => e.series.find((s) => s.periodo === d.filters.periodo)).filter(Boolean)[0];
      body = `<div class="empty"><b>Esta es la línea base${base && base.mean !== null ? ` · ${fmt(base.mean)}` : ""}.</b>${esc(evs[0].reason || "")}</div>`;
    } else {
      body = Charts.line(evs.map((e, i) => ({ name: `${e.test}`, color: colors[i], points: e.series }))) +
        (codes.length > 1 ? `<div class="legend">${evs.map((e, i) => `<span><i style="background:${colors[i]}"></i>${e.test} · ${esc(d.profiles[e.test].name)}</span>`).join("")}</div>` : "");
    }
    const rows = evs.flatMap((e) => e.series.map((s) => [e.test, s.periodo, s.mean === null ? "Muestra insuficiente" : fmt(s.mean), s.n]));
    return panel("Evolución", "Media descriptiva entre mediciones compatibles (misma versión)", body,
      { table: rows.length ? table(["Test", "Periodo", "Media", "n"], rows, [2, 3]) : null, cls: o.cls });
  }

  const CONTROL_LABEL = { OK: "OK", METADATOS: "metadatos incompletos", DUPLICADO: "duplicadas", VALOR_INVALIDO: "valor fuera de escala" };
  function qualityPanel(d, o = {}) {
    const rows = Object.entries(d.quality).map(([code, c]) => {
      const total = Object.values(c).reduce((a, b) => a + b, 0);
      const bad = Object.entries(c).filter(([k]) => k !== "OK").map(([k, n]) => `${n} ${CONTROL_LABEL[k] || k}`).join(" · ");
      return `<li><span><b>${code}</b> · ${c.OK || 0} de ${total} capturas OK${bad ? ` · excluidas: ${esc(bad)}` : ""}</span></li>`;
    }).join("");
    const nv = d.extras.nv && d.individual ? `<li><span>«No observable» en ${d.extras.nv.nv} ítems: se excluyen del cálculo, nunca cuentan como cero.</span></li>` : "";
    return panel(o.title || "Sobre los datos", "Control de calidad de la captura en este corte", `<ul class="checks">${rows}${nv}
      <li><span>Competencia con al menos 2 de 3 ítems válidos; media descriptiva con 6 de 8 competencias.</span></li>
      <li><span>${d.individual ? "Consulta individual: mínimo 1." : `Grupos: mínimo ${d.min_group} personas; por debajo se oculta.`}</span></li></ul>`,
      { foot: "El control no comprueba identidad, acuerdo colectivo ni veracidad.", cls: o.cls });
  }

  function scalePanel(d, code) {
    const labels = d.scale_labels[code] || {};
    const isNum = d.dashboard.tests.find((t) => t.code === code)?.scale_id === "NUM_1_5";
    const rows = Object.entries(labels).map(([k, v]) => `<li><span><span class="tag">${k}</span>${esc(v)}</span></li>`).join("");
    return panel("Cómo leer este resultado", isNum ? "Escala numérica 1–5 · anclajes verbales pendientes en el maestro" : "Frecuencia de cada conducta",
      `<ul class="checks">${rows}<li><span><span class="tag">NV</span>No observable o sin oportunidad de observarlo</span></li></ul>`);
  }

  function itemsPanel(d, code, title = "Mis respuestas por competencia") {
    const blocks = d.extras.items?.[code];
    if (!blocks) return "";
    const rows = blocks.flatMap((b) => b.items.map((it) => [esc(b.short), it.item_id, esc(it.text), it.value ?? (it.nv ? "NV" : "—")]));
    return panel(title, "Cada círculo es un ítem; el rombo es la media de la competencia", Charts.dotStrip(blocks, { color: code === "T05" ? "var(--s2)" : "var(--ref)" }),
      { table: table(["Competencia", "Ítem", "Enunciado", "Respuesta"], rows, [3]) });
  }

  /* ---------- plan editable */
  const PLAZOS = ["30 días", "60 días", "90 días"];
  function planPanel(d, title = "Plan de desarrollo · 90 días") {
    const plan = d.plan;
    const acts = PLAZOS.map((p, i) => plan.actions[i] || { plazo: p, accion: "", responsable: "", fecha_limite: "", estado: "Pendiente", evidencia: "" });
    const saved = plan.updated_at ? `Guardado por ${esc(plan.updated_by)} · ${esc(plan.updated_at.replace("T", " "))}` : "Sin guardar todavía";
    let body;
    if (!plan.editable) {
      const has = plan.objetivo || plan.actions.some((a) => a.accion);
      body = has ? `<div class="plan plan-readonly"><p><b>Objetivo:</b> ${esc(plan.objetivo || "—")}</p><div class="plan-actions">${plan.actions.filter((a) => a.accion).map((a) => `<div class="action"><span class="when">${esc(a.plazo)}</span><span>${esc(a.accion)}</span><span class="muted small">${esc(a.responsable)}${a.fecha_limite ? " · " + esc(a.fecha_limite) : ""}</span><span class="state ${a.estado === "En curso" ? "on" : a.estado === "Hecha" ? "done" : ""}">${esc(a.estado)}</span></div>`).join("")}</div><p class="saved">${saved}</p></div>`
        : empty("Sin plan registrado", "Tu rol puede consultar el plan, pero no editarlo.");
    } else {
      body = `<form class="plan" id="plan-form"><label>Objetivo<textarea name="objetivo" maxlength="500" placeholder="p. ej. practicar la repriorización cuando cambian las necesidades">${esc(plan.objetivo)}</textarea></label>
        <div class="plan-actions">${acts.map((a, i) => `<div class="action"><span class="when">${esc(PLAZOS[i])}</span>
          <input name="accion${i}" maxlength="300" placeholder="Acción o práctica" value="${esc(a.accion)}" aria-label="Acción a ${PLAZOS[i]}">
          <input name="responsable${i}" maxlength="300" placeholder="Responsable" value="${esc(a.responsable)}" aria-label="Responsable a ${PLAZOS[i]}">
          <input name="fecha${i}" type="date" value="${esc(a.fecha_limite)}" aria-label="Fecha objetivo a ${PLAZOS[i]}">
          <select name="estado${i}" aria-label="Estado a ${PLAZOS[i]}">${["Pendiente", "En curso", "Hecha"].map((s) => `<option ${s === a.estado ? "selected" : ""}>${s}</option>`).join("")}</select>
          <input name="evidencia${i}" maxlength="300" placeholder="Evidencia (opcional)" value="${esc(a.evidencia)}" aria-label="Evidencia a ${PLAZOS[i]}">
        </div>`).join("")}</div>
        <div class="row-actions"><span class="saved" id="plan-saved">${saved}</span><button class="btn primary small" type="submit">Guardar plan</button></div></form>`;
    }
    return panel(title, "Registro manual para esta selección · no son recomendaciones automáticas", body, { cls: "accent-top" });
  }
  view.addEventListener("submit", async (e) => {
    if (e.target.id !== "plan-form") return;
    e.preventDefault();
    const fd = new FormData(e.target);
    const body = { objetivo: fd.get("objetivo"), actions: PLAZOS.map((p, i) => ({ plazo: p, accion: fd.get("accion" + i), responsable: fd.get("responsable" + i), fecha_limite: fd.get("fecha" + i), estado: fd.get("estado" + i), evidencia: fd.get("evidencia" + i) })) };
    const key = state.data.key;
    try {
      const plan = await api(`/api/dashboard/${key}/plan?${query(currentFilters(key))}`, { method: "PUT", body: JSON.stringify(body) });
      $("#plan-saved").textContent = `Guardado por ${plan.updated_by} · ${plan.updated_at.replace("T", " ")}`;
    } catch (err) { $("#plan-saved").textContent = "No se pudo guardar: " + err.message; }
  });

  /* ---------- filtros */
  function currentFilters(key) {
    const own = state.perDash[key] || {};
    return { tipo: state.common.tipo, periodo: state.common.periodo, organizacion: state.common.organizacion, equipo: own.equipo || "", persona: own.persona || "" };
  }

  function filtersBar(d) {
    const o = d.options, f = d.filters, locked = new Set(f.locked);
    const sel = (name, label, opts, value, dis) => `<label>${label}<select name="${name}" ${dis ? "disabled" : ""}>${opts.map(([v, t]) => `<option value="${esc(v)}" ${v === value ? "selected" : ""}>${esc(t)}</option>`).join("")}</select></label>`;
    const orgOpts = (o.organizaciones.length > 1 || !locked.has("organizacion") && state.me.role === "admin" ? [["TODOS", "Todas"]] : []).concat(o.organizaciones.map((x) => [x.id, x.name]));
    const teamOpts = [["TODOS", "Todos"]].concat(o.equipos.map((t) => [t.id, `${t.name} · ${t.census} pers.`]));
    const parts = [
      sel("tipo", "Datos", o.tipos.map((t) => [t, t]), f.tipo, false),
      sel("periodo", "Periodo", o.periodos.length ? o.periodos.map((p) => [p, p]) : [["", "Sin periodos"]], f.periodo, false),
      sel("organizacion", "Organización", orgOpts, f.organizacion, locked.has("organizacion")),
    ];
    const individualDash = d.dashboard.key && ["persona", "persona_ia", "liderazgo", "liderazgo_ia"].includes(d.key);
    if (!(individualDash && f.persona !== "TODOS")) parts.push(sel("equipo", "Equipo", teamOpts, f.equipo, locked.has("equipo")));
    if (individualDash && (o.personas.length || locked.has("persona"))) {
      const label = d.key.startsWith("liderazgo") ? "Líder" : "Persona";
      const pOpts = (locked.has("persona") && f.persona !== "TODOS" ? [] : [["TODOS", d.key.startsWith("liderazgo") ? "Todos los líderes (agregado)" : "Todas (agregado)"]])
        .concat(o.personas.map((p) => [p.id, `${p.id} · ${p.team}`]));
      parts.push(sel("persona", label, pOpts, f.persona, locked.has("persona")));
    }
    return `<form class="filters" id="filters" aria-label="Filtros">${parts.join("")}<div class="badges">${f.tipo === "DEMO" ? '<span class="badge demo">Datos DEMO ficticios</span>' : '<span class="badge">Datos REAL</span>'}<span class="badge">Rol: ${esc(state.me.role_label)}</span></div></form>`;
  }

  view.addEventListener("change", (e) => {
    const form = e.target.closest("#filters");
    if (!form) return;
    const key = state.data?.key || "inicio";
    const name = e.target.name, value = e.target.value;
    const own = state.perDash[key] = state.perDash[key] || {};
    if (name === "tipo") { state.common.tipo = value; state.common.periodo = ""; }
    else if (name === "periodo") state.common.periodo = value;
    else if (name === "organizacion") { state.common.organizacion = value; Object.values(state.perDash).forEach((x) => { x.equipo = ""; x.persona = ""; }); }
    else if (name === "equipo") own.equipo = value;
    else if (name === "persona") { own.persona = value; own.equipo = ""; }
    if (key === "inicio") renderOverview(); else renderDashboard(key);
  });

  /* ---------- cuadro */
  async function renderDashboard(key) {
    if (state.editing === key && $("#board")) state.draft = readBoard();
    view.innerHTML = `<p class="loading">Cargando el cuadro…</p>`;
    let d;
    try {
      d = await api(`/api/dashboard/${key}?${query(currentFilters(key))}`);
    } catch (e) {
      view.innerHTML = `<div class="panel"><h2>No se puede mostrar este cuadro</h2><p class="psub">${esc(e.message)}</p></div>`;
      return;
    }
    if (state.editing && state.editing !== key) { state.editing = null; state.draft = null; }
    state.data = d;
    state.common.periodo = d.filters.periodo;
    state.common.organizacion = d.filters.organizacion;
    const editing = state.editing === key;
    const tests = d.dashboard.tests;
    const persona = d.filters.persona !== "TODOS" ? `Persona ${d.filters.persona}` : "Agregado";
    const n = Object.values(d.profiles).map((p) => `${p.test} n = ${p.n}`).join(" · ");
    const meta = `<div class="meta"><span>${tests.map((t) => `${t.code} ${esc(t.name)} · ${esc(t.version)}`).join(" | ")}</span><span>Periodo: ${esc(d.filters.periodo || "—")}</span><span>${esc(persona)}</span><span>${n}</span><span>Mínimo por grupo: ${d.min_group}</span></div>`;
    const custom = !!d.layout;
    const head = `<div class="head"><div><span class="eyebrow">Cuadro de mando · ${esc(d.dashboard.label)}</span><h1>${esc(d.dashboard.title)}</h1><p class="sub">${esc(d.dashboard.subtitle)}</p></div>
      <div class="head-actions">${editing ? "" : `${custom ? `<button class="btn ghost" type="button" data-layout="reset">Distribución estándar</button>` : ""}
        <button class="btn ghost" type="button" data-layout="edit">${icon("layout", 16)} Personalizar</button>`}
        <button class="btn primary" type="button" id="export-btn">${icon("download", 16)} Descargar Excel</button></div></div>`;
    const notice = `<div class="notice">${icon("info")}<span>${esc(d.notice)}</span></div>`;
    const toolbar = editing ? `<div class="edit-bar" role="region" aria-label="Edición de la distribución">
        <span>${icon("layout", 18)}<span><b>Modo edición.</b> Arrastra cada panel por su asa ⠿ para moverlo, cambia su ancho con − y +, u ocúltalo con el ojo. Con el teclado, usa las flechas sobre el asa.<span class="mobile-note"> En el móvil los paneles ocupan siempre el ancho completo; los anchos se aplican en pantallas grandes.</span></span></span>
        <span class="edit-actions"><button class="btn ghost small" type="button" data-layout="standard">Volver a la distribución estándar</button>
        <button class="btn ghost small" type="button" data-layout="cancel">Cancelar</button>
        <button class="btn accent small" type="button" data-layout="save">Guardar distribución</button></span></div>` : "";
    const tiles = d.kpis.map((k, i) => tile(`kpi-${i + 1}`, 3, kpi(k), true)).concat(LAYOUTS[key](d));
    stdOrder = tiles.map((t) => t.id);
    const layout = editing ? state.draft : d.layout;
    view.innerHTML = head + meta + filtersBar(d) + notice + toolbar + board(tiles, layout, editing) + `<p class="footer">${esc(d.disclaimer)}</p>`;
    $("#export-btn").onclick = openExport;
  }

  /* Ficha del tablero: identificador estable + ancho estándar (columnas de 12). */
  const tile = (id, span, html, isKpi = false) => ({ id, span, html, kpi: isKpi });
  const SPANS = [3, 4, 6, 8, 9, 12];
  const SPAN_LABEL = { 3: "¼", 4: "⅓", 6: "½", 8: "⅔", 9: "¾", 12: "completo" };

  function board(tiles, layout, editing) {
    let ordered = tiles;
    if (layout && layout.order?.length) {
      const pos = new Map(layout.order.map((id, i) => [id, i]));
      // Los paneles que no estaban en la distribución guardada conservan su sitio relativo tras el último conocido.
      let last = -1;
      const keyed = tiles.map((t, i) => {
        if (pos.has(t.id)) last = pos.get(t.id);
        return { t, k: pos.has(t.id) ? pos.get(t.id) : last + 0.001 * (i + 1) };
      });
      ordered = keyed.sort((a, b) => a.k - b.k).map((x) => x.t);
    }
    const hidden = new Set(layout?.hidden || []);
    const spans = layout?.spans || {};
    return `<div class="board${editing ? " editing" : ""}" id="board">${ordered.map((t) => {
      const span = SPANS.includes(spans[t.id]) ? spans[t.id] : t.span;
      const isHidden = hidden.has(t.id);
      if (isHidden && !editing) return `<div class="tile" data-id="${t.id}" data-span="${span}" data-std="${t.span}" data-hidden="1" hidden></div>`;
      const tools = editing ? `<div class="tile-tools">
          <button class="tile-handle" type="button" aria-label="Mover panel (flechas para cambiar de posición)" title="Arrastrar para mover">⠿</button>
          <span class="tile-width"><button type="button" data-w="-1" aria-label="Estrechar panel">−</button><span class="w-label">${SPAN_LABEL[span]}</span><button type="button" data-w="1" aria-label="Ensanchar panel">+</button></span>
          <button type="button" class="tile-eye" data-eye aria-label="${isHidden ? "Mostrar panel" : "Ocultar panel"}" aria-pressed="${isHidden}" title="${isHidden ? "Mostrar" : "Ocultar"}">${icon(isHidden ? "eyeoff" : "eye", 16)}</button></div>` : "";
      return `<div class="tile${t.kpi ? " tile-kpi" : ""}${isHidden ? " is-hidden" : ""}" data-id="${t.id}" data-span="${span}" data-std="${t.span}"${isHidden ? ' data-hidden="1"' : ""} style="--span:${span}">${tools}${t.html}</div>`;
    }).join("")}</div>`;
  }

  function readBoard() {
    const tiles = [...document.querySelectorAll("#board > .tile")];
    const spans = {};
    tiles.forEach((t) => { if (+t.dataset.span !== +t.dataset.std) spans[t.dataset.id] = +t.dataset.span; });
    return { order: tiles.map((t) => t.dataset.id), spans, hidden: tiles.filter((t) => t.dataset.hidden === "1").map((t) => t.dataset.id) };
  }

  /* Botones de la distribución */
  view.addEventListener("click", async (e) => {
    const b = e.target.closest("[data-layout]");
    if (!b) return;
    const key = state.data.key, action = b.dataset.layout;
    try {
      if (action === "edit") { state.editing = key; state.draft = state.data.layout; }
      else if (action === "cancel") { state.editing = null; state.draft = null; }
      else if (action === "standard") { state.draft = null; }
      else if (action === "save") {
        const layout = readBoard();
        const isStandard = !Object.keys(layout.spans).length && !layout.hidden.length &&
          layout.order.join() === [...document.querySelectorAll("#board > .tile")].map((t) => t.dataset.id).sort((a, b) => stdIndex(a) - stdIndex(b)).join();
        if (isStandard) await api(`/api/layout/${key}`, { method: "DELETE" });
        else await api(`/api/layout/${key}`, { method: "PUT", body: JSON.stringify(layout) });
        state.editing = null; state.draft = null;
      } else if (action === "reset") {
        if (!confirm("¿Volver a la distribución estándar de este cuadro? Se perderá tu distribución personalizada.")) return;
        await api(`/api/layout/${key}`, { method: "DELETE" });
      }
    } catch (err) { alert("No se pudo guardar la distribución: " + err.message); return; }
    if (action === "standard") { renderStandardDraft(); return; }
    renderDashboard(key);
  });

  let stdOrder = [];
  function stdIndex(id) { const i = stdOrder.indexOf(id); return i < 0 ? 999 : i; }
  function renderStandardDraft() {
    // Vuelve a pintar en modo edición con la distribución estándar, sin guardar todavía.
    state.draft = null;
    const boardEl = $("#board");
    const tiles = [...boardEl.children];
    tiles.sort((a, b) => stdIndex(a.dataset.id) - stdIndex(b.dataset.id)).forEach((t) => {
      boardEl.appendChild(t);
      setSpan(t, +t.dataset.std);
      setHidden(t, false);
    });
  }

  function setSpan(t, span) {
    t.dataset.span = span;
    t.style.setProperty("--span", span);
    const l = t.querySelector(".w-label");
    if (l) l.textContent = SPAN_LABEL[span];
  }
  function setHidden(t, hide) {
    if (hide) t.dataset.hidden = "1"; else delete t.dataset.hidden;
    t.classList.toggle("is-hidden", hide);
    const eye = t.querySelector("[data-eye]");
    if (eye) {
      eye.innerHTML = icon(hide ? "eyeoff" : "eye", 16);
      eye.setAttribute("aria-pressed", hide);
      eye.setAttribute("aria-label", hide ? "Mostrar panel" : "Ocultar panel");
    }
  }

  /* Ancho y visibilidad */
  view.addEventListener("click", (e) => {
    const t = e.target.closest("#board.editing > .tile");
    if (!t) return;
    const w = e.target.closest("[data-w]");
    if (w) {
      const i = SPANS.indexOf(+t.dataset.span);
      setSpan(t, SPANS[Math.max(0, Math.min(SPANS.length - 1, i + +w.dataset.w))]);
    } else if (e.target.closest("[data-eye]")) {
      setHidden(t, t.dataset.hidden !== "1");
    }
  });

  /* Mover con el teclado: flechas sobre el asa */
  view.addEventListener("keydown", (e) => {
    const h = e.target.closest(".tile-handle");
    if (!h) return;
    const t = h.closest(".tile");
    if (["ArrowLeft", "ArrowUp"].includes(e.key) && t.previousElementSibling) t.parentNode.insertBefore(t, t.previousElementSibling);
    else if (["ArrowRight", "ArrowDown"].includes(e.key) && t.nextElementSibling) t.parentNode.insertBefore(t.nextElementSibling, t);
    else return;
    e.preventDefault();
    h.focus();
  });

  /* Arrastrar con ratón o pantalla táctil (eventos de puntero) */
  let drag = null;
  view.addEventListener("pointerdown", (e) => {
    const h = e.target.closest("#board.editing .tile-handle");
    if (!h || e.button > 0) return;
    e.preventDefault();
    const t = h.closest(".tile");
    h.setPointerCapture(e.pointerId);
    drag = { t, h, id: e.pointerId };
    t.classList.add("dragging");
    document.body.classList.add("is-dragging");
  });
  view.addEventListener("pointermove", (e) => {
    if (!drag || e.pointerId !== drag.id) return;
    if (e.clientY < 70) window.scrollBy(0, -14); else if (e.clientY > window.innerHeight - 70) window.scrollBy(0, 14);
    const over = document.elementFromPoint(e.clientX, e.clientY)?.closest("#board > .tile");
    if (!over || over === drag.t) return;
    const r = over.getBoundingClientRect();
    const full = r.width > over.parentNode.getBoundingClientRect().width * 0.9;
    const before = full ? e.clientY < r.top + r.height / 2 : e.clientX < r.left + r.width / 2;
    over.parentNode.insertBefore(drag.t, before ? over : over.nextElementSibling);
  });
  const endDrag = (e) => {
    if (!drag || e.pointerId !== drag.id) return;
    drag.t.classList.remove("dragging");
    document.body.classList.remove("is-dragging");
    drag = null;
  };
  view.addEventListener("pointerup", endDrag);
  view.addEventListener("pointercancel", endDrag);

  /* Composición estándar de cada cuadro: fichas con identificador estable y ancho en columnas de 12. */
  const LAYOUTS = {
    persona(d) {
      const p = d.profiles.T01;
      const [fort, areas] = strengthsPanels(p);
      return [
        tile("competencias", 4, competencesPanel(d, "T01", { title: d.individual ? "Mis competencias · 1–5" : "Competencias · 1–5" })),
        tile("radar", 4, radarPanel(d, ["T01"])),
        tile("bienestar", 4, pulsePanel(d, ["bienestar", "seguridad"])),
        tile("fortalezas", 6, fort), tile("areas", 6, areas),
        tile("plan", 12, planPanel(d)),
        ...(d.extras.items ? [tile("respuestas", 8, itemsPanel(d, "T01")), tile("escala", 4, scalePanel(d, "T01"))] : []),
        tile("condiciones", 4, pulsePanel(d, ["condiciones"], "Condiciones de trabajo")),
        tile("evolucion", 4, evolutionPanel(d, ["T01"])),
        tile("calidad", 4, qualityPanel(d)),
      ];
    },
    equipo(d) {
      const p = d.profiles.T02, x = d.extras;
      const dist = statusEmpty(p, d.min_n) || Charts.heatDistribution(x.distribution);
      const agree = statusEmpty(p, d.min_n) || (x.agreement.length ? Charts.agreement(x.agreement) : empty("Sin datos suficientes", ""));
      const part = x.participation;
      const dots = Array.from({ length: Math.min(part.census, 40) }, (_, i) => `<span style="display:inline-block;width:20px;height:20px;border-radius:50%;margin:3px;background:${i < part.responded ? "var(--mark)" : "var(--bar-track)"}"></span>`).join("");
      const [fort, areas] = strengthsPanels(p, ["Fortalezas compartidas", "Áreas para explorar"]);
      return [
        tile("acuerdo", 4, panel("Media y acuerdo del equipo", "Cada punto es una competencia · más arriba, más acuerdo entre las personas", agree, { foot: "Eje horizontal: media de la competencia. Eje vertical: desviación típica entre personas (referencia en 0,8)." })),
        tile("distribucion", 4, panel("Cómo responde el equipo", "Personas según la media de sus 3 ítems, redondeada · mapa de calor", dist, { foot: `Cada fila se publica solo si la competencia reúne al menos ${d.min_group} personas.` })),
        tile("enps", 4, enpsPanel(d, "eNPS del equipo")),
        tile("competencias", 8, competencesPanel(d, "T02", { title: "Las 8 competencias del equipo", ref: x.reference?.blocks, refLabel: x.reference ? `${x.reference.label} (n = ${x.reference.n})` : null, selfLabel: "Equipo" })),
        tile("participacion", 4, panel("Participación", "Personas con datos válidos en este corte", `<div aria-hidden="true">${dots}</div><p style="margin-top:10px"><b>${part.responded} de ${part.census}</b> personas · umbral de anonimato: ${part.min_group}</p>`)),
        tile("fortalezas", 4, fort), tile("areas", 4, areas),
        tile("seguridad", 4, pulsePanel(d, ["seguridad"], "Seguridad psicológica")),
        tile("plan", 12, planPanel(d, "Acciones del equipo")),
        tile("bienestar", 4, pulsePanel(d, ["bienestar"])),
        tile("evolucion", 4, evolutionPanel(d, ["T02"])),
        tile("calidad", 4, qualityPanel(d)),
      ];
    },
    liderazgo(d) {
      const p = d.profiles.T03, x = d.extras;
      const received = Charts.bars(x.received.map((r) => ({ label: r.short, full: r.text, value: r.mean, n: r.n, note: r.suppressed ? `Oculto · n = ${r.n} (umbral ${d.min_group})` : "Sin datos suficientes" })));
      const sources = `<div class="mini-grid">${x.sources.map((s) => `<div class="card-soft"><b>${esc(s.label)} · ${esc(s.value)}</b><p class="muted small" style="margin-top:4px">${esc(s.text)}</p></div>`).join("")}</div>`;
      let middle;
      if (x.conversations) {
        const c = x.conversations;
        middle = [
          tile("conversaciones", 6, panel("Conversaciones para abrir", `Conductas de «${c.explore_block || "—"}» para contrastar con tu equipo`, c.explore.length ? `<ul class="checks">${c.explore.map((t) => `<li><span>¿Cómo lo vive el equipo? «${esc(t)}»</span></li>`).join("")}</ul>` : empty("Sin lectura relativa", ""))),
          tile("practicas", 6, panel("Lo que más practicas", `Conductas de «${c.practice_block || "—"}»`, c.practice.length ? `<ul class="checks">${c.practice.map((t) => `<li><span>${esc(t)}</span></li>`).join("")}</ul>` : empty("Sin lectura relativa", ""))),
        ];
      } else {
        const [fort, areas] = strengthsPanels(p);
        middle = [tile("fortalezas", 6, fort), tile("areas", 6, areas)];
      }
      return [
        tile("competencias", 6, competencesPanel(d, "T03", { title: d.individual ? "Mi mirada · autopercepción" : "Autopercepción de los líderes" })),
        tile("percepcion", 6, panel(d.individual ? "Lo que percibe mi equipo" : "Percepción del responsable", "Pulso L01–L03 · preguntas distintas de T03: no se calcula brecha", received, { foot: `Se publica solo con ${d.min_group} o más personas informantes.` })),
        ...middle,
        tile("bienestar", 4, pulsePanel(d, ["bienestar"], d.individual ? "Relación descriptiva con el equipo" : "Experiencia laboral")),
        tile("fuentes", 8, panel("Fuentes y muestra", "Cada resultado indica qué fuentes intervienen y cuántas respuestas lo sustentan", sources)),
        tile("plan", 12, planPanel(d, d.individual ? "Mi plan de liderazgo" : "Plan de liderazgo")),
        tile("condiciones", 4, pulsePanel(d, ["seguridad", "condiciones"], "Condiciones y seguridad")),
        tile("evolucion", 4, evolutionPanel(d, ["T03"])),
        tile("calidad", 4, qualityPanel(d)),
      ];
    },
    organizacion(d) {
      const p = d.profiles.T04, x = d.extras;
      const cards = statusEmpty(p, d.min_n) || `<div class="mini-grid">${p.blocks.map((b) => `<div class="card-soft" data-tip="${esc(`<b>${b.name}</b><br>Media ${fmt(b.mean)} · n = ${b.n}`)}" tabindex="0"><div style="display:flex;justify-content:space-between;gap:8px"><span class="small"><b>Competencia ${b.idx}</b></span><b style="font-size:20px">${fmt(b.mean, 1)}</b></div><p style="margin:6px 0 8px;font-weight:700">${esc(b.name)}</p><div class="track thin"><span class="fill" style="width:${b.mean ? ((b.mean - 1) / 4) * 100 : 0}%"></span></div><p class="small muted" style="margin-top:6px">n = ${b.n}</p></div>`).join("")}</div>`;
      const five = Charts.bars(x.five_profiles.map((f) => ({ label: f.name, sub: `${f.test} · n = ${f.n_summary} de ${f.n_data}`, value: f.media, n: f.n_summary })));
      const prio = x.priorities.length ? `<ul class="checks">${x.priorities.map((b) => `<li><span><b>${esc(b.name)}</b> · media ${fmt(b.mean)}</span></li>`).join("")}</ul>` : empty("Sin datos suficientes", "");
      return [
        tile("competencias", 12, panel("Ocho competencias clave", "Lectura ejecutiva · T04 Organización · cada competencia con una sola asignación", cards, { table: blockTable(p) })),
        tile("enps", 6, enpsPanel(d)),
        tile("evolucion", 6, evolutionPanel(d, ["T04"])),
        tile("equipos", 12, panel("Resultados por equipo", `Media de cada competencia T04 por equipo · solo equipos con ${d.min_group} respuestas o más`, Charts.heatTeams(x.teams.blocks, x.teams.rows))),
        tile("perfiles", 6, panel("Visión conjunta de los cinco perfiles", "Cada ámbito con su propio n · sin índice global", five, { foot: "No existe media conjunta de los cinco perfiles ni puntuación de madurez." })),
        tile("prioridades", 6, panel("Prioridades organizativas", "Las tres competencias T04 con menor media", prio, { cls: "accent-top" })),
        tile("plan", 12, planPanel(d, "Plan de acción organizativo")),
        tile("pulso", 6, pulsePanel(d, ["condiciones", "bienestar", "seguridad"])),
        tile("calidad", 6, qualityPanel(d)),
      ];
    },
    ia(d) {
      const p = d.profiles.T05, x = d.extras;
      const teams = x.teams.rows.length ? Charts.bars(x.teams.rows.map((t) => ({ label: t.team, sub: `n = ${t.n}`, value: t.media, n: t.n, note: t.visible ? "Sin resumen suficiente" : `Oculto · n = ${t.n}` })))
        : empty("Sin datos", "");
      const beh = (arr) => arr.map((b) => `<li><span><span class="tag">${esc(b.item_id)}</span>${esc(b.text)} <b>${fmt(b.mean, 1)}</b></span></li>`).join("");
      const behaviours = x.behaviours.top.length ? `<div class="section-title">Más frecuentes</div><ul class="checks">${beh(x.behaviours.top)}</ul><div class="section-title">Menos frecuentes</div><ul class="checks">${beh(x.behaviours.bottom)}</ul>`
        : empty("Sin datos suficientes", `Cada ítem necesita al menos ${d.min_group} respuestas.`);
      const [fort, areas] = strengthsPanels(p);
      return [
        tile("competencias", 6, competencesPanel(d, "T05", { title: "Competencias de IA", cls: "blue-top" })),
        tile("equipos", 6, panel("IA por equipo", `Media descriptiva T05 por equipo · solo grupos con ${d.min_group} respuestas o más`, teams)),
        tile("conductas", 6, panel("Conductas a observar", "Ítems del cuestionario con mayor y menor frecuencia media", behaviours)),
        tile("radar", 6, radarPanel(d, ["T05"], "Perfil de IA")),
        tile("fortalezas", 6, fort), tile("areas", 6, areas),
        tile("plan", 12, planPanel(d, "Buenas prácticas para los equipos")),
        tile("bienestar", 4, pulsePanel(d, ["bienestar", "seguridad"])),
        tile("evolucion", 4, evolutionPanel(d, ["T05"])),
        tile("calidad", 4, qualityPanel(d)),
      ];
    },
    persona_ia(d) { return mixedLayout(d, "T01", "Agilidad personal", "Colaboración humano-IA"); },
    liderazgo_ia(d) { return mixedLayout(d, "T03", "Liderazgo", "IA"); },
  };

  function mixedLayout(d, a, labelA, labelB) {
    const x = d.extras, pa = d.profiles[a], pb = d.profiles.T05;
    const ref = x.reference;
    const bridges = pa.blocks_calculated && pb.blocks_calculated ? Charts.dumbbell(x.bridges, [`${a} · ${labelA}`, `T05 · ${labelB}`])
      : empty("Sin datos suficientes", "Los puentes necesitan los dos cuestionarios calculados.");
    const bridgeRows = x.bridges.map((b) => [esc(b.a.name), fmt(b.a.mean), esc(b.b.name), fmt(b.b.mean), esc(b.prompt)]);
    const combined = x.combined || {};
    const leader = d.key === "liderazgo_ia";
    const t05Title = leader ? (d.individual ? "T05 · Mi IA frente a la de mi equipo" : "T05 · IA de los líderes frente a sus equipos") : "T05 · Colaboración humano-IA";
    const [fort, areas] = strengthsPanels({ strengths: combined.strengths || [], areas: combined.areas || [] }, ["Fortalezas combinadas", "Áreas combinadas para explorar"]);
    const first = leader
      ? panel(d.individual ? "Lo que percibe mi equipo" : "Percepción del responsable", "Pulso L01–L03 · mínimo 5 informantes",
        Charts.bars(x.received.map((r) => ({ label: r.short, full: r.text, value: r.mean, n: r.n, note: r.suppressed ? `Oculto · n = ${r.n}` : "Sin datos suficientes" }))))
      : pulsePanel(d, ["bienestar"]);
    return [
      tile("competencias-a", 6, competencesPanel(d, a, { title: `${a} · ${labelA}`, color: "var(--s1)", cls: "blue-top" })),
      tile("competencias-ia", 6, competencesPanel(d, "T05", { title: t05Title, color: "var(--s2)", ref: ref?.blocks, refLabel: ref ? `${ref.label} (n = ${ref.n})` : null, selfLabel: leader ? (d.individual ? "Mi IA" : "Líderes") : "T05", cls: "accent-top" })),
      tile("puentes", 12, panel(leader ? "Liderar con IA · puentes de lectura" : "Agilidad aumentada · puentes de lectura", "Dos competencias relacionadas, cada una medida en su cuestionario · propuesta para conversar, no una relación validada", bridges, { table: table(["Competencia A", "Media", "Competencia T05", "Media", "Para conversar"], bridgeRows, [1, 3]) })),
      tile("fortalezas", 6, fort), tile("areas", 6, areas),
      tile("plan", 12, planPanel(d, leader ? "Mi plan · liderar con IA" : "Mi plan · agilidad aumentada")),
      ...(x.items ? [tile("respuestas-a", 6, itemsPanel(d, a, `Mis respuestas · ${a}`)), tile("respuestas-ia", 6, itemsPanel(d, "T05", "Mis respuestas · T05"))] : []),
      tile(leader ? "percepcion" : "bienestar", 4, first),
      tile("evolucion", 4, evolutionPanel(d, [a, "T05"])),
      tile("calidad", 4, qualityPanel(d)),
      tile(leader ? "bienestar" : "condiciones", 6, leader ? pulsePanel(d, ["bienestar", "seguridad"], d.individual ? "Relación descriptiva con el equipo" : "Experiencia laboral") : pulsePanel(d, ["condiciones", "seguridad"], "Condiciones de trabajo")),
      tile("escala", 6, scalePanel(d, "T05")),
    ];
  }

  /* ---------- inicio */
  async function renderOverview() {
    view.innerHTML = `<p class="loading">Cargando…</p>`;
    state.data = null;
    let o;
    try { o = await api(`/api/overview?${query({ tipo: state.common.tipo, periodo: state.common.periodo, organizacion: state.common.organizacion })}`); }
    catch (e) { view.innerHTML = `<div class="panel"><h2>Error</h2><p class="psub">${esc(e.message)}</p></div>`; return; }
    state.common.periodo = o.filters.periodo || "";
    const cards = o.cards.map((c) => `<a class="ov-card ${c.tests.length > 1 ? "mixed" : ""}" href="#/${c.key}"><span class="eyebrow" style="align-self:flex-start;margin:0">${esc(c.label)}${c.tests.length > 1 ? " · mixto" : ""}</span><h3>${esc(c.title)}</h3><p class="muted small">${esc(c.subtitle)}</p>
      ${c.tests.map((t) => `<div class="row"><span>${t.test} · ${esc(t.name)}${c.individual ? " · tu resultado" : ""}</span><b>${t.media !== null ? fmt(t.media) : "—"} · n = ${t.n}</b></div>`).join("")}</a>`).join("");
    const admin = state.me.can_import ? `<div class="grid g2" style="margin-top:16px">${panel("Importar capturas", "Libro .xlsx con hojas Datos_T01…Datos_T05 y/o Datos_PULSO (formato del libro de diseño)",
      `<form id="import-form"><input type="file" name="file" accept=".xlsx" required> <button class="btn primary small" type="submit">Importar</button></form><p class="panel-foot" id="import-result">Una fila con un evaluacion_id existente sustituye a la anterior. Se recalcula el control de calidad.</p>`)}
      ${panel("Auditoría", "Accesos, exportaciones, planes e importaciones", `<a href="/api/audit" target="_blank" rel="noopener">Ver las últimas 50 entradas</a>`)}</div>` : "";
    view.innerHTML = `<div class="head"><div><span class="eyebrow">Centro de mando · Agile Institute</span><h1>Cuadros de mando por dimensión</h1><p class="sub">Elige la dimensión profesional: cada cuadro usa su propio cuestionario y su propio n.</p></div></div>
      <form class="filters" id="filters" aria-label="Filtros"><label>Datos<select name="tipo">${["DEMO", "REAL"].map((t) => `<option ${t === state.common.tipo ? "selected" : ""}>${t}</option>`).join("")}</select></label>
      <label>Periodo<select name="periodo">${(o.periodos.length ? o.periodos : [""]).map((p) => `<option value="${p}" ${p === state.common.periodo ? "selected" : ""}>${p || "Sin periodos"}</option>`).join("")}</select></label>
      <div class="badges"><span class="badge">Rol: ${esc(state.me.role_label)}</span></div></form>
      <div class="ov-grid">${cards}</div>${admin}<p class="footer">${esc(o.disclaimer)}</p>`;
    const form = $("#import-form");
    if (form) form.onsubmit = async (e) => {
      e.preventDefault();
      const out = $("#import-result");
      out.textContent = "Importando…";
      try {
        const r = await fetch("/api/import", { method: "POST", body: new FormData(form), credentials: "same-origin" });
        const j = await r.json();
        if (!r.ok) throw new Error(j.detail || r.statusText);
        out.textContent = "Importado: " + Object.entries(j.rows).map(([k, n]) => `${k} ${n} filas`).join(" · ");
      } catch (err) { out.textContent = "Error: " + err.message; }
    };
  }

  /* ---------- exportación */
  const dlg = $("#export-dialog");
  function openExport() {
    const d = state.data;
    const items = ["Cuadro: indicadores, competencias con gráfico, fortalezas y áreas", "Pulso: indicadores de experiencia laboral y eNPS", "Detalle: tablas propias de este cuadro", "Trazabilidad: filtros, versiones, mínimos y control de calidad"];
    $("#export-contents").innerHTML = items.map((i) => `<li>${esc(i)}</li>`).join("");
    $("#export-admin").hidden = !state.me.can_export_data;
    $("#export-data").checked = false;
    $("#export-reason-wrap").hidden = true;
    $("#export-error").hidden = true;
    $("#export-title").textContent = `Descargar Excel · ${d.dashboard.label}`;
    dlg.showModal();
  }
  $("#export-data").onchange = (e) => { $("#export-reason-wrap").hidden = !e.target.checked; };
  $("#export-go").onclick = async () => {
    const key = state.data.key;
    const params = new URLSearchParams(query(currentFilters(key)));
    if ($("#export-data").checked) {
      const reason = $("#export-reason").value.trim();
      if (reason.length < 10) { const p = $("#export-error"); p.textContent = "Indica un motivo de al menos 10 caracteres."; p.hidden = false; return; }
      params.set("include_data", "true"); params.set("reason", reason);
    }
    try {
      const r = await fetch(`/api/dashboard/${key}/export.xlsx?${params}`, { credentials: "same-origin" });
      if (!r.ok) throw new Error((await r.json()).detail || r.statusText);
      const blob = await r.blob();
      const name = (r.headers.get("content-disposition") || "").match(/filename="([^"]+)"/)?.[1] || "cuadro.xlsx";
      const a = Object.assign(document.createElement("a"), { href: URL.createObjectURL(blob), download: name });
      a.click(); URL.revokeObjectURL(a.href);
      dlg.close();
    } catch (err) { const p = $("#export-error"); p.textContent = err.message; p.hidden = false; }
  };

  boot();
})();

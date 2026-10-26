"""Catálogo de los cinco cuestionarios (T01–T05) y del pulso de experiencia laboral.

La fuente es el libro de diseño `Mejora/Agile_Competences_5_Cuadros_Diseno.xlsx`:
- `Items_T01` … `Items_T05`: ítem, competencia (bloque), enunciado, escala, rango, inverso, activo, versión, fuente.
- `Items_PULSO`: los 12 ítems del pulso (F01–F08, ENPS, L01–L03).
- `CM_*`, celdas E61:E68: rótulo corto de cada competencia en su cuadro.

Solo los ítems activos forman las 8 competencias de cada test (3 ítems por competencia).
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

import openpyxl

DEFAULT_CATALOG = os.path.join(os.path.dirname(__file__), "..", "Mejora", "Agile_Competences_5_Cuadros_Diseno.xlsx")

# test -> (dimensión, nombre, hoja de cuadro, subtítulo del cuadro en el libro de diseño)
TEST_META = {
    "T01": ("persona", "Agilidad personal", "CM_Persona", "Competencias actuales · instrumento piloto pendiente de validación"),
    "T02": ("equipo", "Contribución individual al equipo", "CM_Equipo",
            "Contribución individual a equipos ágiles · agregación descriptiva de autoinformes"),
    "T03": ("liderazgo", "Liderazgo", "CM_Liderazgo", "Autopercepción de liderazgo · no es evaluación 360"),
    "T04": ("organizacion", "Organización", "CM_Organizacion", "Competencias actuales · instrumento piloto pendiente de validación"),
    "T05": ("ia", "IA transversal", "CM_IA", "Competencias actuales · instrumento piloto pendiente de validación"),
}

SCALE_LABELS = {
    "FREC_1_5": {1: "Nunca", 2: "Casi nunca", 3: "A veces", 4: "Casi siempre", 5: "Siempre"},
    # T05: escala numérica 1–5; los anclajes verbales siguen pendientes en el maestro.
    "NUM_1_5": {1: "1", 2: "2", 3: "3", 4: "4", 5: "5"},
}

PULSE_GROUPS = {
    "condiciones": ["F01", "F02", "F03"],
    "seguridad": ["F04"],
    "bienestar": ["F05", "F06", "F07", "F08"],
    "enps": ["ENPS"],
    "responsable": ["L01", "L02", "L03"],
}

PULSE_SHORT = {
    "F01": "Objetivos claros", "F02": "Reto / habilidades", "F03": "Feedback útil",
    "F04": "Expresar dudas sin temor", "F05": "Energía", "F06": "Implicación",
    "F07": "Atención sin interrupciones", "F08": "Disfrute", "ENPS": "eNPS",
    "L01": "Facilita expresar dudas", "L02": "Da autonomía", "L03": "Ajusta prioridades",
}


@dataclass
class Item:
    item_id: str
    block: int            # 1..8, 0 = reserva inactiva
    block_name: str
    text: str
    scale_id: str
    minimo: int
    maximo: int
    inverse: bool
    active: bool
    version: str
    source: str


@dataclass
class Test:
    code: str
    dimension: str
    name: str
    sheet: str
    subtitle: str
    version: str
    scale_id: str
    blocks: list[dict] = field(default_factory=list)   # {"idx", "name", "short", "items": [item_id]}
    items: list[Item] = field(default_factory=list)

    @property
    def active_items(self) -> list[Item]:
        return [i for i in self.items if i.active]


@dataclass
class PulseItem:
    item_id: str
    component: str
    text: str
    scale_id: str
    minimo: int
    maximo: int
    version: str

    @property
    def short(self) -> str:
        return PULSE_SHORT.get(self.item_id, self.item_id)


@dataclass
class Catalog:
    tests: dict[str, Test]
    pulse: list[PulseItem]
    source: str

    def pulse_item(self, item_id: str) -> PulseItem:
        return next(p for p in self.pulse if p.item_id == item_id)


def _rows(ws):
    it = ws.iter_rows(values_only=True)
    header = [str(h).strip() if h is not None else None for h in next(it)]
    for row in it:
        if row and row[0] is not None and str(row[0]).strip():
            yield {h: v for h, v in zip(header, row) if h}


def _bool(v) -> bool:
    if isinstance(v, bool):
        return v
    return str(v).strip().lower() in ("true", "1", "verdadero", "sí", "si")


def load_catalog(path: str | None = None) -> Catalog:
    path = path or os.environ.get("CDM_CATALOG_PATH", DEFAULT_CATALOG)
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    tests: dict[str, Test] = {}
    for code, (dimension, name, sheet, subtitle) in TEST_META.items():
        shorts = [r[0] for r in wb[sheet].iter_rows(min_row=61, max_row=68, min_col=5, max_col=5, values_only=True)]
        items, blocks = [], []
        for r in _rows(wb[f"Items_{code}"]):
            active = _bool(r["activo"])
            bname = str(r["bloque"]).strip()
            if active and (not blocks or blocks[-1]["name"] != bname):
                blocks.append({"idx": len(blocks) + 1, "name": bname, "items": []})
            block_idx = blocks[-1]["idx"] if active else 0
            item = Item(item_id=str(r["item_id"]).strip(), block=block_idx, block_name=bname,
                        text=str(r["enunciado"]).strip(), scale_id=str(r["escala_id"]).strip(),
                        minimo=int(r["minimo"]), maximo=int(r["maximo"]), inverse=_bool(r["inverso"]),
                        active=active, version=str(r["version"]).strip(), source=str(r.get("fuente") or ""))
            items.append(item)
            if active:
                blocks[-1]["items"].append(item.item_id)
        if len(blocks) != 8 or any(len(b["items"]) != 3 for b in blocks):
            raise ValueError(f"{code}: se esperaban 8 competencias de 3 ítems activos en Items_{code}.")
        for b, short in zip(blocks, shorts):
            b["short"] = short or b["name"]
        active = [i for i in items if i.active]
        tests[code] = Test(code=code, dimension=dimension, name=name, sheet=sheet, subtitle=subtitle,
                           version=active[0].version, scale_id=active[0].scale_id, blocks=blocks, items=items)
    pulse = [PulseItem(item_id=str(r["item_id"]).strip(), component=str(r["componente"]).strip(),
                       text=str(r["enunciado"]).strip(), scale_id=str(r["escala"]).strip(),
                       minimo=int(r["minimo"]), maximo=int(r["maximo"]), version=str(r["version"]).strip())
             for r in _rows(wb["Items_PULSO"])]
    wb.close()
    return Catalog(tests=tests, pulse=pulse, source=os.path.basename(path))


_catalog: Catalog | None = None


def get_catalog() -> Catalog:
    global _catalog
    if _catalog is None:
        _catalog = load_catalog()
    return _catalog

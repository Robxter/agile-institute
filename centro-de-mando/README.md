# Cuadros de mando por dimensión · Agile Institute (v2)

Rediseño del centro de mando siguiendo la carpeta `Mejora/`: un cuadro de mando distinto para cada dimensión profesional,
alimentado por el libro de diseño `Mejora/Agile_Competences_5_Cuadros_Diseno.xlsx` y con el aspecto de las maquetas de
`Mejora/CUADROS DE MANDO EJEMPLO 5/`.

La versión anterior (un único cuadro operativo del MVP) está íntegra en `../centro-de-mando_v1_respaldo/`.

## Arranque

```bash
pip install -r requirements.txt
python -m app.seed                             # catálogo del libro de diseño + datos DEMO ficticios
python -m uvicorn app.main:app --port 8765     # http://127.0.0.1:8765
python -m pytest -q                            # 30 pruebas
```

Si no existe `data/centro_mando.db`, el servidor la construye al arrancar.
Variables opcionales: `CDM_DB_PATH`, `CDM_CATALOG_PATH` (libro de diseño), `CDM_MIN_GROUP` (mínimo por grupo, nunca
menor que 5) y `CDM_DEMO_LOGIN=0` (desactiva el acceso de demostración).

## Los siete cuadros

| Cuadro | Fuente | Qué muestra |
|---|---|---|
| **Persona** | T01 Agilidad personal | Competencias, radar, fortalezas y áreas relativas, respuestas ítem a ítem (consulta individual), plan 30/60/90, bienestar, condiciones y evolución. |
| **Equipo** | T02 Contribución al equipo | Media y acuerdo (media frente a desviación típica), cómo responde el equipo (mapa de calor), eNPS, comparación con la media de la organización, participación. |
| **Liderazgo** | T03 + pulso L01–L03 | Autopercepción del líder junto a la percepción que recibe de su equipo (mínimo 5), conversaciones para abrir, fuentes y muestra (360 pendiente). |
| **Organización** | T04 + T01–T05 | Ocho competencias clave, eNPS, resultados por equipo con anonimato, visión conjunta de los cinco perfiles (cada uno con su n, sin índice global), prioridades. |
| **IA transversal** | T05 | Competencias de IA, IA por equipo, conductas más y menos frecuentes, perfil. |
| **Persona + IA** (mixto) | T01 + T05 | Los dos perfiles lado a lado y seis *puentes de lectura* entre competencias relacionadas (p. ej. Mentalidad abierta · Pensamiento crítico aumentado). |
| **Líder + IA** (mixto) | T03 + T05 | Liderazgo y uso de IA del líder, su IA frente a la IA de su equipo (marca de referencia), percepción recibida y puentes líder–IA. |

Los cuadros mixtos nunca suman ni restan cuestionarios distintos: muestran cada media con su propio n. Los puentes de
lectura son una propuesta para conversar, no una relación validada (están en `BRIDGES`, `app/dashboard.py`).

## Distribución personalizable

Cada panel y cada tarjeta de indicador es una ficha que el usuario puede reorganizar con **Personalizar**:

- **Mover**: arrastra la ficha por su asa ⠿ (ratón o pantalla táctil) o usa las flechas del teclado sobre el asa.
- **Ancho**: − y + recorren ¼, ⅓, ½, ⅔, ¾ y completo, sobre una rejilla de 12 columnas.
- **Ocultar / mostrar**: el ojo de cada ficha. Las fichas ocultas siguen visibles, atenuadas, mientras se edita.
- **Guardar distribución**, **Cancelar** o **Volver a la distribución estándar** desde la barra de edición. Fuera del
  modo edición, el botón **Distribución estándar** aparece cuando el cuadro tiene una distribución propia.

La distribución se guarda en el servidor por usuario y por cuadro (`user_layout`, `GET/PUT/DELETE /api/layout/{cuadro}`),
y sirve para cualquier filtro. En pantallas medianas las fichas estrechas se ensanchan, y en el móvil todas ocupan el ancho
completo. Personalizar solo cambia la presentación: no cambia qué datos autoriza cada rol.

## Reglas del libro de diseño (aplicadas en el backend)

- **Control de calidad** por fila: `METADATOS`, `DUPLICADO` (mismo `evaluacion_id`, o misma persona + periodo + tipo),
  `VALOR_INVALIDO` u `OK`. Solo las filas OK entran en los cuadros.
- **Competencia**: media de sus ítems válidos con al menos 2 de 3. `NV` y blanco no cuentan.
- **Media descriptiva**: con al menos 6 de 8 competencias. Sin baremos ni niveles A1–A5.
- **Confidencialidad**: grupos con mínimo 5 personas; la consulta individual (mínimo 1) solo la ven la propia persona,
  administración y consultoría. La percepción del responsable (L01–L03) y el eNPS exigen siempre 5.
- **Pulso**: energía, implicación, atención, disfrute, condiciones y seguridad se muestran por separado; no hay índice
  global de Flow o bienestar. eNPS = 100 × (promotores 9–10 − detractores 0–6) / n.
- **Evolución**: solo entre periodos con la misma versión del cuestionario y muestra suficiente; con un solo periodo
  se muestra la línea base.
- **DEMO y REAL nunca se combinan**; el periodo siempre es un corte concreto.

## Roles

| Rol | Cuadros | Alcance |
|---|---|---|
| Administración | Los siete | Todo; elige persona; exporta datos ítem a ítem (con motivo); importa capturas; auditoría. |
| Consultor | Los siete | Organizaciones asignadas; elige persona. |
| RRHH · solo lectura | Los siete | Su organización, solo agregados (nunca una persona concreta). Edita el plan organizativo. |
| Líder | Persona, Persona + IA, Liderazgo, Líder + IA, Equipo, IA | Su propio resultado y su propio equipo (agregado). |
| Participante | Persona, Persona + IA | Solo su propio resultado. |
| Gestor de test | Ninguno | Sin acceso a cuadros de mando. |

## Datos

- **Catálogo**: se lee al arrancar de `Items_T01…T05` e `Items_PULSO` del libro de diseño (ítems activos, competencias,
  escalas, versiones) y de los rótulos cortos de las hojas `CM_*`.
- **DEMO**: el libro de diseño se entrega vacío, así que `app/seed.py` genera 62 personas anónimas en dos organizaciones
  y ocho equipos, con dos cortes (2026-04 y 2026-10), y tres errores de captura para ver el control de calidad.
- **REAL**: rellena las hojas `Datos_T01…T05` / `Datos_PULSO` del libro de diseño (mismos encabezados) e impórtalas desde
  *Inicio → Importar capturas* (administración) o con `python -m app.importer RUTA.xlsx`. Un `evaluacion_id` existente
  se sustituye; los repetidos dentro del mismo fichero se marcan como DUPLICADO.

## Excel por cuadro

`Descargar Excel` en cada cuadro genera `Cuadro` (indicadores, competencias con gráfico nativo, fortalezas y áreas),
`Pulso`, `Detalle` (tablas propias del cuadro) y `Trazabilidad`. Administración puede añadir las hojas `Datos_Txx`
ítem a ítem indicando un motivo; queda en la auditoría. Ejemplos en `docs/`.

## Arquitectura

- `app/catalog.py` · catálogo de T01–T05 y del pulso desde el libro de diseño.
- `app/db.py` · esquema SQLite (capturas, competencias calculadas, pulso, planes, usuarios, auditoría).
- `app/scoring.py` · control de calidad, competencias (2/3) y media descriptiva (6/8).
- `app/importer.py` · importación del formato `Datos_Txx` / `Datos_PULSO`.
- `app/seed.py` · datos DEMO ficticios.
- `app/dashboard.py` · los siete cuadros, permisos por rol, mínimos de anonimato y planes.
- `app/export_xlsx.py` · exportación Excel.
- `app/main.py` · API FastAPI.
- `static/` · interfaz sin dependencias (`charts.js` con los gráficos SVG, `app.js`, `styles.css`), modo oscuro y móvil.

## Pendiente

- **Autenticación real**: el acceso de demostración elige un rol sin contraseña.
- **T05**: anclajes verbales de la escala pendientes en el maestro; no administrar como REAL sin resolverlos.
- **360, Flow global, niveles A1–A5, benchmark y madurez**: fuera de alcance hasta que se definan y validen.
- **Instrumento piloto** sin validación psicométrica: resultados para el desarrollo, no para selección ni promoción.

# Centro de mando · Centro de Test (Agile Institute)

Implementación del **menú 5 "Informes y cuadros de mando"** del *Documento Funcional del MVP – Centro de Test v1.0*
(sección 7, roles de la sección 3, seguridad de la sección 15), alimentado con el
*Excel Maestro Importable v1.0* de `../Resources`.

## Arranque

```bash
pip install -r requirements.txt
python -m app.seed                      # importa el Excel maestro y genera datos ficticios
python -m uvicorn app.main:app --port 8765   # http://127.0.0.1:8765
python -m pytest -q                     # 15 pruebas
```

Si no existe `data/centro_test.db`, el servidor la construye solo al arrancar.
Variables opcionales: `CDM_DB_PATH`, `CDM_EXCEL_PATH`, `CDM_MIN_SAMPLE` (muestra mínima, por defecto 3) y
`CDM_DEMO_LOGIN=0` (desactiva el acceso de demostración).

## Qué incluye

| Indicador (sección 7) | Implementación |
|---|---|
| Test enviados | Tarjeta principal; filtros de empresa, test y periodo (sobre `sent_at`). |
| Realizados, pendientes y caducados | Estado calculado con la regla 4.4 (`completed_at`, `expires_at`); gráfico por empresa. |
| Tasa de finalización | Realizados / enviados, con la marca del objetivo del piloto (80 %). |
| Tiempo medio de respuesta | Media y mediana de `sent_at` a `completed_at`, en días. |
| Recordatorios enviados | Recuento de `EmailLog` de tipo `reminder` en el periodo. |
| Resultado medio por indicador | Solo para un test concreto, dentro del alcance del rol y con muestra ≥ `CDM_MIN_SAMPLE`. |
| Distribución por niveles | Niveles de `INTERPRETACIONES`, por indicador y global. |
| Evolución temporal | Media mensual del global, solo con mediciones comparables (mismo `test_version` y `scoring_version`) y con más de un periodo válido. |

Además incluye una tabla de resultados individuales con búsqueda, filtro de estado y ordenación, y una vista en tabla de cada gráfico.

**Excel visual** (`GET /api/export.xlsx`, mismo diseño que la hoja `DASHBOARD_DEMO`):

- `Resumen`: indicadores operativos y cinco gráficos nativos de Excel.
- `Resultados`: tabla de Excel filtrable.
- `Indicadores`: agregados autorizados.
- `Trazabilidad`: filtros, versiones, autor y advertencias.

Las respuestas ítem a ítem solo se añaden en una exportación administrativa expresa. Requiere el rol de administrador y un motivo, y queda registrada en `audit_event`. Todas las exportaciones se auditan.
Hay un ejemplo en `docs/ejemplo_centro_de_mando.xlsx`.

## Roles (sección 3), aplicados en el backend

| Rol | Acceso al centro de mando |
|---|---|
| Administrador | Todo, incluida la exportación ítem a ítem y la auditoría (`/api/audit`). |
| Gestor de test | Sin acceso. El documento le asigna usuarios, envíos, informes y estados. |
| Consultor | Solo las empresas asignadas (`staff_company_access`). Si pide otra empresa recibe un 403. |
| Visor | Solo los cuadros compartidos (`dashboard_share`) y solo agregados, sin datos personales. |

## Arquitectura

- `app/db.py`: esquema SQLite con las entidades de la sección 5, más las tablas de personal, asignaciones y cuadros compartidos.
- `app/seed.py`: importa las hojas del Excel en el orden de `MAPA_IMPORTACION` y genera invitaciones, respuestas y correos ficticios.
- `app/scoring.py`: motor determinista. Invierte ítems, calcula la media por indicador y la media ponderada global, redondea hacia arriba y asigna el nivel según el rango.
- `app/dashboard.py`: consultas del cuadro de mando. Todo pasa por `Scope`, que aplica los permisos.
- `app/export_xlsx.py`: genera el Excel con openpyxl.
- `app/main.py`: API FastAPI y servidor de la interfaz.
- `static/`: interfaz en JavaScript sin dependencias, con gráficos SVG accesibles, tooltips, modo oscuro y versión móvil.

Esta arquitectura sirve como implementación de referencia y especificación ejecutable. Las entidades, reglas y endpoints se trasladan uno a uno a Base44, que es la plataforma recomendada en la sección 9.

## Avisos detectados en el Excel maestro

El importador los muestra al ejecutarse:

- **TESTS:** tres filas no tienen `test_code`: DEMO FORTALEZAS+FLOW, DEMO METACOMPETENCIAS ORGANIZACION 5,0 y ASSESMENT DE MADUREZ 5,0. No se importan.
- **DEMO-AGILE-12:** tiene ficha, indicadores, ítems y reglas, pero no aparece en `TESTS`. Se registra como test demo v1.0.
- **DEMO-AGILE-50:** sus 180 ítems usan el indicador `DD` y no hay indicadores, reglas ni interpretaciones. Solo muestra métricas operativas.
- **INVITACIONES_DEMO:** las cuatro filas apuntan a los códigos USR-0001…0004, que no existen en `USUARIOS`. Se omiten.
- **PLANTILLAS_EMAIL:** las plantillas `*-50` tienen el evento `completed` en las tres filas y la fecha 08/11/2026 escrita a mano. No afecta al centro de mando.

## Pendiente fuera de este módulo

- **Autenticación real.** El acceso de demostración elige un rol sin contraseña. En producción se usará la autenticación de la plataforma.
- **Decisión D-04.** Falta decidir qué resultados puede ver la empresa. El rol Visor se ha implementado solo con agregados y una muestra mínima de 3 hasta que Antonio lo apruebe.

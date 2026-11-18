<!-- converted from Excel_Maestro_Importable_Centro_de_Test_MVP_v1_0.xlsx -->

## Sheet: INICIO
| Centro de Test · Excel maestro importable |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Agile Institute · MVP v1.0 · 23/09/2026 |  |  |  |  |  |  |  |
| Orden de importación | Hoja / entidad |  |  |  |  |  |  |
| 1 | USUARIOS |  |  |  |  |  |  |
| 2 | TESTS |  |  |  |  |  |  |
| 3 | FICHAS_TECNICAS |  |  |  |  |  |  |
| 4 | INDICADORES |  |  |  |  |  |  |
| 5 | ITEMS |  |  |  |  |  |  |
| 6 | OPCIONES_RESPUESTA |  |  |  |  |  |  |
| 7 | REGLAS_PUNTUACION |  |  |  |  |  |  |
| 8 | INTERPRETACIONES |  |  |  |  |  |  |
| 9 | PLANTILLAS_EMAIL |  |  |  |  |  |  |
| Regla | Aplicación |  |  |  |  |  |  |
| No borrar códigos | Son las claves que relacionan las hojas y las entidades de Base44. |  |  |  |  |  |  |
| Una fila = un registro | Guardar cada hoja como CSV UTF-8 antes de importarla en Base44. |  |  |  |  |  |  |
| Datos ficticios | Las filas de ejemplo no contienen datos personales reales. |  |  |  |  |  |  |
| Campos amarillos | Deben revisarse o completarse antes del piloto. |  |  |  |  |  |  |
| Ítems protegidos | No cargar ítems de pruebas de terceros sin licencia o autorización. |  |  |  |  |  |  |
| Publicación | Bloquear la versión de un test cuando ya tenga respuestas. |  |  |  |  |  |  |
| Trazabilidad | Cada resultado debe conservar test_code, test_version y scoring_version. |  |  |  |  |  |  |
| Fuente técnica | Enlace |  |  |  |  |  |  |
| Base44 | https://docs.base44.com/ |  |  |  |  |  |  |
| Base44 · correos | https://docs.base44.com/documentation/building-your-app/sending-emails |  |  |  |  |  |  |
| Base44 · automatizaciones | https://docs.base44.com/developers/backend/resources/backend-functions/automations |  |  |  |  |  |  |
| Resend | https://resend.com/pricing |  |  |  |  |  |  |
## Sheet: DASHBOARD_DEMO
| Cuadro de mando de ejemplo |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Datos totalmente ficticios. Sirve para validar el diseño de la exportación Excel. |  |  |  |  |  |  |  |
| Indicador | Valor |  |  |  |  |  |  |
| Test enviados | 8 |  |  |  |  |  |  |
| Realizados | 4 |  |  |  |  |  |  |
| Pendientes | 3 |  |  |  |  |  |  |
| Caducados | 1 |  |  |  |  |  |  |
| Indicador medido | Media (1-5) |  |  |  |  |  |  |
| Adaptabilidad | 3.8 |  |  |  |  |  |  |
| Colaboración | 4.2 |  |  |  |  |  |  |
| Orientación a valor | 3.5 |  |  |  |  |  |  |
| Aprendizaje continuo | 3.9 |  |  |  |  |  |  |
| Uso responsable de IA | 3.4 |  |  |  |  |  |  |
| Empresa | Persona | Test | Estado | Fecha | Resultado global |  |  |
| Empresa Demo A | Ana López | Demo Capacidades Ágiles | Realizado | 2026-09-12 00:00:00 | 3.8 |  |  |
| Empresa Demo A | Luis García | Demo Capacidades Ágiles | Realizado | 2026-09-13 00:00:00 | 4.1 |  |  |
| Empresa Demo B | Marta Soler | Demo Capacidades Ágiles | Pendiente |  |  |  |  |
| Empresa Demo B | Carlos Ruiz | Demo Capacidades Ágiles | Caducado |  |  |  |  |
| Empresa Demo B | Nora Pérez | Demo Capacidades Ágiles | Realizado | 2026-09-18 00:00:00 | 3.4 |  |  |
## Sheet: USUARIOS
| Usuarios |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Todos los destinatarios de test deben existir aquí antes del envío. |  |  |  |  |  |  |  |  |  |  |
| user_code | company_name | first_name | last_name | position | dimension | email | language | status | consent_status | created_at |
| USR-M3Q7 | Empresa Demo A | Carlos | López | Líder de equipo | Equipo | carlos.lopez@example.com | es | active | pending | 2026-10-05 00:00:00 |
| USR-P6N2 | Empresa Demo A | María | Sánchez | Participante | Persona | maria.sanchez@example.com | es | active | pending | 2026-10-05 00:00:00 |
| USR-R4T9 | Empresa Demo A | Pablo | Martín | Participante | Persona | pablo.martin@example.com | es | active | pending | 2026-10-05 00:00:00 |
| USR-V2L8 | Empresa Demo B | Laura | Gómez | Líder de equipo | Equipo | laura.gomez@example.com | es | active | pending | 2026-10-05 00:00:00 |
| USR-Y7C5 | Empresa Demo B | Daniel | Ruiz | Participante | Persona | daniel.ruiz@example.com | es | active | pending | 2026-10-05 00:00:00 |
| USR-Z5H1 | Empresa Demo B | Elena | Torres | Participante | Persona | elena.torres@example.com | es | active | pending | 2026-10-05 00:00:00 |
| USR-K8P4 | Empresa Demo A | Ana | García | Responsable de RRHH | Organizativa | ana.garcia@example.com | es | active | pending | 2026-10-05 00:00:00 |
## Sheet: TESTS
| Catálogo de test |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Un test publicado no debe modificarse; se crea una nueva versión. |  |  |  |  |  |  |  |  |  |  |  |
| test_code | test_name | version | status | owner | purpose | default_scale_code | report_template_code | expiry_days | reminder_days | ai_report_enabled | license_status |
|  | DEMO FORTALEZAS+FLOW |  |  |  |  |  |  |  |  |  |  |
|  | DEMO METACOMPETENCIAS ORGANIZACION 5,0 |  |  |  |  |  |  |  |  |  |  |
|  | ASSESMENT DE MADUREZ 5,0 |  |  |  |  |  |  |  |  |  |  |
| DEMO-AGILE-50 | METACOMPETENCIAS ORGANIZACIÓN 5.0® | 2,0 | PILOTO/NO VALIDABLE |  | DIAGNÓSTICO Y DESARROLLO | 1–5 + NA |  |  |  |  |  |
## Sheet: FICHAS_TECNICAS
| Fichas técnicas |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| La ficha debe estar aprobada antes de activar un test. |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| test_code | name | authors | year | adaptation | num_items | item_format | scales | psychometric_properties | interpretation | references | rights_and_license | approved_by | approval_date |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| DEMO-AGILE-12 | Demo Capacidades Ágiles | Agile Institute | 2026 | Instrumento sintético para pruebas técnicas | 12 | Likert de 5 puntos | Adaptabilidad; Colaboración; Orientación a valor; Aprendizaje continuo; Uso responsable de IA | No es una prueba validada. Usar únicamente para probar la plataforma. | Una puntuación alta representa mayor presencia declarada de las conductas incluidas. | Documentación interna del MVP | Propiedad de Agile Institute; uso técnico |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| UWES9-REF | Escala Utrecht de Engagement-9 (UWES-9) | Schaufeli, Salanova y Bakker | 2002 | Adaptación española disponible | 9 | Likert de 7 puntos | Vigor; Dedicación; Absorción | La documentación aportada informa de consistencia interna por escala y estructura trifactorial. | Una puntuación superior refleja mayor engagement. La interpretación final debe seguir el manual y baremos autorizados. | Schaufeli, Salanova y Bakker (2002); documentación oficial de UWES | No cargar ítems ni administrar sin comprobar derechos, manual y condiciones de uso. |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| DEMO-AGILE-50 | MetaCompetencias Organización 5.0® | Agile Institute  | 2026 | Versión piloto 2.0. Personas adultas en contexto organizativo. Autoinforme. | 180 | Conductas observables; primera persona; una conducta principal por ítem; marco temporal últimos seis meses. | 0 No aplica · 1 Nunca · 2 Rara vez · 3 A veces · 4 Frecuentemente · 5 Casi siempre  | Instrumento pendiente de validación. Preparado para pilotaje y validación. Los 8 indicadores son lecturas ejecutivas y no factores psicométricos independientes hasta que los datos lo confirmen. | Competencia: media de sus ítems válidos; mínimo 2 de 3. Metacompetencia/indicador: media de competencias válidas; mínimo 70% disponibles. NA se excluye y nunca se convierte en cero. Puntuaciones descriptivas, no diagnósticas. No hay puntos de corte A1-A5 definitivos antes de validación/baremación. | Manual técnico del instrumento empírico 180/60/13/8 · Piloto 2.1 · Septiembre 2026; Cuestionario Piloto MetaCompetencias Organización 5.0® · Versión piloto 2.0 · Septiembre 2026. | Propiedad de Agile Institute; uso técnico/piloto. No presentar como validado ni utilizar por sí solo para selección, promoción o decisiones laborales de alto impacto. | Pendiente | Pendiente |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
## Sheet: ITEMS
| Ítems |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ejemplos propios para probar la aplicación; no constituyen un instrumento validado. |  |  |  |  |  |  |  |  |
| item_code | test_code | indicator_code | item_text | response_scale_code | display_order | required | reverse_scored | active |
| DEM-001 | DEMO-AGILE-12 | ADA | Cuando cambia una prioridad, ajusto mi forma de trabajar sin perder de vista el objetivo. | LIKERT5 | 1 | True | False | True |
| DEM-002 | DEMO-AGILE-12 | ADA | Necesito demasiado tiempo para reaccionar cuando aparece información nueva. | LIKERT5 | 2 | True | True | True |
| DEM-003 | DEMO-AGILE-12 | COL | Comparto información útil antes de que otras personas tengan que pedírmela. | LIKERT5 | 3 | True | False | True |
| DEM-004 | DEMO-AGILE-12 | COL | Pido ayuda y ofrezco apoyo cuando una tarea depende de varias personas. | LIKERT5 | 4 | True | False | True |
| DEM-005 | DEMO-AGILE-12 | VAL | Antes de empezar, aclaro qué resultado útil se espera conseguir. | LIKERT5 | 5 | True | False | True |
| DEM-006 | DEMO-AGILE-12 | VAL | Mantengo tareas aunque ya no esté claro el valor que aportan. | LIKERT5 | 6 | True | True | True |
| DEM-007 | DEMO-AGILE-12 | APR | Convierto el feedback recibido en una acción concreta de mejora. | LIKERT5 | 7 | True | False | True |
| DEM-008 | DEMO-AGILE-12 | APR | Después de una experiencia relevante, reviso qué aprendí y qué haré distinto. | LIKERT5 | 8 | True | False | True |
| DEM-009 | DEMO-AGILE-12 | IA | Compruebo la información generada por IA antes de utilizarla para decidir. | LIKERT5 | 9 | True | False | True |
| DEM-010 | DEMO-AGILE-12 | IA | Evito introducir datos sensibles en herramientas de IA no autorizadas. | LIKERT5 | 10 | True | False | True |
| DEM-011 | DEMO-AGILE-12 | COL | Cuando discrepo, explico mi punto de vista con respeto y escucho la alternativa. | LIKERT5 | 11 | True | False | True |
| DEM-012 | DEMO-AGILE-12 | VAL | Compruebo con evidencia si una solución ha producido el resultado esperado. | LIKERT5 | 12 | True | False | True |
| ITEM 1 | DEMO-AGILE-50 | DD | Identifico mis emociones y reconozco cómo influyen en mi conducta. | 0-5 |  |  |  |  |
| ITEM 2 | DEMO-AGILE-50 | DD | Distingo hechos, interpretaciones y reacciones emocionales antes de actuar. | 0-5 |  |  |  |  |
| ITEM 3 | DEMO-AGILE-50 | DD | Reconozco mis patrones emocionales en situaciones de presión o cambio. | 0-5 |  |  |  |  |
| ITEM 4 | DEMO-AGILE-50 | DD | Gestiono mis respuestas ante presión, frustración o conflicto sin perder eficacia. | 0-5 |  |  |  |  |
| ITEM 5 | DEMO-AGILE-50 | DD | Hago pausas deliberadas cuando una reacción emocional puede afectar a una decisión. | 0-5 |  |  |  |  |
| ITEM 6 | DEMO-AGILE-50 | DD | Adapto mi respuesta emocional a las necesidades de la situación. | 0-5 |  |  |  |  |
| ITEM 7 | DEMO-AGILE-50 | DD | Escucho e interpreto las necesidades y perspectivas de otras personas. | 0-5 |  |  |  |  |
| ITEM 8 | DEMO-AGILE-50 | DD | Adapto mi comunicación considerando emociones y contexto del interlocutor. | 0-5 |  |  |  |  |
| ITEM 9 | DEMO-AGILE-50 | DD | Evito atribuir intenciones sin contrastarlas y busco comprender antes de responder. | 0-5 |  |  |  |  |
| ITEM 10 | DEMO-AGILE-50 | DD | Abordo desacuerdos de forma directa y respetuosa. | 0-5 |  |  |  |  |
| ITEM 11 | DEMO-AGILE-50 | DD | Separo a las personas del problema y busco intereses compartidos. | 0-5 |  |  |  |  |
| ITEM 12 | DEMO-AGILE-50 | DD | Convierto el conflicto en una oportunidad de aprendizaje y mejora. | 0-5 |  |  |  |  |
| ITEM 13 | DEMO-AGILE-50 | DD | Considero perspectivas alternativas antes de cerrar una posición. | 0-5 |  |  |  |  |
| ITEM 14 | DEMO-AGILE-50 | DD | Reviso mis supuestos cuando aparece nueva evidencia. | 0-5 |  |  |  |  |
| ITEM 15 | DEMO-AGILE-50 | DD | Experimento con nuevas formas de trabajar sin aferrarme a hábitos por inercia. | 0-5 |  |  |  |  |
| ITEM 16 | DEMO-AGILE-50 | DD | Actúo de forma razonable aun cuando la información sea incompleta. | 0-5 |  |  |  |  |
| ITEM 17 | DEMO-AGILE-50 | DD | Distingo lo que sé de lo que necesito descubrir. | 0-5 |  |  |  |  |
| ITEM 18 | DEMO-AGILE-50 | DD | Evito bloquear la acción esperando certezas que no existen. | 0-5 |  |  |  |  |
| ITEM 19 | DEMO-AGILE-50 | DD | Mantengo el foco en lo controlable ante situaciones cambiantes. | 0-5 |  |  |  |  |
| ITEM 20 | DEMO-AGILE-50 | DD | Recupero el aprendizaje después de un error o contratiempo. | 0-5 |  |  |  |  |
| ITEM 21 | DEMO-AGILE-50 | DD | Solicito apoyo y reorganizo prioridades cuando la situación lo requiere. | 0-5 |  |  |  |  |
| ITEM 22 | DEMO-AGILE-50 | DD | Anticipo necesidades y propongo acciones concretas. | 0-5 |  |  |  |  |
| ITEM 23 | DEMO-AGILE-50 | DD | Convierto problemas detectados en pequeños experimentos o iniciativas. | 0-5 |  |  |  |  |
| ITEM 24 | DEMO-AGILE-50 | DD | Hago seguimiento de los compromisos asumidos y ajusto cuando es necesario. | 0-5 |  |  |  |  |
| ITEM 25 | DEMO-AGILE-50 | DD | Interpreto el error como información para mejorar. | 0-5 |  |  |  |  |
| ITEM 26 | DEMO-AGILE-50 | DD | Busco retos que amplíen mis capacidades. | 0-5 |  |  |  |  |
| ITEM 27 | DEMO-AGILE-50 | DD | Cambio de estrategia cuando la evidencia muestra que una forma de actuar no funciona. | 0-5 |  |  |  |  |
| ITEM 28 | DEMO-AGILE-50 | DD | Formulo preguntas para comprender mejor problemas y oportunidades. | 0-5 |  |  |  |  |
| ITEM 29 | DEMO-AGILE-50 | DD | Busco información relevante más allá de la primera respuesta. | 0-5 |  |  |  |  |
| ITEM 30 | DEMO-AGILE-50 | DD | Transformo la curiosidad en acciones de aprendizaje concretas. | 0-5 |  |  |  |  |
| ITEM 31 | DEMO-AGILE-50 | DD | Defino qué quiero mejorar y practico de forma intencionada. | 0-5 |  |  |  |  |
| ITEM 32 | DEMO-AGILE-50 | DD | Reviso periódicamente qué ha funcionado y qué debe cambiar. | 0-5 |  |  |  |  |
| ITEM 33 | DEMO-AGILE-50 | DD | Utilizo el feedback para ajustar mi comportamiento. | 0-5 |  |  |  |  |
| ITEM 34 | DEMO-AGILE-50 | DD | Aplico lo aprendido en situaciones diferentes a aquella en la que lo adquirí. | 0-5 |  |  |  |  |
| ITEM 35 | DEMO-AGILE-50 | DD | Explico cómo puedo reutilizar una práctica en otro contexto. | 0-5 |  |  |  |  |
| ITEM 36 | DEMO-AGILE-50 | DD | Evito convertir una solución útil en una receta rígida. | 0-5 |  |  |  |  |
| ITEM 37 | DEMO-AGILE-50 | DD | Busco comprender necesidades, problemas y contexto antes de proponer soluciones. | 0-5 |  |  |  |  |
| ITEM 38 | DEMO-AGILE-50 | DD | Contrasto supuestos directamente con clientes o usuarios cuando es posible. | 0-5 |  |  |  |  |
| ITEM 39 | DEMO-AGILE-50 | DD | Integro feedback real en las decisiones del equipo. | 0-5 |  |  |  |  |
| ITEM 40 | DEMO-AGILE-50 | DD | Explico qué valor se espera generar con una iniciativa. | 0-5 |  |  |  |  |
| ITEM 41 | DEMO-AGILE-50 | DD | Priorizo resultados para cliente y negocio frente a actividad por actividad. | 0-5 |  |  |  |  |
| ITEM 42 | DEMO-AGILE-50 | DD | Reviso si el trabajo realizado está produciendo el valor esperado. | 0-5 |  |  |  |  |
| ITEM 43 | DEMO-AGILE-50 | DD | Ordeno opciones según impacto, urgencia, esfuerzo y evidencia disponible. | 0-5 |  |  |  |  |
| ITEM 44 | DEMO-AGILE-50 | DD | Hago explícitos los criterios de priorización. | 0-5 |  |  |  |  |
| ITEM 45 | DEMO-AGILE-50 | DD | Repriorizo cuando cambian las necesidades o aparece nueva información. | 0-5 |  |  |  |  |
| ITEM 46 | DEMO-AGILE-50 | DD | Pruebo hipótesis antes de realizar inversiones grandes. | 0-5 |  |  |  |  |
| ITEM 47 | DEMO-AGILE-50 | DD | Busco feedback temprano sobre entregables y decisiones. | 0-5 |  |  |  |  |
| ITEM 48 | DEMO-AGILE-50 | DD | Incorporo aprendizajes en ciclos sucesivos de mejora. | 0-5 |  |  |  |  |
| ITEM 49 | DEMO-AGILE-50 | DD | Construyo una comprensión común del propósito y del resultado esperado. | 0-5 |  |  |  |  |
| ITEM 50 | DEMO-AGILE-50 | DD | Hago visibles objetivos, dependencias y criterios de éxito. | 0-5 |  |  |  |  |
| ITEM 51 | DEMO-AGILE-50 | DD | Compruebo que las decisiones del equipo siguen conectadas con el propósito. | 0-5 |  |  |  |  |
| ITEM 52 | DEMO-AGILE-50 | DD | Comparto información relevante con otras áreas sin esperar a que la soliciten. | 0-5 |  |  |  |  |
| ITEM 53 | DEMO-AGILE-50 | DD | Busco soluciones que optimicen el sistema y no solo mi propio ámbito. | 0-5 |  |  |  |  |
| ITEM 54 | DEMO-AGILE-50 | DD | Facilito acuerdos entre funciones con intereses diferentes. | 0-5 |  |  |  |  |
| ITEM 55 | DEMO-AGILE-50 | DD | Asumo responsabilidad por resultados compartidos. | 0-5 |  |  |  |  |
| ITEM 56 | DEMO-AGILE-50 | DD | Evito trasladar automáticamente los problemas a otra persona o área. | 0-5 |  |  |  |  |
| ITEM 57 | DEMO-AGILE-50 | DD | Pido ayuda y ofrezco apoyo cuando el resultado común lo requiere. | 0-5 |  |  |  |  |
| ITEM 58 | DEMO-AGILE-50 | DD | Identifico dependencias antes de que se conviertan en bloqueos. | 0-5 |  |  |  |  |
| ITEM 59 | DEMO-AGILE-50 | DD | Acuerdo responsables, expectativas y fechas de coordinación. | 0-5 |  |  |  |  |
| ITEM 60 | DEMO-AGILE-50 | DD | Escalo impedimentos con información suficiente y propuesta de solución. | 0-5 |  |  |  |  |
| ITEM 61 | DEMO-AGILE-50 | DD | Escucho sin interrumpir y verifico que he comprendido. | 0-5 |  |  |  |  |
| ITEM 62 | DEMO-AGILE-50 | DD | Formulo preguntas para aclarar necesidades y supuestos. | 0-5 |  |  |  |  |
| ITEM 63 | DEMO-AGILE-50 | DD | Distingo escuchar de limitarme a esperar mi turno para hablar. | 0-5 |  |  |  |  |
| ITEM 64 | DEMO-AGILE-50 | DD | Expreso ideas con estructura y propósito. | 0-5 |  |  |  |  |
| ITEM 65 | DEMO-AGILE-50 | DD | Adapto el nivel de detalle al interlocutor y a la situación. | 0-5 |  |  |  |  |
| ITEM 66 | DEMO-AGILE-50 | DD | Hago explícitos acuerdos, decisiones y próximos pasos. | 0-5 |  |  |  |  |
| ITEM 67 | DEMO-AGILE-50 | DD | Ofrezco feedback específico sobre conductas y efectos. | 0-5 |  |  |  |  |
| ITEM 68 | DEMO-AGILE-50 | DD | Combino reconocimiento con oportunidades concretas de mejora. | 0-5 |  |  |  |  |
| ITEM 69 | DEMO-AGILE-50 | DD | Solicito feedback sobre mi propio desempeño. | 0-5 |  |  |  |  |
| ITEM 70 | DEMO-AGILE-50 | DD | Abordo conversaciones pendientes antes de que escalen. | 0-5 |  |  |  |  |
| ITEM 71 | DEMO-AGILE-50 | DD | Expongo hechos y necesidades sin descalificar a la persona. | 0-5 |  |  |  |  |
| ITEM 72 | DEMO-AGILE-50 | DD | Busco acuerdos y compromisos verificables. | 0-5 |  |  |  |  |
| ITEM 73 | DEMO-AGILE-50 | DD | Conecto las decisiones diarias con un propósito comprensible. | 0-5 |  |  |  |  |
| ITEM 74 | DEMO-AGILE-50 | DD | Alineo expectativas y prioridades con claridad. | 0-5 |  |  |  |  |
| ITEM 75 | DEMO-AGILE-50 | DD | Utilizo el propósito como criterio para resolver dilemas y prioridades. | 0-5 |  |  |  |  |
| ITEM 76 | DEMO-AGILE-50 | DD | Construyo credibilidad mediante la escucha, la coherencia y la colaboración. | 0-5 |  |  |  |  |
| ITEM 77 | DEMO-AGILE-50 | DD | Influyo desde argumentos, relaciones y propósito, no solo desde el cargo. | 0-5 |  |  |  |  |
| ITEM 78 | DEMO-AGILE-50 | DD | Facilito acuerdos entre personas con intereses diferentes. | 0-5 |  |  |  |  |
| ITEM 79 | DEMO-AGILE-50 | DD | Delego resultados y contexto, no solo tareas. | 0-5 |  |  |  |  |
| ITEM 80 | DEMO-AGILE-50 | DD | Defino límites de decisión claros y permito autonomía. | 0-5 |  |  |  |  |
| ITEM 81 | DEMO-AGILE-50 | DD | Intervengo para desbloquear sin recuperar innecesariamente el control. | 0-5 |  |  |  |  |
| ITEM 82 | DEMO-AGILE-50 | DD | Mantengo conversaciones periódicas sobre desarrollo y desempeño. | 0-5 |  |  |  |  |
| ITEM 83 | DEMO-AGILE-50 | DD | Creo oportunidades para asumir responsabilidad y aprender. | 0-5 |  |  |  |  |
| ITEM 84 | DEMO-AGILE-50 | DD | Adapto el acompañamiento al nivel de autonomía de cada persona o equipo. | 0-5 |  |  |  |  |
| ITEM 85 | DEMO-AGILE-50 | DD | Distingo problemas simples, complicados y complejos antes de actuar. | 0-5 |  |  |  |  |
| ITEM 86 | DEMO-AGILE-50 | DD | Trabajo con hipótesis cuando no existe una solución conocida. | 0-5 |  |  |  |  |
| ITEM 87 | DEMO-AGILE-50 | DD | Evito respuestas lineales ante problemas sistémicos. | 0-5 |  |  |  |  |
| ITEM 88 | DEMO-AGILE-50 | DD | Invito a expresar dudas, errores y desacuerdos sin represalias. | 0-5 |  |  |  |  |
| ITEM 89 | DEMO-AGILE-50 | DD | Reconozco públicamente aprendizajes derivados de errores. | 0-5 |  |  |  |  |
| ITEM 90 | DEMO-AGILE-50 | DD | Modelo la vulnerabilidad profesional pidiendo ayuda cuando la necesito. | 0-5 |  |  |  |  |
| ITEM 91 | DEMO-AGILE-50 | DD | Reconozco contribuciones concretas y su impacto. | 0-5 |  |  |  |  |
| ITEM 92 | DEMO-AGILE-50 | DD | Equilibro reconocimiento de resultados con reconocimiento de comportamientos valiosos. | 0-5 |  |  |  |  |
| ITEM 93 | DEMO-AGILE-50 | DD | Hago visible el progreso del equipo. | 0-5 |  |  |  |  |
| ITEM 94 | DEMO-AGILE-50 | DD | Detecto señales de sobrecarga antes de que afecten al desempeño. | 0-5 |  |  |  |  |
| ITEM 95 | DEMO-AGILE-50 | DD | Priorizo y protejo el foco ante exceso de trabajo. | 0-5 |  |  |  |  |
| ITEM 96 | DEMO-AGILE-50 | DD | Promuevo ritmos sostenibles y reviso cargas de forma periódica. | 0-5 |  |  |  |  |
| ITEM 97 | DEMO-AGILE-50 | DD | Integro necesidades de sostenibilidad personal en la planificación cuando es posible. | 0-5 |  |  |  |  |
| ITEM 98 | DEMO-AGILE-50 | DD | Evito normalizar disponibilidad permanente como criterio de compromiso. | 0-5 |  |  |  |  |
| ITEM 99 | DEMO-AGILE-50 | DD | Gestiono expectativas para proteger tiempos de descanso y recuperación. | 0-5 |  |  |  |  |
| ITEM 100 | DEMO-AGILE-50 | DD | Considero el impacto humano de las decisiones de gestión. | 0-5 |  |  |  |  |
| ITEM 101 | DEMO-AGILE-50 | DD | Activo conversaciones de cuidado cuando aparecen señales de riesgo. | 0-5 |  |  |  |  |
| ITEM 102 | DEMO-AGILE-50 | DD | Integro bienestar y desempeño en lugar de tratarlos como objetivos opuestos. | 0-5 |  |  |  |  |
| ITEM 103 | DEMO-AGILE-50 | DD | Genero alternativas antes de elegir una solución. | 0-5 |  |  |  |  |
| ITEM 104 | DEMO-AGILE-50 | DD | Reformulo problemas desde perspectivas diferentes. | 0-5 |  |  |  |  |
| ITEM 105 | DEMO-AGILE-50 | DD | Combino ideas y recursos existentes para crear nuevas posibilidades. | 0-5 |  |  |  |  |
| ITEM 106 | DEMO-AGILE-50 | DD | Formulo hipótesis verificables antes de experimentar. | 0-5 |  |  |  |  |
| ITEM 107 | DEMO-AGILE-50 | DD | Diseño experimentos pequeños y medibles. | 0-5 |  |  |  |  |
| ITEM 108 | DEMO-AGILE-50 | DD | Decido continuar, adaptar o abandonar según la evidencia. | 0-5 |  |  |  |  |
| ITEM 109 | DEMO-AGILE-50 | DD | Identifico oportunidades de mejora en el trabajo cotidiano. | 0-5 |  |  |  |  |
| ITEM 110 | DEMO-AGILE-50 | DD | Mido cambios antes y después de una intervención cuando es posible. | 0-5 |  |  |  |  |
| ITEM 111 | DEMO-AGILE-50 | DD | Convierto aprendizajes en nuevas prácticas. | 0-5 |  |  |  |  |
| ITEM 112 | DEMO-AGILE-50 | DD | Distingo el error de la negligencia y analizo sus causas sin buscar culpables de forma automática. | 0-5 |  |  |  |  |
| ITEM 113 | DEMO-AGILE-50 | DD | Extraigo aprendizajes concretos de los fallos. | 0-5 |  |  |  |  |
| ITEM 114 | DEMO-AGILE-50 | DD | Introduzco cambios para reducir la repetición de errores relevantes. | 0-5 |  |  |  |  |
| ITEM 115 | DEMO-AGILE-50 | DD | Cuestiono supuestos antes de convertirlos en decisiones. | 0-5 |  |  |  |  |
| ITEM 116 | DEMO-AGILE-50 | DD | Comparo explicaciones alternativas ante un problema. | 0-5 |  |  |  |  |
| ITEM 117 | DEMO-AGILE-50 | DD | Distingo correlación, causalidad, evidencia y opinión. | 0-5 |  |  |  |  |
| ITEM 118 | DEMO-AGILE-50 | DD | Defino qué información necesito antes de decidir. | 0-5 |  |  |  |  |
| ITEM 119 | DEMO-AGILE-50 | DD | Explicito criterios y supuestos de una decisión. | 0-5 |  |  |  |  |
| ITEM 120 | DEMO-AGILE-50 | DD | Reviso decisiones cuando cambia la evidencia. | 0-5 |  |  |  |  |
| ITEM 121 | DEMO-AGILE-50 | DD | Presento datos de forma comprensible para la audiencia. | 0-5 |  |  |  |  |
| ITEM 122 | DEMO-AGILE-50 | DD | Diferencio datos relevantes de ruido informativo. | 0-5 |  |  |  |  |
| ITEM 123 | DEMO-AGILE-50 | DD | Explico tendencias y límites de los datos sin manipular su interpretación. | 0-5 |  |  |  |  |
| ITEM 124 | DEMO-AGILE-50 | DD | Comprendo conceptos básicos de datos, modelos y resultados generados por IA. | 0-5 |  |  |  |  |
| ITEM 125 | DEMO-AGILE-50 | DD | Identifico cuándo una salida automatizada necesita validación adicional. | 0-5 |  |  |  |  |
| ITEM 126 | DEMO-AGILE-50 | DD | Utilizo herramientas de datos e IA teniendo en cuenta sus limitaciones. | 0-5 |  |  |  |  |
| ITEM 127 | DEMO-AGILE-50 | DD | Defino indicadores relacionados con resultados y no solo con actividad. | 0-5 |  |  |  |  |
| ITEM 128 | DEMO-AGILE-50 | DD | Comparo resultados con objetivos y expectativas. | 0-5 |  |  |  |  |
| ITEM 129 | DEMO-AGILE-50 | DD | Utilizo las métricas para aprender y adaptar, no solo para controlar. | 0-5 |  |  |  |  |
| ITEM 130 | DEMO-AGILE-50 | DD | Convierto objetivos en resultados y próximos pasos claros. | 0-5 |  |  |  |  |
| ITEM 131 | DEMO-AGILE-50 | DD | Actualizo planes cuando cambian prioridades o restricciones. | 0-5 |  |  |  |  |
| ITEM 132 | DEMO-AGILE-50 | DD | Hago visibles compromisos, responsables y dependencias. | 0-5 |  |  |  |  |
| ITEM 133 | DEMO-AGILE-50 | DD | Defino criterios de calidad antes de ejecutar. | 0-5 |  |  |  |  |
| ITEM 134 | DEMO-AGILE-50 | DD | Integro prevención y revisión en el flujo de trabajo. | 0-5 |  |  |  |  |
| ITEM 135 | DEMO-AGILE-50 | DD | No sacrifico la calidad crítica para aparentar velocidad. | 0-5 |  |  |  |  |
| ITEM 136 | DEMO-AGILE-50 | DD | Limito el trabajo en curso cuando se genera saturación. | 0-5 |  |  |  |  |
| ITEM 137 | DEMO-AGILE-50 | DD | Identifico cuellos de botella y actúo sobre ellos. | 0-5 |  |  |  |  |
| ITEM 138 | DEMO-AGILE-50 | DD | Priorizo finalizar valor antes que iniciar más actividad. | 0-5 |  |  |  |  |
| ITEM 139 | DEMO-AGILE-50 | DD | Identifico tareas repetitivas que pueden automatizarse con seguridad. | 0-5 |  |  |  |  |
| ITEM 140 | DEMO-AGILE-50 | DD | Evalúo coste, beneficio y riesgo antes de automatizar. | 0-5 |  |  |  |  |
| ITEM 141 | DEMO-AGILE-50 | DD | Superviso los resultados de automatizaciones y ajusto cuando es necesario. | 0-5 |  |  |  |  |
| ITEM 142 | DEMO-AGILE-50 | DD | Defino resultados esperados y cómo comprobarlos. | 0-5 |  |  |  |  |
| ITEM 143 | DEMO-AGILE-50 | DD | Hago seguimiento del avance hacia resultados. | 0-5 |  |  |  |  |
| ITEM 144 | DEMO-AGILE-50 | DD | Reoriento recursos cuando la actividad no produce el impacto esperado. | 0-5 |  |  |  |  |
| ITEM 145 | DEMO-AGILE-50 | DD | Identifico señales relevantes del entorno interno y externo. | 0-5 |  |  |  |  |
| ITEM 146 | DEMO-AGILE-50 | DD | Comparto señales de cambio con las personas afectadas. | 0-5 |  |  |  |  |
| ITEM 147 | DEMO-AGILE-50 | DD | Utilizo escenarios y tendencias para anticipar posibles impactos. | 0-5 |  |  |  |  |
| ITEM 148 | DEMO-AGILE-50 | DD | Reviso roles y procesos cuando dejan de aportar valor. | 0-5 |  |  |  |  |
| ITEM 149 | DEMO-AGILE-50 | DD | Simplifico pasos, aprobaciones o dependencias innecesarias. | 0-5 |  |  |  |  |
| ITEM 150 | DEMO-AGILE-50 | DD | Rediseño el sistema cuando el problema no se resuelve optimizando una parte. | 0-5 |  |  |  |  |
| ITEM 151 | DEMO-AGILE-50 | DD | Defino derechos de decisión y responsabilidades claros. | 0-5 |  |  |  |  |
| ITEM 152 | DEMO-AGILE-50 | DD | Equilibro autonomía con controles proporcionales al riesgo. | 0-5 |  |  |  |  |
| ITEM 153 | DEMO-AGILE-50 | DD | Hago trazables las decisiones relevantes. | 0-5 |  |  |  |  |
| ITEM 154 | DEMO-AGILE-50 | DD | Alineo capacidades, comportamientos y cultura con la estrategia. | 0-5 |  |  |  |  |
| ITEM 155 | DEMO-AGILE-50 | DD | Facilito movilidad y aprendizaje entre áreas. | 0-5 |  |  |  |  |
| ITEM 156 | DEMO-AGILE-50 | DD | Integro nuevos comportamientos en procesos de talento y liderazgo. | 0-5 |  |  |  |  |
| ITEM 157 | DEMO-AGILE-50 | DD | Mantengo capacidad de respuesta ante cambios significativos. | 0-5 |  |  |  |  |
| ITEM 158 | DEMO-AGILE-50 | DD | Aprendo de crisis, incidentes y disrupciones. | 0-5 |  |  |  |  |
| ITEM 159 | DEMO-AGILE-50 | DD | Construyo redundancias, capacidades y relaciones que aumentan la resiliencia. | 0-5 |  |  |  |  |
| ITEM 160 | DEMO-AGILE-50 | DD | Conecto las decisiones estratégicas y operativas con el propósito, los valores y el impacto esperado de la organización. | 0-5 |  |  |  |  |
| ITEM 161 | DEMO-AGILE-50 | DD | Considero las consecuencias económicas, humanas, sociales y ambientales antes de impulsar cambios relevantes. | 0-5 |  |  |  |  |
| ITEM 162 | DEMO-AGILE-50 | DD | Evalúo si la transformación genera valor sostenible para clientes, personas, organización y otros grupos de interés. | 0-5 |  |  |  |  |
| ITEM 163 | DEMO-AGILE-50 | DD | Comprendo capacidades, límites y riesgos básicos de la IA. | 0-5 |  |  |  |  |
| ITEM 164 | DEMO-AGILE-50 | DD | Selecciono herramientas según problema, contexto y sensibilidad de la información. | 0-5 |  |  |  |  |
| ITEM 165 | DEMO-AGILE-50 | DD | Distingo contenido generado por IA de información validada. | 0-5 |  |  |  |  |
| ITEM 166 | DEMO-AGILE-50 | DD | Formulo objetivos, contexto, restricciones y criterios de calidad. | 0-5 |  |  |  |  |
| ITEM 167 | DEMO-AGILE-50 | DD | Itero las instrucciones a partir de los resultados obtenidos. | 0-5 |  |  |  |  |
| ITEM 168 | DEMO-AGILE-50 | DD | Utilizo IA para analizar, sintetizar, crear, comparar y transformar información con propósito. | 0-5 |  |  |  |  |
| ITEM 169 | DEMO-AGILE-50 | DD | Contrasto resultados de IA antes de utilizarlos para decidir. | 0-5 |  |  |  |  |
| ITEM 170 | DEMO-AGILE-50 | DD | Detecto errores, sesgos, omisiones o respuestas plausibles pero incorrectas. | 0-5 |  |  |  |  |
| ITEM 171 | DEMO-AGILE-50 | DD | Solicito fuentes, evidencias o comprobaciones cuando el riesgo lo requiere. | 0-5 |  |  |  |  |
| ITEM 172 | DEMO-AGILE-50 | DD | Defino qué tareas realiza la persona y cuáles puede apoyar la IA. | 0-5 |  |  |  |  |
| ITEM 173 | DEMO-AGILE-50 | DD | Integro IA en dinámicas de equipo manteniendo responsabilidades explícitas. | 0-5 |  |  |  |  |
| ITEM 174 | DEMO-AGILE-50 | DD | Comparto buenas prácticas de uso de IA y reviso su impacto en el trabajo. | 0-5 |  |  |  |  |
| ITEM 175 | DEMO-AGILE-50 | DD | Identifico oportunidades de automatización con impacto potencial. | 0-5 |  |  |  |  |
| ITEM 176 | DEMO-AGILE-50 | DD | Prototipo soluciones pequeñas antes de escalar. | 0-5 |  |  |  |  |
| ITEM 177 | DEMO-AGILE-50 | DD | Mido beneficios, costes y riesgos de una automatización antes de consolidarla. | 0-5 |  |  |  |  |
| ITEM 178 | DEMO-AGILE-50 | DD | Protejo datos confidenciales, personales y estratégicos. | 0-5 |  |  |  |  |
| ITEM 179 | DEMO-AGILE-50 | DD | Considero privacidad, propiedad intelectual, sesgos, seguridad y trazabilidad. | 0-5 |  |  |  |  |
| ITEM 180 | DEMO-AGILE-50 | DD | Mantengo supervisión humana en decisiones donde el riesgo o la responsabilidad lo requieren. | 0-5 |  |  |  |  |
## Sheet: INDICADORES
| Indicadores |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Cada indicador pertenece a una versión concreta del test. |  |  |  |  |  |  |  |  |
| indicator_code | test_code | indicator_name | description | display_order | weight | min_score | max_score | active |
| ADA | DEMO-AGILE-12 | Adaptabilidad | Ajusta su forma de actuar ante cambios y nueva información. | 1 | 1 | 1 | 5 | True |
| COL | DEMO-AGILE-12 | Colaboración | Coopera, comparte información y construye con otras personas. | 2 | 1 | 1 | 5 | True |
| VAL | DEMO-AGILE-12 | Orientación a valor | Prioriza resultados útiles para clientes y organización. | 3 | 1 | 1 | 5 | True |
| APR | DEMO-AGILE-12 | Aprendizaje continuo | Aprende de la experiencia y convierte feedback en mejora. | 4 | 1 | 1 | 5 | True |
| IA | DEMO-AGILE-12 | Uso responsable de IA | Usa IA con criterio, verificación y protección de datos. | 5 | 1 | 1 | 5 | True |
## Sheet: OPCIONES_RESPUESTA
| Opciones de respuesta |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Catálogos de escala reutilizables. |  |  |  |  |  |  |  |
| scale_code | value | label | description | display_order |  |  |  |
| LIKERT5 | 1 | Nunca o casi nunca | La conducta rara vez está presente. | 1 |  |  |  |
| LIKERT5 | 2 | Pocas veces | Aparece de manera ocasional. | 2 |  |  |  |
| LIKERT5 | 3 | A veces | Aparece con una frecuencia intermedia. | 3 |  |  |  |
| LIKERT5 | 4 | A menudo | Aparece de forma habitual. | 4 |  |  |  |
| LIKERT5 | 5 | Siempre o casi siempre | Aparece de forma muy consistente. | 5 |  |  |  |
| LIKERT7 | 0 | Nunca | Consultar manual autorizado. | 1 |  |  |  |
| LIKERT7 | 1 | Casi nunca | Consultar manual autorizado. | 2 |  |  |  |
| LIKERT7 | 2 | Algunas veces | Consultar manual autorizado. | 3 |  |  |  |
| LIKERT7 | 3 | Regularmente | Consultar manual autorizado. | 4 |  |  |  |
| LIKERT7 | 4 | Bastantes veces | Consultar manual autorizado. | 5 |  |  |  |
| LIKERT7 | 5 | Casi siempre | Consultar manual autorizado. | 6 |  |  |  |
| LIKERT7 | 6 | Siempre | Consultar manual autorizado. | 7 |  |  |  |
## Sheet: REGLAS_PUNTUACION
| Reglas de puntuación |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Estas reglas deben verificarse manualmente antes del piloto. |  |  |  |  |  |  |  |  |  |
| rule_code | test_code | level | target_code | formula_type | formula_description | weight | round_decimals | scoring_version | active |
| R-IND-01 | DEMO-AGILE-12 | indicator | ALL | mean | Media de los ítems válidos del indicador, aplicando inversión cuando reverse_scored = true. | 1 | 2 | 1.0 | True |
| R-GLOBAL-01 | DEMO-AGILE-12 | global | GLOBAL | weighted_mean | Media ponderada de indicadores activos. Los cinco indicadores pesan igual en el demo. | 1 | 2 | 1.0 | True |
| R-REV-01 | DEMO-AGILE-12 | item | DEM-002;DEM-006 | reverse_1_5 | Puntuación invertida = 6 - respuesta. | 1 | 0 | 1.0 | True |
## Sheet: INTERPRETACIONES
| Interpretaciones |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Textos aprobados que alimentan el informe; la IA solo puede redactar dentro de estas reglas. |  |  |  |  |  |  |  |  |  |
| interpretation_code | test_code | target_code | min_score | max_score | level_name | approved_text | recommended_action | ai_allowed | active |
| INT-1 | DEMO-AGILE-12 | ALL | 1 | 1.79 | Inicial | La conducta evaluada aparece de forma poco consistente en las respuestas. | Elegir una conducta concreta y practicarla durante dos semanas. | True | True |
| INT-2 | DEMO-AGILE-12 | ALL | 1.8 | 2.59 | En desarrollo | La conducta aparece en algunas situaciones, pero todavía necesita apoyo o regularidad. | Definir una práctica observable y pedir feedback. | True | True |
| INT-3 | DEMO-AGILE-12 | ALL | 2.6 | 3.39 | Competente | La conducta está presente con una consistencia suficiente en situaciones habituales. | Consolidar la práctica y aplicarla en un reto real. | True | True |
| INT-4 | DEMO-AGILE-12 | ALL | 3.4 | 4.19 | Avanzado | La conducta está presente de forma habitual y se sostiene en situaciones más exigentes. | Compartir la práctica y ayudar a otra persona a desarrollarla. | True | True |
| INT-5 | DEMO-AGILE-12 | ALL | 4.2 | 5 | Referente | La conducta aparece de forma muy consistente y puede contribuir a desarrollar capacidad en el entorno. | Convertir la práctica en una referencia transferible al equipo. | True | True |
## Sheet: PLANTILLAS_EMAIL
| Plantillas de correo |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Variables entre llaves se sustituyen automáticamente. |  |  |  |  |  |  |  |
| template_code | event | language | subject | body_text | active |  |  |
| MAIL-INV-ES | invitation | es | Te invitamos a realizar {{test_name}} | Hola {{first_name}},

{{company_name}} te invita a realizar el test {{test_name}}. Podrás completarlo hasta el {{expires_at}}.

Accede aquí: {{test_link}}

El enlace es personal y no debe compartirse.

Gracias,
Agile Institute | True |  |  |
| MAIL-REM-ES | reminder | es | Recordatorio: tienes un test pendiente | Hola {{first_name}},

Hace tres días te enviamos el test {{test_name}} y todavía figura como pendiente. Puedes completarlo aquí: {{test_link}}

El enlace caduca el {{expires_at}}. Si ya lo has realizado, ignora este mensaje.

Gracias,
Agile Institute | True |  |  |
| MAIL-DONE-ES | completed | es | Tu informe de {{test_name}} ya está disponible | Hola {{first_name}},

Hemos recibido tus respuestas y tu informe ya está disponible.

Acceso seguro: {{report_link}}

Gracias,
Agile Institute | True |  |  |
| MAIL-INV-50 | completed | es | Invitación para realizar el test METACOMPETENCIAS ORGANIZACIÓN 5.0®.
 | Hola {{first_name}},

{{company_name}} te invita a realizar el test METACOMPETENCIAS ORGANIZACIÓN 5.0®.

El objetivo de este test es obtener información orientada al diagnóstico y desarrollo. Recuerda responder pensando en tu comportamiento real durante los últimos seis meses.

Podrás completar el test hasta el 08/11/2026.

Accede al test desde este enlace:
{{test_link}}

El enlace es personal, seguro y temporal. No lo compartas con otras personas.

Gracias por tu participación.

Agile Institute |  |  |  |
| MAIL-REC-50 | completed | es | Recordatorio: tienes un test pendiente de completar | Hola {{first_name}},

Te recordamos que tienes pendiente completar el test {{test_name}}.

Podrás realizarlo hasta el 08/11/2026.

Accede al test aquí:
{{test_link}}

El enlace es personal, seguro y temporal. No debe compartirse.

Gracias por tu participación.

Agile Institute |  |  |  |
| MAIL-DONE-50 | completed | es | Resultados de tu test METACOMPETENCIAS ORGANIZACIÓN 5.0®. | Hola {{first_name}},

Hemos recibido correctamente tus respuestas del test METACOMPETENCIAS ORGANIZACIÓN 5.0®.

Ya puedes consultar los resultados correspondientes a tu evaluación.

Consulta tus resultados aquí:
{{report_link}}

Gracias por tu participación.

Agile Institute |  |  |  |
## Sheet: INVITACIONES_DEMO
| Invitaciones de ejemplo |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Datos ficticios para probar estados, recordatorios y caducidad. |  |  |  |  |  |  |  |  |  |
| invitation_code | user_code | test_code | sent_at | expires_at | status | reminder_sent_at | completed_at | report_status | token_demo |
| INV-0001 | USR-0001 | DEMO-AGILE-12 | 2026-09-10 00:00:00 | 2026-10-10 00:00:00 | completed |  | 2026-09-12 00:00:00 | sent | TOKEN-NO-REAL-0001 |
| INV-0002 | USR-0002 | DEMO-AGILE-12 | 2026-09-10 00:00:00 | 2026-10-10 00:00:00 | completed | 2026-09-13 00:00:00 | 2026-09-13 00:00:00 | sent | TOKEN-NO-REAL-0002 |
| INV-0003 | USR-0003 | DEMO-AGILE-12 | 2026-09-20 00:00:00 | 2026-10-20 00:00:00 | pending |  |  | not_created | TOKEN-NO-REAL-0003 |
| INV-0004 | USR-0004 | DEMO-AGILE-12 | 2026-08-01 00:00:00 | 2026-08-31 00:00:00 | expired | 2026-08-04 00:00:00 |  | not_created | TOKEN-NO-REAL-0004 |
## Sheet: MAPA_IMPORTACION
| Mapa de importación a Base44 |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Correspondencia recomendada entre hojas y entidades. |  |  |  |  |  |  |  |
| order | sheet_name | base44_entity | primary_key | foreign_keys | import_mode | validation_before_import |  |
| 1 | USUARIOS | UserProfile | user_code |  | upsert | Email válido y user_code único |  |
| 2 | TESTS | TestDefinition | test_code |  | upsert | Código y versión únicos |  |
| 3 | FICHAS_TECNICAS | TestTechnicalSheet | test_code | test_code -> TestDefinition | upsert | Test existente y licencia revisada |  |
| 4 | INDICADORES | TestIndicator | indicator_code | test_code -> TestDefinition | upsert | Orden, pesos y rango válidos |  |
| 5 | ITEMS | TestItem | item_code | test_code; indicator_code | upsert | Escala existente y texto no vacío |  |
| 6 | OPCIONES_RESPUESTA | ResponseOption | scale_code + value |  | upsert | Valores sin duplicados |  |
| 7 | REGLAS_PUNTUACION | ScoringRule | rule_code | test_code; target_code | upsert | Fórmula y versión aprobadas |  |
| 8 | INTERPRETACIONES | InterpretationRule | interpretation_code | test_code; target_code | upsert | Rangos sin huecos ni solapes |  |
| 9 | PLANTILLAS_EMAIL | EmailTemplate | template_code |  | upsert | Variables reconocidas y prueba de envío |  |
## Sheet: DECISIONES_PENDIENTES
| Decisiones pendientes |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Deben aprobarse antes de pasar de datos ficticios a personas reales. |  |  |  |  |  |  |  |
| decision_code | decision | owner | deadline | status | notes |  |  |
| D-01 | Aprobar los test que entran en el piloto y comprobar sus licencias. | Antonio | Semana 2 | pending |  |  |  |
| D-02 | Aprobar fórmulas, rangos e interpretaciones de cada test. | Antonio | Semana 4 | pending |  |  |  |
| D-03 | Aprobar si el informe se envía como PDF adjunto o enlace seguro. | Antonio | Semana 5 | pending | Se recomienda enlace seguro con caducidad. |  |  |
| D-04 | Definir plazos de conservación y procedimiento de eliminación. | Privacidad | Antes del piloto | pending |  |  |  |
| D-05 | Aprobar el uso de IA y los textos de limitación. | Antonio + privacidad | Semana 6 | pending | La IA no modifica puntuaciones. |  |  |
| D-06 | Aprobar remitente y dominio de correo. | Antonio | Semana 3 | pending | Ejemplo: tests@agileinstitute.es |  |  |
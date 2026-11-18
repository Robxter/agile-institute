# Graph Report - Agile Institute  (2026-11-18)

## Corpus Check
- 62 files · ~465,526 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 16 file(s) not represented in the graph (top: .css 12, (none) 2, .db 1)

## Summary
- 1084 nodes · 2378 edges · 42 communities (39 shown, 3 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 232 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e4ccfcd2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- centro-de-mando/app/main.py
- centro-de-mando/app/seed.py
- Maestro v3.1 Competency Framework
- Excel Export v2
- Dashboard Service v1
- Frontend App v2
- Test Suite v2
- Frontend App v1
- Persona Dashboard Mockups
- Organizacion Dashboard Mockups
- MetaCompetencias Platform Spec
- Shared Dashboard Rules
- IA Dashboard Mockups
- centro-de-mando_v1_respaldo/app/seed.py
- landing.ts
- Equipo Dashboard Mockups
- Liderazgo Dashboard Mockups
- T03 Leadership & Flow Pulse
- Importable Excel Master
- Centro de Test Data Model
- package.json
- Preserved Master M_ Sheets
- Centro de Test MVP Stack
- T04 Organizacion Competencies
- T02 Equipo Competencies
- centro-de-mando/app/dashboard.py
- Chart Library
- T01 Persona Competencies
- Data Capture & Quality Sheets
- Scoring & AI Report Rules
- T05 IA Competencies
- Pulse & T05 Data Sheets
- Security & Acceptance Tests
- Evaluation Sources & Levels
- Product Owner Decisions
- index.mjs
- README Cuadros de mando por dimensión (v2)
- compilerOptions
- centro-de-mando/app/scoring.py
- catalog.py
- vite-env.d.ts

## God Nodes (most connected - your core abstractions)
1. `Maestro v3.1 (hojas M_, Agile Competences operativo para pilotaje)` - 34 edges
2. `Agile Competences Maestro v3.1 (pilotaje)` - 30 edges
3. `Scope` - 28 edges
4. `get_catalog()` - 24 edges
5. `README Cuadros de mando por dimensión (v2)` - 23 edges
6. `README Centro de mando v1 (Centro de Test)` - 23 edges
7. `Instructions v2: how the system works` - 20 edges
8. `Filters` - 19 edges
9. `Plataforma de Evaluación de MetaCompetencias Agile (MVP)` - 19 edges
10. `Catalog` - 18 edges

## Surprising Connections (you probably didn't know these)
- `Roles v2 (Administración, Consultor, RRHH, Líder, Participante, Gestor de test)` --semantically_similar_to--> `Roles v1 (Administrador, Gestor de test, Consultor, Visor)`  [INFERRED] [semantically similar]
  centro-de-mando/README.md → centro-de-mando_v1_respaldo/README.md
- `Agile_Competences_5_Cuadros_Diseno.xlsx (libro de diseño)` --semantically_similar_to--> `Excel Maestro Importable v1.0`  [INFERRED] [semantically similar]
  centro-de-mando/README.md → centro-de-mando_v1_respaldo/README.md
- `Confidencialidad: mínimo de grupo 5` --semantically_similar_to--> `Muestra mínima CDM_MIN_SAMPLE = 3`  [INFERRED] [semantically similar]
  centro-de-mando/README.md → centro-de-mando_v1_respaldo/README.md
- `Regla competencia 2 de 3 ítems y media descriptiva 6 de 8` --semantically_similar_to--> `Motor de puntuación determinista (inversión, media, redondeo, nivel)`  [INFERRED] [semantically similar]
  centro-de-mando/README.md → centro-de-mando_v1_respaldo/README.md
- `index.html v2 (Cuadros de mando)` --semantically_similar_to--> `index.html v1 (Centro de Test)`  [INFERRED] [semantically similar]
  centro-de-mando/static/index.html → centro-de-mando_v1_respaldo/static/index.html

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Pipeline de datos v1 (Excel maestro, seed, scoring, dashboard, API/Excel)** — centro_de_mando_v1_respaldo_app_seed, centro_de_mando_v1_respaldo_app_db, centro_de_mando_v1_respaldo_app_scoring, centro_de_mando_v1_respaldo_app_dashboard, centro_de_mando_v1_respaldo_app_main, centro_de_mando_v1_respaldo_app_export_xlsx [EXTRACTED 1.00]
- **Pipeline de datos v2 (catálogo, captura, scoring, cuadros, API/Excel)** — centro_de_mando_app_catalog, centro_de_mando_app_seed, centro_de_mando_app_importer, centro_de_mando_app_scoring, centro_de_mando_app_dashboard, centro_de_mando_app_main, centro_de_mando_app_export_xlsx [EXTRACTED 1.00]
- **Reglas de anonimato y calidad del libro de diseño** — centro_de_mando_readme_control_calidad, centro_de_mando_readme_regla_competencia_2_de_3, centro_de_mando_readme_confidencialidad_minimo_5, centro_de_mando_readme_pulso_enps, centro_de_mando_readme_demo_real_separation [EXTRACTED 1.00]
- **Pipeline calcular-interpretar-redactar del Centro de Test** — graphify_out_converted_documento_funcional_mvp_centro_de_test_v1_0_23092026__1__ad098a4b_entity_scoringrule, graphify_out_converted_documento_funcional_mvp_centro_de_test_v1_0_23092026__1__ad098a4b_entity_result, graphify_out_converted_documento_funcional_mvp_centro_de_test_v1_0_23092026__1__ad098a4b_entity_interpretationrule, graphify_out_converted_documento_funcional_mvp_centro_de_test_v1_0_23092026__1__ad098a4b_sintesis_ia, graphify_out_converted_documento_funcional_mvp_centro_de_test_v1_0_23092026__1__ad098a4b_informe_individual [EXTRACTED 1.00]
- **Anonymity threshold gates heatmap, participation and eNPS comments** — centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_equipo_2_umbral_anonimato, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_equipo_2_mapa_calor_respuestas, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_equipo_2_participacion, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_equipo_2_enps_equipo [EXTRACTED 1.00]
- **Orden de importación Excel maestro a entidades Base44** — graphify_out_converted_excel_maestro_importable_centro_de_test_mvp_v1_0_355ab3f8_sheet_usuarios, graphify_out_converted_excel_maestro_importable_centro_de_test_mvp_v1_0_355ab3f8_sheet_tests, graphify_out_converted_excel_maestro_importable_centro_de_test_mvp_v1_0_355ab3f8_sheet_fichas_tecnicas, graphify_out_converted_excel_maestro_importable_centro_de_test_mvp_v1_0_355ab3f8_sheet_indicadores, graphify_out_converted_excel_maestro_importable_centro_de_test_mvp_v1_0_355ab3f8_sheet_items, graphify_out_converted_excel_maestro_importable_centro_de_test_mvp_v1_0_355ab3f8_sheet_opciones_respuesta, graphify_out_converted_excel_maestro_importable_centro_de_test_mvp_v1_0_355ab3f8_sheet_reglas_puntuacion, graphify_out_converted_excel_maestro_importable_centro_de_test_mvp_v1_0_355ab3f8_sheet_interpretaciones, graphify_out_converted_excel_maestro_importable_centro_de_test_mvp_v1_0_355ab3f8_sheet_plantillas_email [EXTRACTED 1.00]
- **Cinco cuadros de mando con estructura comun (filtros, media descriptiva, confidencialidad, plan, pulso)** — graphify_out_converted_agile_competences_5_cuadros_diseno_804266f7_sheet_cm_persona, graphify_out_converted_agile_competences_5_cuadros_diseno_804266f7_sheet_cm_equipo, graphify_out_converted_agile_competences_5_cuadros_diseno_804266f7_sheet_cm_liderazgo, graphify_out_converted_agile_competences_5_cuadros_diseno_804266f7_sheet_cm_organizacion, graphify_out_converted_agile_competences_5_cuadros_diseno_804266f7_sheet_cm_ia [EXTRACTED 1.00]
- **Operational validity and privacy rules** — graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_rule_item_scale, graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_rule_min_2_of_3, graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_rule_coverage_70, graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_rule_privacy_min5, graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_rule_no_mix_versions, graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_no_global_index [EXTRACTED 1.00]
- **IA dashboard sections awaiting external or validated data** — centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_05_ia_propuesta_impacto_productividad_real, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_05_ia_propuesta_historico_benchmark, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_05_ia_propuesta_anclajes_escala, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_05_ia_propuesta_itinerario_desarrollo [EXTRACTED 1.00]
- **Ciclo de vida de la invitación (token, estados, recordatorio, caducidad)** — graphify_out_converted_documento_funcional_mvp_centro_de_test_v1_0_23092026__1__ad098a4b_enlace_seguro_token, graphify_out_converted_documento_funcional_mvp_centro_de_test_v1_0_23092026__1__ad098a4b_estados_invitacion, graphify_out_converted_documento_funcional_mvp_centro_de_test_v1_0_23092026__1__ad098a4b_recordatorio_3_dias, graphify_out_converted_documento_funcional_mvp_centro_de_test_v1_0_23092026__1__ad098a4b_automatizacion_diaria, graphify_out_converted_documento_funcional_mvp_centro_de_test_v1_0_23092026__1__ad098a4b_entity_invitation, graphify_out_converted_documento_funcional_mvp_centro_de_test_v1_0_23092026__1__ad098a4b_entity_emaillog [EXTRACTED 1.00]
- **Pulso de experiencia laboral: captura, items, calculo, eNPS y responsable** — graphify_out_converted_agile_competences_5_cuadros_diseno_804266f7_sheet_datos_pulso, graphify_out_converted_agile_competences_5_cuadros_diseno_804266f7_sheet_items_pulso, graphify_out_converted_agile_competences_5_cuadros_diseno_804266f7_sheet_calculo_pulso, graphify_out_converted_agile_competences_5_cuadros_diseno_804266f7_enps, graphify_out_converted_agile_competences_5_cuadros_diseno_804266f7_flow_experiencia_laboral, graphify_out_converted_agile_competences_5_cuadros_diseno_804266f7_percepcion_del_responsable [EXTRACTED 1.00]
- **Responsible reporting principles (anonymity, no global score, demo honesty)** — centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_organizaci_n_2_umbral_anonimato, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_04_organizacion_propuesta_sin_indice_global, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_04_organizacion_propuesta_pending_data_placeholders, centro_de_mando_instrumento_piloto_datos_demo [INFERRED 0.75]
- **Flujo captura -> control -> media descriptiva -> cuadro** — graphify_out_converted_agile_competences_5_cuadros_diseno_804266f7_sheet_datos_t01, graphify_out_converted_agile_competences_5_cuadros_diseno_804266f7_control_calidad, graphify_out_converted_agile_competences_5_cuadros_diseno_804266f7_media_descriptiva, graphify_out_converted_agile_competences_5_cuadros_diseno_804266f7_filtros_comunes, graphify_out_converted_agile_competences_5_cuadros_diseno_804266f7_minimo_confidencialidad, graphify_out_converted_agile_competences_5_cuadros_diseno_804266f7_sheet_cm_persona [INFERRED 0.85]
- **Team dashboard instrument lenses: T02, ECOL, Pulso, eNPS** — centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_02_equipo_propuesta_t02_contribucion_individual, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_02_equipo_propuesta_ecol_funcionamiento_colectivo, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_02_equipo_propuesta_pulso_experiencia_laboral, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_02_equipo_propuesta_enps_independiente [INFERRED 0.85]
- **Flow pulse pipeline (Catalogo -> Captura -> Calculo -> CM_Flow)** — graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_sheet_catalogo_flow, graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_sheet_captura_flow, graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_sheet_calculo_flow, graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_sheet_cm_flow, graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_enps, graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_leader_questions [INFERRED 0.85]
- **Competency test scoring pipeline (Captura -> Calculo -> CM_T)** — graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_sheet_guia_captura, graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_sheet_captura_tests, graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_sheet_calculo, graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_sheet_configuracion, graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_sheet_cm_t01, graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_sheet_cm_t02, graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_sheet_cm_t03, graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_sheet_cm_t04, graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_sheet_cm_t05, graphify_out_converted_maestro_de_origen_sin_modificar_d0be1079_sheet_cm_organizacion [INFERRED 0.85]
- **Indicator 6 scoring and global integration model** — centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_ia_transversal_2_indicador_6, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_ia_transversal_2_modelo_180_60_13_8, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_ia_transversal_2_integracion_global, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_ia_transversal_2_kpi_cards [INFERRED 0.85]
- **Leadership insight-to-action flow** — centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_liderazgo_2_brecha_equipo_autopercepcion, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_liderazgo_2_conversaciones_para_abrir, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_liderazgo_2_mi_plan_de_liderazgo [INFERRED 0.85]
- **Multi-source leadership perception (self, team, responsable, peers)** — centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_03_liderazgo_propuesta_evaluacion_360, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_liderazgo_2_fuentes_y_muestra, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_liderazgo_2_brecha_equipo_autopercepcion, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_liderazgo_2_umbral_anonimato [INFERRED 0.85]
- **Diagnose-prioritize-act loop in Organizacion dashboard** — centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_organizaci_n_2_ocho_indicadores, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_organizaci_n_2_prioridades, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_organizaci_n_2_planes_accion_3_meses, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_organizaci_n_2_evolucion [INFERRED 0.85]
- **Persona v1 competency result views (bars, radar, strengths, areas)** — centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_01_persona_propuesta_mis_competencias_bars, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_01_persona_propuesta_perfil_radar, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_01_persona_propuesta_fortalezas, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_01_persona_propuesta_areas_explorar, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_01_persona_propuesta_eight_competencies [INFERRED 0.85]
- **Data validity and transparency rules** — centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_personas_2_coverage_rule_70, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_personas_2_no_aplica_handling, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_personas_2_sobre_tus_datos, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_personas_2_development_not_selection [INFERRED 0.85]
- **Model 180/60/13/8 scoring hierarchy (items to competencies to metacompetencies and indicators)** — centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_personas_2_modelo_180_60_13_8, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_personas_2_competencias_dot_plot, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_personas_2_ocho_indicadores, centro_de_mando_mejora_cuadros_de_mando_ejemplo_5_ejemplos_cuadros_de_mando_propuesta_personas_2_trece_metacompetencias [INFERRED 0.85]

## Communities (42 total, 3 thin omitted)

### Community 0 - "centro-de-mando/app/main.py"
Cohesion: 0.10
Nodes (32): BadRequest, Forbidden, _layout_check(), layout_get(), layout_reset(), layout_save(), options(), overview() (+24 more)

### Community 1 - "centro-de-mando/app/seed.py"
Cohesion: 0.12
Nodes (20): Catalog, connect(), init_schema(), _cell(), ensure_people(), import_workbook(), insert_evaluation(), insert_pulse() (+12 more)

### Community 2 - "Maestro v3.1 Competency Framework"
Cohesion: 0.06
Nodes (72): Marco de 60 competencias de origen (13 metacompetencias), DOI 10.2307/2666999 (psychological safety), DOI 10.1027/1015-5759/a000430 (energia, implicacion), DOI 10.1108/02683940710733115 (feedback, autonomia), DOI 10.1016/j.jvb.2007.11.007 (concentracion, disfrute), DOI 10.1007/s11031-008-9102-4 (objetivos y reto-habilidad), eNPS (employee Net Promoter Score), Agrupaciones piloto T02 (EQ01-EQ08) (+64 more)

### Community 3 - "Excel Export v2"
Cohesion: 0.13
Nodes (20): build_workbook(), _header(), _sheet_cuadro(), _sheet_datos(), _sheet_detalle(), _sheet_pulso(), _sheet_traza(), _table() (+12 more)

### Community 4 - "Dashboard Service v1"
Cohesion: 0.09
Nodes (32): dashboard(), filter_options(), Filters, Forbidden, _indicators(), invitation_status(), item_responses(), _levels() (+24 more)

### Community 5 - "Frontend App v2"
Cohesion: 0.15
Nodes (38): api(), blockRows(), board(), boot(), competencesPanel(), currentFilters(), enpsPanel(), equipo() (+30 more)

### Community 6 - "Test Suite v2"
Cohesion: 0.06
Nodes (39): get_catalog(), client(), conn(), login(), scope(), test_all_seven_dashboards_build_for_admin(), test_block_needs_two_of_three_and_summary_six_of_eight(), test_catalog_has_five_tests_of_eight_blocks_and_pulse() (+31 more)

### Community 7 - "Frontend App v1"
Cohesion: 0.15
Nodes (32): api(), bindTips(), boot(), card(), chartActivity(), chartDist(), chartEvo(), chartMeans() (+24 more)

### Community 8 - "Persona Dashboard Mockups"
Cohesion: 0.10
Nodes (28): Persona Dashboard Proposal v1 (Mi resultado - Agilidad personal), Areas para explorar (Autorregulacion, Iniciativa), Data source: Base en Excel v3.0, Experiencia de trabajo y bienestar (Energia, Disfrute, Implicacion, Atencion, Seguridad psicologica), Condiciones de trabajo indicadores (Objetivos claros, Reto/habilidades, Feedback util), 8 Agility Competencies (Autoconciencia, Autorregulacion, Empatia, Mentalidad abierta, Incertidumbre, Iniciativa, Aprendizaje, Transferencia), Filters: Persona, Periodo, Tipo evaluacion (Autoinforme), Flow global y niveles A1-A5 (pending model definition) (+20 more)

### Community 9 - "Organizacion Dashboard Mockups"
Cohesion: 0.11
Nodes (19): Sidebar nav (Inicio, Organizacion, Personas, Equipos, Liderazgo, IA transversal), 04 Organizacion Propuesta (dashboard mockup), Bienestar y experiencia laboral - Pulso (Energia, Disfrute, Implicacion, Atencion, Seguridad psicologica), Cinco perfiles (Persona, Equipo, Liderazgo, Organizacion, IA transversal) medias 1-5, Cobertura de la propuesta (24 items / 8 competencias por ambito, Excel v3.0), Detalle organizativo T04 - 8 competencias, KPI cards: 120 items / 40 competencias / 12 personas / eNPS +40, Planes de accion (accion, responsable, fecha) (+11 more)

### Community 10 - "MetaCompetencias Platform Spec"
Cohesion: 0.15
Nodes (21): Evolución hacia MetaCompetencias (Incremento 1 y 2), Incremento 2: Plataforma MetaCompetencias, Roles: Administrador, Gestor de test, Consultor, Destinatario, Visor, Anexo A Plantilla de importación de usuarios (CSV), Anexo B Plantilla de importación del modelo, Cálculo jerárquico (comportamiento→competencia→MetaCompetencia→dimensión→global), Campaña de evaluación, Decisiones D 01-D 08 antes de programar el cálculo (+13 more)

### Community 11 - "Shared Dashboard Rules"
Cohesion: 0.17
Nodes (19): eNPS (indicador independiente), Filtros comunes (REAL/DEMO, equipo, periodo, organizacion, persona), Agile_Competences_Piloto_T04_Organizacion_5_0.xlsx (fuente), Plan de desarrollo editable (manual), CM_Equipo (cuadro de mando Equipo), CM_IA (cuadro de mando IA transversal), CM_Liderazgo (cuadro de mando Liderazgo), CM_Persona (cuadro de mando Persona) (+11 more)

### Community 12 - "IA Dashboard Mockups"
Cohesion: 0.13
Nodes (18): 05_IA_Propuesta (IA transversal dashboard mockup), Anclajes de escala (pending review), Base en Excel v3.0 (data source), Bienestar y experiencia - Pulso (Energia, Atencion, Implicacion, Seguridad psicologica), Competencias de IA 1-5 bar chart (8 competencies), Historico y benchmark (pending data), Itinerario de desarrollo (Objetivo > Practica > Evidencia > Revision), Lectura relativa de esta muestra (top 2 / areas a explorar) (+10 more)

### Community 13 - "centro-de-mando_v1_respaldo/app/seed.py"
Cohesion: 0.07
Nodes (36): connect(), init_schema(), get_conn(), compute_result(), interpret(), round_half_up(), scale_bounds(), scoring_config() (+28 more)

### Community 14 - "landing.ts"
Cohesion: 0.06
Nodes (51): ApiError, APP_URL, FieldErrors, PilotRequest, request(), submitPilotRequest(), App(), Assessment() (+43 more)

### Community 15 - "Equipo Dashboard Mockups"
Cohesion: 0.15
Nodes (18): 02_Equipo_Propuesta (Cuadro de mando Equipo, propuesta visual), Comparativas y benchmark (requiere datos y reglas de confidencialidad), Funcionamiento colectivo ECOL (18 items), eNPS independiente (+40), Plan de accion del equipo (por desarrollar), Experiencia laboral Pulso (bienestar, implicacion, seguridad psicologica), Contribucion individual al equipo T02 (8 dimensiones, escala 1-5), Propuesta_Equipo_2 (Cuadro de mando Equipos, vista Lider) (+10 more)

### Community 16 - "Liderazgo Dashboard Mockups"
Cohesion: 0.15
Nodes (18): Liderazgo Dashboard Proposal (03), Autopercepcion de liderazgo (8 competencies, 1-5), Benchmark y niveles (pending validation), Bienestar y experiencia del equipo, Condiciones que declaro generar, Evaluacion 360 (Auto, Equipo, Pares, Responsable), Base en Excel v3.0 (data source), Mi responsable - percepcion recibida (Pulso) (+10 more)

### Community 17 - "T03 Leadership & Flow Pulse"
Cohesion: 0.14
Nodes (18): Cultura de cuidado, Delegación y empoderamiento, Gestión de la complejidad, Gestión sostenible de la energía, Liderazgo compartido e influencia transversal, Seguridad psicológica, Condiciones de trabajo (F01-F04), Experiencias personales (F05-F08: energia, implicacion, atencion, disfrute) (+10 more)

### Community 18 - "Importable Excel Master"
Cohesion: 0.17
Nodes (18): Cuadros de mando y descarga Excel, Menú del producto (6 módulos), DEMO-AGILE-12 Demo Capacidades Ágiles (12 ítems, 5 indicadores), DEMO-AGILE-50 MetaCompetencias Organización 5.0® (180 ítems, piloto), Excel Maestro Importable Centro de Test MVP v1.0, EmailTemplate (entidad Base44), Indicadores ADA, COL, VAL, APR, IA, Plantillas MAIL-INV/REM/DONE (ES y 50) (+10 more)

### Community 19 - "Centro de Test Data Model"
Cohesion: 0.21
Nodes (17): Automatización diaria de caducidad, AuditEvent (entidad), Company (entidad), EmailLog (entidad), InterpretationRule (entidad), Invitation (entidad), Person (entidad), Response (entidad) (+9 more)

### Community 20 - "package.json"
Cohesion: 0.05
Nodes (47): dependencies, @fontsource-variable/montserrat@^5.1.0, react@^18.3.1, react-dom@^18.3.1, description, devDependencies, concurrently@^9.1.0, jsdom@^25.0.1 (+39 more)

### Community 21 - "Preserved Master M_ Sheets"
Cohesion: 0.19
Nodes (16): ECOL - modulo colectivo de equipo (complementario), Maestro v3.1 (hojas M_, Agile Competences operativo para pilotaje), Formulas_maestro (registro de formulas originales), M_Acciones - Registro manual de acciones, M_Banco original - Banco integro v2.1 (180 comportamientos), M_Calculo - Calculo activo desde Captura tests (100 evaluaciones), M_Captura tests - Captura tests (maestro), M_Catalogo tests - Catalogo operativo: ocho competencias por test (+8 more)

### Community 22 - "Centro de Test MVP Stack"
Cohesion: 0.19
Nodes (14): Agile Institute, Base44 Builder, Centro de Test (MVP), Documento Funcional MVP Centro de Test v1.0, Repositorio GitHub privado de Agile Institute, Paula (funcional y calidad), Plan de 8 semanas, Presupuesto MVP (2.300-4.800 € primer año) (+6 more)

### Community 23 - "T04 Organizacion Competencies"
Cohesion: 0.18
Nodes (14): Anticipación y adaptación al cambio, Calidad y mejora de procesos, Colaboración y cuidado en el cambio, Continuidad y aprendizaje ante incidentes, Coordinación y gestión del flujo, Decisiones y aprendizaje con evidencia, Gobernanza y responsabilidad ética, CM_Organizacion (cuadro de mando Organizacion) (+6 more)

### Community 24 - "T02 Equipo Competencies"
Cohesion: 0.15
Nodes (13): Aprendizaje y experimentación, Cliente y creación de valor, Comunicación y escucha, Cooperación y apoyo mutuo, Coordinación y responsabilidad compartida, Feedback y conflicto constructivo, Participación y autogestión responsable, Priorización y adaptación (+5 more)

### Community 25 - "centro-de-mando/app/dashboard.py"
Cohesion: 0.12
Nodes (33): Test, _bridges(), build(), _build_equipo(), _build_ia(), _build_liderazgo(), _build_liderazgo_ia(), _build_organizacion() (+25 more)

### Community 27 - "T01 Persona Competencies"
Cohesion: 0.20
Nodes (10): Actuación ante la incertidumbre, Aprendizaje deliberado y práctica reflexiva, Autoconciencia emocional, Autorregulación emocional, Empatía y comprensión del otro, Iniciativa y responsabilidad personal, Mentalidad abierta, Transferencia a nuevos contextos (+2 more)

### Community 28 - "Data Capture & Quality Sheets"
Cohesion: 0.27
Nodes (9): Escala FREC_1_5 (Nunca-Siempre), Datos_T01, Datos_T02, Datos_T03, Datos_T04, Items_T01, Items_T02, Items_T03 (+1 more)

### Community 29 - "Scoring & AI Report Rules"
Cohesion: 0.24
Nodes (7): Report (entidad), Result (entidad), ScoringRule (entidad), Informe individual estandarizado (web imprimible + PDF), Síntesis asistida por IA (con alternativa sin IA), Reglas R-IND-01 (media), R-GLOBAL-01 (media ponderada), R-REV-01 (6 - respuesta), Hoja REGLAS_PUNTUACION

### Community 30 - "T05 IA Competencies"
Cohesion: 0.25
Nodes (9): Alfabetización en datos e IA, Alfabetización en IA, Automatización y experimentación, Automatización y uso inteligente de tecnología, Colaboración humano-IA, IA responsable y ética, Interacción efectiva con IA, Pensamiento crítico aumentado (+1 more)

### Community 31 - "Pulse & T05 Data Sheets"
Cohesion: 0.29
Nodes (8): Escala NUM_1_5 (anclajes verbales pendientes), Calculo_Pulso, Datos_PULSO (captura pulso experiencia laboral), Datos_T05, Items_T05, M_Calculo Flow - Calculo Flow por componente, M_Captura Flow - Captura Flow (100 pulsos), M_CM_Flow - Cuadro Flow / experiencia laboral (maestro)

### Community 32 - "Security & Acceptance Tests"
Cohesion: 0.25
Nodes (7): Enlace seguro con token (hash, un solo uso, 30 días), Licencias de test de terceros, Pruebas de aceptación PA-01..PA-12, Seguridad, privacidad y propiedad intelectual (RGPD), Plan de construcción de 10 semanas, Pruebas de aceptación PA 01-PA 12, Seguridad y protección de datos (privacy by design)

### Community 33 - "Evaluation Sources & Levels"
Cohesion: 0.25
Nodes (7): Acciones de desarrollo y seguimiento, Agile Flow Maturity (A1-A5), Brechas y evolución, Escala de respuesta 1-5 (Inicial..Referente), Fuentes de evaluación AUTO/LIDER/PAR/EQUIPO/ORG/FLOW, Niveles Inicial/En desarrollo/Competente/Avanzado/Referente (1-1.79..4.2-5), Hoja INTERPRETACIONES (INT-1..INT-5)

### Community 35 - "Product Owner Decisions"
Cohesion: 1.00
Nodes (3): Antonio Cano García (Product Owner), Decisiones D-01..D-08 de Antonio, Hoja DECISIONES_PENDIENTES

### Community 36 - "index.mjs"
Cohesion: 0.11
Nodes (20): Arranque, Decisiones, Estructura, Front-end · Landing Agile Institute, Variables, cdmUrl(), DATA_DIR, DIST (+12 more)

### Community 37 - "README Cuadros de mando por dimensión (v2)"
Cohesion: 0.15
Nodes (20): Instructions v2: how the system works, README Cuadros de mando por dimensión (v2), Cuadro Equipo (T02), Cuadro IA transversal (T05), Cuadro mixto Líder + IA (T03+T05), Cuadro Liderazgo (T03 + L01–L03), Cuadro Organización (T04), Cuadro Persona (T01) (+12 more)

### Community 38 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, isolatedModules, jsx, lib, module, moduleResolution, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 39 - "centro-de-mando/app/scoring.py"
Cohesion: 0.26
Nodes (6): block_scores(), metadata_ok(), parse_raw(), recompute_all(), recompute_pulse(), recompute_test()

### Community 40 - "catalog.py"
Cohesion: 0.29
Nodes (5): _bool(), Item, load_catalog(), PulseItem, _rows()

## Ambiguous Edges - Review These
- `Modelo de MetaCompetencias Agile v3.0 (4/13/59/177)` → `DEMO-AGILE-50 MetaCompetencias Organización 5.0® (180 ítems, piloto)`  [AMBIGUOUS]
  graphify-out/converted/Excel_Maestro_Importable_Centro_de_Test_MVP_v1_0_355ab3f8.md · relation: conceptually_related_to
- `Indicador 6 - Inteligencia aumentada y colaboracion humano-IA (7 competencias, 21 items)` → `Competencias de IA 1-5 bar chart (8 competencies)`  [AMBIGUOUS]
  centro-de-mando/Mejora/CUADROS DE MANDO EJEMPLO 5/05_IA_Propuesta.png · relation: conceptually_related_to
- `Documento Funcional del MVP – Centro de Test v1.0` → `MVP Formación Agile Institute`  [AMBIGUOUS]
  Practicas.txt · relation: conceptually_related_to
- `Experiencia laboral Pulso (bienestar, implicacion, seguridad psicologica)` → `Los 8 indicadores del equipo (vs media Demo Corp)`  [AMBIGUOUS]
  centro-de-mando/Mejora/CUADROS DE MANDO EJEMPLO 5/02_Equipo_Propuesta.png · relation: conceptually_related_to
- `UWES (Utrecht Work Engagement Scale)` → `DOI 10.1027/1015-5759/a000430 (energia, implicacion)`  [AMBIGUOUS]
  graphify-out/converted/Maestro_de_origen_sin_modificar_d0be1079.md · relation: conceptually_related_to
- `WOLF (Work-reLated Flow inventory)` → `DOI 10.1016/j.jvb.2007.11.007 (concentracion, disfrute)`  [AMBIGUOUS]
  graphify-out/converted/Maestro_de_origen_sin_modificar_d0be1079.md · relation: conceptually_related_to
- `8 Agility Competencies (Autoconciencia, Autorregulacion, Empatia, Mentalidad abierta, Incertidumbre, Iniciativa, Aprendizaje, Transferencia)` → `Mis 8 indicadores (Agilidad e IA en puesto/equipo, Liderar con IA, Flow/bienestar, Decisiones, Inteligencia aumentada, Valor cliente, Comprension/aprendizaje)`  [AMBIGUOUS]
  centro-de-mando/Mejora/CUADROS DE MANDO EJEMPLO 5/EJEMPLOS CUADROS DE MANDO/Propuesta_Personas_2.png · relation: conceptually_related_to
- `Modelo 180/60/13/8 v2.1 piloto` → `Sin indice global ni puntuacion de madurez`  [AMBIGUOUS]
  centro-de-mando/Mejora/CUADROS DE MANDO EJEMPLO 5/04_Organizacion_Propuesta.png · relation: conceptually_related_to

## Knowledge Gaps
- **79 isolated node(s):** `Cuadro Equipo (T02)`, `Cuadro IA transversal (T05)`, `Cuadro Persona (T01)`, `Identidad visual Agile Institute (Montserrat, 0B3A4A, 1FA3A3)`, `Reglas de publicación y compartición de informes` (+74 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 249 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Distribución personalizable (user_layout)` connect `README Cuadros de mando por dimensión (v2)` to `centro-de-mando/app/main.py`, `Frontend App v2`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `Scope` (e.g. with `current_scope()` and `delete_layout()`) actually correct?**
  _`Scope` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Cuadro Equipo (T02)`, `Cuadro IA transversal (T05)`, `Cuadro Persona (T01)` to the rest of the system?**
  _79 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `centro-de-mando/app/main.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09713487071977638 - nodes in this community are weakly interconnected._
- **Why does `README Cuadros de mando por dimensión (v2)` connect `README Cuadros de mando por dimensión (v2)` to `centro-de-mando/app/main.py`, `centro-de-mando/app/seed.py`, `Excel Export v2`, `centro-de-mando/app/scoring.py`, `catalog.py`, `centro-de-mando_v1_respaldo/app/seed.py`, `centro-de-mando/app/dashboard.py`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Modelo de MetaCompetencias Agile v3.0 (4/13/59/177)` and `DEMO-AGILE-50 MetaCompetencias Organización 5.0® (180 ítems, piloto)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Indicador 6 - Inteligencia aumentada y colaboracion humano-IA (7 competencias, 21 items)` and `Competencias de IA 1-5 bar chart (8 competencies)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
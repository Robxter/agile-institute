<!-- converted from Documento_Funcional_MVP_Plataforma_MetaCompetencias_Agile_v1_0 (1).docx -->



Documento Funcional del MVP
Plataforma de Evaluación de MetaCompetencias Agile
Especificación para la construcción de una primera versión funcional, segura y escalable
| Campo | Información |
| --- | --- |
| Propietario | Agile Institute |
| Responsable funcional | Antonio Cano García |
| Modelo | MetaCompetencias Agile Versión 3.0 |
| Versión del documento | 1.0 |
| Fecha | 16 de septiembre de 2026 |
| Estado | Documento base para construcción y piloto |

Uso interno y para colaboradores autorizados del proyecto

# Control del documento
Este documento define qué debe hacer el producto mínimo viable, qué datos utilizará, cómo se calcularán y mostrarán los resultados y qué condiciones debe cumplir antes de trabajar con datos reales. Será la referencia común de Antonio Cano, las personas en prácticas, el apoyo técnico y cualquier proveedor que participe en el proyecto.
| Versión | Fecha | Responsable | Cambio |
| --- | --- | --- | --- |
| 1.0 | 16/09/2026 | Antonio Cano García | Primera especificación funcional del MVP |

## Decisión de producto
La primera versión validará si una organización puede configurar equipos, lanzar evaluaciones, calcular resultados fiables y obtener informes útiles sin intervención técnica. El MVP se construirá con una herramienta no code asistida por inteligencia artificial y con una arquitectura que permita exportar el código y migrar la solución si el volumen o los requisitos corporativos lo exigen.
# Contenido
- 1 Propósito y objetivos
- 2 Alcance del MVP
- 3 Modelo de evaluación
- 4 Usuarios y permisos
- 5 Procesos funcionales
- 6 Módulos y requisitos
- 7 Modelo de datos
- 8 Reglas de cálculo
- 9 Indicadores e informes
- 10 Seguridad y protección de datos
- 11 Experiencia de usuario
- 12 Requisitos no funcionales
- 13 Pruebas de aceptación
- 14 Plan de construcción
- 15 Riesgos y decisiones pendientes
- Anexos de campos y pruebas

# 1 Propósito y objetivos
El MVP permitirá medir y desarrollar las MetaCompetencias Agile de personas, equipos, líderes y organizaciones. El sistema debe administrar varias organizaciones de forma independiente, agrupar participantes por equipos, ejecutar campañas de evaluación y generar resultados que puedan consultarse y compartirse con seguridad.
## 1.1 Objetivos funcionales
- Centralizar el Modelo de MetaCompetencias Agile en una estructura digital versionable.
- Reducir el trabajo manual necesario para preparar cuestionarios, calcular resultados y crear informes.
- Ofrecer una lectura individual, de equipo, de liderazgo y organizativa.
- Incorporar Agile Flow Maturity como diagnóstico de equipo desde la primera fase.
- Permitir mediciones sucesivas para observar evolución y efecto de las acciones de desarrollo.
- Proteger la confidencialidad de las respuestas y separar los datos de cada organización.
- Comprobar la utilidad comercial y metodológica antes de invertir en un desarrollo a medida.
## 1.2 Indicadores de éxito del piloto
| Indicador | Criterio de éxito |
| --- | --- |
| Finalización | Al menos el 80 por ciento de los participantes completa la evaluación sin asistencia individual. |
| Exactitud | Los resultados automáticos coinciden con una comprobación manual sobre una muestra de respuestas. |
| Usabilidad | Un administrador crea una campaña, incorpora participantes y descarga informes siguiendo el manual. |
| Privacidad | Las pruebas confirman que ningún rol puede consultar información no autorizada. |
| Comprensión | Los usuarios entienden sus fortalezas y prioridades a partir del informe. |
| Escalabilidad | Se incorpora una segunda organización sin duplicar la aplicación ni las tablas del modelo. |

# 2 Alcance del MVP
## 2.1 Funcionalidades incluidas
- Alta, edición, desactivación y consulta de organizaciones.
- Alta e importación de usuarios y asignación a uno o varios equipos.
- Roles de Superadministrador, Administrador de organización, Consultor, Líder, Participante y Visor.
- Diccionario versionable de dimensiones, MetaCompetencias, competencias, comportamientos e ítems.
- Campañas de autoevaluación, evaluación de líder, equipo, organización y Agile Flow.
- Cuestionarios web adaptados a ordenador, tableta y móvil.
- Cálculo por comportamiento, competencia, MetaCompetencia, dimensión y resultado global.
- Lectura transversal de Inteligencia aumentada y colaboración humano IA.
- Dashboards individual, de equipo y organizativo.
- Informes imprimibles o guardables como PDF y exportación de datos autorizados a CSV.
- Comparación entre dos mediciones de la misma población.
- Registro básico de acciones de desarrollo y seguimiento.
## 2.2 Funcionalidades fuera del MVP
- Aplicaciones nativas para iOS o Android.
- Facturación, pagos, licencias automáticas y tienda de servicios.
- Integraciones con SAP, Workday, SuccessFactors u otros sistemas de recursos humanos.
- Inicio de sesión corporativo SSO y aprovisionamiento automático SCIM.
- Benchmark sectorial externo o comparación con una norma poblacional.
- Interpretaciones clínicas, diagnósticos psicológicos o decisiones laborales automatizadas.
- Generación automática de recomendaciones mediante modelos de IA con datos personales.
- Evaluación 360 completa con reglas avanzadas de nominación y calibración.
- Aplicación multilingüe, salvo preparación técnica para incorporar traducciones posteriormente.
## 2.3 Supuestos de partida
El MVP se probará inicialmente con una organización, dos equipos y entre 20 y 40 participantes. El cuestionario, los pesos y los textos interpretativos serán aprobados por Antonio Cano antes de su publicación. Durante el desarrollo solo se utilizarán datos ficticios. Los resultados del modelo se presentarán como diagnóstico para el desarrollo y no como prueba psicométrica estandarizada hasta completar su validación empírica.
# 3 Modelo de evaluación
La plataforma utilizará como fuente oficial la versión 3.0 del Modelo de MetaCompetencias Agile de Agile Institute. La arquitectura funcional debe almacenar el modelo en la base de datos, sin escribir nombres, preguntas o pesos directamente en las pantallas. De este modo se podrán publicar nuevas versiones sin reconstruir la aplicación.
| Nivel | Contenido | Cantidad vigente |
| --- | --- | --- |
| 1 | Dimensiones Persona, Equipo, Líder y Organización | 4 |
| 2 | MetaCompetencias Agile | 13 |
| 3 | Competencias asociadas | 59 |
| 4 | Comportamientos observables | 177 |
| 5 | Ítems o preguntas de evaluación | Configurable |

## 3.1 MetaCompetencia transversal
Inteligencia aumentada y colaboración humano IA se almacenará como la MetaCompetencia 13 y se mostrará como una capa transversal. No constituye una quinta dimensión. Su puntuación aparecerá separada en los informes y no se sumará dos veces al resultado global.
## 3.2 Escala de respuesta
| Valor | Nivel | Descriptor general |
| --- | --- | --- |
| 1 | Inicial | La competencia aparece ocasionalmente o necesita apoyo frecuente. |
| 2 | En desarrollo | La aplica con apoyo en situaciones conocidas. |
| 3 | Competente | La aplica de forma autónoma y consistente. |
| 4 | Avanzado | La aplica en situaciones complejas y ayuda a otras personas. |
| 5 | Referente | Genera capacidad en otras personas y transforma el sistema. |

## 3.3 Fuentes de evaluación
| Código | Fuente | Uso en el MVP |
| --- | --- | --- |
| AUTO | Autoevaluación | Obligatoria en campañas individuales. |
| LIDER | Evaluación del líder | Opcional para persona y liderazgo. |
| PAR | Evaluación entre pares | Preparada, pero limitada en el MVP. |
| EQUIPO | Percepción del equipo | Agregada y sujeta a umbral de anonimato. |
| ORG | Percepción organizativa | Agregada por organización o área. |
| FLOW | Agile Flow Maturity | Diagnóstico específico de equipo. |

# 4 Usuarios y permisos
| Rol | Responsabilidad | Acceso principal |
| --- | --- | --- |
| Superadministrador | Gobierna la plataforma y el modelo. | Todas las organizaciones, configuraciones y auditoría. |
| Administrador de organización | Gestiona usuarios, equipos y campañas. | Solo su organización y resultados autorizados. |
| Consultor | Acompaña campañas asignadas. | Organizaciones, campañas e informes asignados. |
| Líder | Participa y consulta su ámbito. | Informe propio y resultados agregados de sus equipos. |
| Participante | Responde evaluaciones. | Cuestionarios e informes personales autorizados. |
| Visor | Consulta un resultado concreto. | Informes o dashboards expresamente compartidos. |

## 4.1 Reglas obligatorias de acceso
- Cada registro funcional deberá incluir el identificador de la organización cuando corresponda.
- Un usuario de una organización no podrá buscar, visualizar ni exportar datos de otra.
- El líder verá datos de equipo agregados, no respuestas individuales de sus miembros.
- Los resultados colectivos no se mostrarán si el número de participantes válidos es inferior al umbral configurado. El valor inicial será cinco.
- Un informe compartido mediante enlace tendrá destinatario, fecha de caducidad y posibilidad de revocación.
- Los cambios de rol, exportaciones y accesos administrativos quedarán registrados.
## 4.2 Matriz resumida de permisos
| Acción | Superadmin | Admin org | Consultor | Líder | Participante |
| --- | --- | --- | --- | --- | --- |
| Gestionar modelo | Sí | No | No | No | No |
| Gestionar organización | Sí | Sí propia | No | No | No |
| Gestionar equipos | Sí | Sí propia | Según asignación | No | No |
| Crear campaña | Sí | Sí propia | Según asignación | No | No |
| Responder | Si está invitado | Si está invitado | Si está invitado | Sí | Sí |
| Ver informe propio | Según política | Según política | Según política | Sí | Sí |
| Ver agregado equipo | Sí | Sí | Según asignación | Sí propio | No |
| Exportar datos | Sí | Agregados | Agregados | No | No |

# 5 Procesos funcionales
## 5.1 Preparación de una organización
- El Superadministrador crea la organización y designa a su administrador.
- El administrador completa los datos básicos, áreas y equipos.
- Los usuarios se cargan manualmente o mediante una plantilla CSV.
- El sistema valida correos duplicados, equipos inexistentes y campos obligatorios.
- El administrador revisa la vista previa y confirma la importación.
## 5.2 Creación y ejecución de una campaña
- El administrador selecciona organización, versión del modelo y tipo de evaluación.
- Define equipos, participantes, fuentes, fechas, anonimato y disponibilidad de informes.
- El sistema muestra una vista previa y ejecuta validaciones antes de publicar.
- Los participantes reciben una invitación personal con acceso seguro.
- El dashboard de seguimiento muestra invitaciones, accesos y cuestionarios completados.
- Al cerrar la campaña se bloquean respuestas y se calculan los resultados definitivos.
- Los informes se revisan y se publican para los destinatarios autorizados.
## 5.3 Experiencia del participante
- Accede con su cuenta o enlace de invitación verificado.
- Lee la finalidad, confidencialidad y tiempo estimado antes de comenzar.
- Responde por bloques y puede guardar para continuar más tarde.
- El sistema impide enviar el cuestionario si faltan respuestas obligatorias.
- Recibe confirmación de envío y consulta su informe cuando sea publicado.
## 5.4 Cierre y seguimiento
Tras publicar los resultados, el usuario puede seleccionar fortalezas, prioridades y acciones. Cada acción incluirá descripción, responsable, fecha objetivo, estado y evidencia opcional. Una medición posterior podrá compararse con la anterior cuando ambas utilicen una versión compatible del modelo.
# 6 Módulos y requisitos
| ID | Módulo | Requisito | Aceptación principal |
| --- | --- | --- | --- |
| RF 01 | Acceso y autenticación | Registrar, invitar, autenticar, recuperar contraseña y cerrar sesión. | El usuario solo accede a las pantallas permitidas por su rol. |
| RF 02 | Organizaciones | Crear, editar, desactivar y consultar organizaciones independientes. | Los datos de una organización nunca aparecen en otra. |
| RF 03 | Equipos y áreas | Crear jerarquías simples y asignar miembros y líderes. | Un usuario puede pertenecer a varios equipos sin duplicarse. |
| RF 04 | Usuarios | Alta manual, invitación e importación CSV. | La importación muestra errores antes de guardar. |
| RF 05 | Modelo | Administrar versiones, dimensiones, MetaCompetencias, competencias, comportamientos e ítems. | Una versión publicada queda bloqueada para conservar la trazabilidad. |
| RF 06 | Campañas | Configurar alcance, participantes, fuentes, fechas y reglas de publicación. | No se publica una campaña con configuración incompleta. |
| RF 07 | Cuestionarios | Presentar ítems por bloques, guardar avance y enviar respuestas. | El envío final genera un registro único y bloquea la edición. |
| RF 08 | Cálculo | Calcular puntuaciones y brechas con reglas versionadas. | Una prueba manual reproduce el resultado mostrado. |
| RF 09 | Dashboards | Mostrar participación, resultados, fortalezas, brechas, dispersión y evolución. | Cada gráfico respeta permisos y umbrales de anonimato. |
| RF 10 | Informes | Generar vistas individuales, de equipo, liderazgo y organización. | El informe imprimible conserva gráficos, textos y fecha de generación. |
| RF 11 | Acciones | Registrar prioridades, compromisos y seguimiento. | La acción conserva historial básico de estado. |
| RF 12 | Notificaciones | Enviar invitaciones, recordatorios y confirmaciones. | No se envían correos duplicados en una misma ejecución. |
| RF 13 | Exportaciones | Exportar datos autorizados a CSV y guardar informes como PDF. | La exportación aplica filtros de organización y rol. |
| RF 14 | Auditoría | Registrar accesos administrativos y cambios relevantes. | El registro identifica usuario, fecha, acción y objeto. |

## 6.1 Requisitos de las pantallas
| Pantalla | Contenido mínimo |
| --- | --- |
| Inicio de sesión | Correo, contraseña, recuperación y aceptación de condiciones. |
| Inicio participante | Evaluaciones pendientes, completadas e informes publicados. |
| Panel administrador | Organizaciones o ámbito propio, campañas, alertas y participación. |
| Organización | Ficha, administradores, áreas, equipos, usuarios y configuración. |
| Equipo | Miembros, líder, campañas, indicadores y evolución. |
| Modelo | Versiones, jerarquía, pesos, ítems, importación y validación. |
| Campaña | Asistente de creación, participantes, calendario, estado y cierre. |
| Cuestionario | Progreso, escala visible, guardado y envío. |
| Resultados | Filtros, gráficos, interpretación y comparación. |
| Informe | Vista imprimible, metadatos, alcance y fecha. |
| Administración | Roles, plantillas, umbrales, auditoría y configuración. |

## 6.2 Estados de campaña
| Estado | Descripción | Acciones permitidas |
| --- | --- | --- |
| Borrador | Configuración en curso. | Editar, validar y eliminar. |
| Programada | Validada y pendiente de apertura. | Modificar fechas o cancelar. |
| Activa | Acepta respuestas. | Invitar, recordar, consultar participación y cerrar. |
| Cerrada | No acepta nuevas respuestas. | Calcular, revisar y reabrir con autorización. |
| Publicada | Informes disponibles. | Consultar, compartir, revocar y archivar. |
| Archivada | Conservación sin uso operativo. | Consultar según permisos. |

# 7 Modelo de datos
La estructura debe utilizar identificadores internos estables y relaciones entre tablas. Los nombres visibles pueden cambiar, pero los resultados históricos deben seguir vinculados a la versión exacta del modelo y a la campaña en la que se generaron.
| Entidad | Campos funcionales principales |
| --- | --- |
| Organización | organization_id, nombre, logo, sector, país, estado |
| Área | area_id, organization_id, nombre, responsable |
| Equipo | team_id, organization_id, area_id, nombre, líder, estado |
| Usuario | user_id, correo, nombre, idioma, estado |
| Membresía | user_id, organization_id, team_id, rol, fecha inicio y fin |
| Versión del modelo | model_version_id, nombre, fecha, estado |
| Dimensión | dimension_id, model_version_id, código, nombre, orden |
| MetaCompetencia | meta_id, dimensión opcional, transversal, peso, orden |
| Competencia | competency_id, meta_id, código, nombre, peso |
| Comportamiento | behavior_id, competency_id, código, descriptor |
| Ítem | item_id, behavior_id, texto, fuente, obligatorio, estado |
| Campaña | campaign_id, organization_id, model_version_id, tipo, fechas, estado |
| Asignación | assignment_id, campaign_id, sujeto, evaluador, fuente, estado |
| Respuesta | response_id, assignment_id, item_id, valor, comentario, fecha |
| Resultado | result_id, campaign_id, sujeto, nivel, objeto, puntuación, n |
| Informe | report_id, campaña, tipo, destinatario, versión, fecha, estado |
| Acción | action_id, sujeto, prioridad, descripción, responsable, fecha, estado |
| Auditoría | audit_id, usuario, fecha, acción, objeto, resultado |

## 7.1 Reglas de integridad
- No se elimina físicamente una organización, campaña o versión del modelo con resultados asociados. Se desactiva o archiva.
- El correo será único por usuario, aunque una persona pueda pertenecer a varias organizaciones si el modelo comercial lo requiere.
- Una respuesta siempre pertenecerá a una asignación, un ítem y una campaña.
- El sistema rechazará valores fuera de la escala activa.
- Los resultados se recalcularán desde las respuestas o conservarán la versión de fórmula utilizada.
- La importación del modelo verificará que existen 4 dimensiones, 13 MetaCompetencias, 59 competencias y 177 comportamientos en la versión 3.0.
# 8 Reglas de cálculo
## 8.1 Cálculo jerárquico
El motor calculará de abajo arriba. La puntuación de un comportamiento será la media de sus ítems válidos. La competencia será la media ponderada de sus comportamientos; la MetaCompetencia, la media ponderada de sus competencias; y la dimensión, la media ponderada de sus MetaCompetencias. Los pesos serán configurables y, mientras no se aprueben otros, se aplicarán pesos iguales.
| Nivel | Regla inicial del MVP |
| --- | --- |
| Comportamiento | Media aritmética de los ítems válidos asociados. |
| Competencia | Media ponderada de comportamientos válidos. |
| MetaCompetencia | Media ponderada de competencias válidas. |
| Dimensión | Media ponderada de MetaCompetencias no transversales. |
| Global | Media ponderada de las cuatro dimensiones. |
| IA transversal | Cálculo independiente y presentación separada. |

## 8.2 Datos incompletos
- Los ítems obligatorios deberán estar respondidos antes del envío.
- Si se permiten ítems no aplicables, el cálculo excluirá esos valores del denominador.
- No se calculará un nivel si no se alcanza el porcentaje mínimo de respuestas configurado. El valor inicial será 80 por ciento.
- El informe indicará cuando una puntuación se basa en una muestra reducida o incompleta.
## 8.3 Combinación de fuentes
El MVP mostrará por separado la autoevaluación y las fuentes externas. También podrá presentar una puntuación combinada cuando los pesos hayan sido aprobados para esa campaña. No se aplicará una ponderación oculta. El informe deberá mostrar siempre qué fuentes intervienen y cuántas respuestas sustentan el resultado.
## 8.4 Niveles Agile Flow Maturity
| Rango inicial | Nivel | Denominación |
| --- | --- | --- |
| 1,00 a 1,79 | A1 | Controla |
| 1,80 a 2,59 | A2 | Dirige |
| 2,60 a 3,39 | A3 | Adapta |
| 3,40 a 4,19 | A4 | Innova y aprende |
| 4,20 a 5,00 | A5 | Impacta y trasciende |

Estos puntos de corte son parámetros iniciales de producto. Deberán revisarse a partir del pilotaje y del proceso de validación del instrumento.
## 8.5 Brechas y evolución
| Indicador | Cálculo |
| --- | --- |
| Brecha auto externa | Puntuación externa menos autoevaluación. |
| Brecha actual objetivo | Nivel esperado menos nivel actual. |
| Evolución absoluta | Puntuación posterior menos puntuación inicial. |
| Evolución porcentual | Evolución absoluta dividida por la puntuación inicial, cuando sea válida. |
| Dispersión de equipo | Desviación estándar o rango intercuartílico de respuestas agregadas. |

# 9 Indicadores e informes
## 9.1 Indicadores operativos
- Personas invitadas, activadas, iniciadas y finalizadas.
- Porcentaje de participación total y por equipo.
- Tiempo medio y mediano de finalización.
- Campañas abiertas, cerradas y publicadas.
- Errores de invitación y usuarios sin equipo.
## 9.2 Indicadores de evaluación
- Puntuación por dimensión, MetaCompetencia, competencia y comportamiento.
- Nivel Agile Flow Maturity A1 a A5.
- Fortalezas y prioridades de desarrollo.
- Diferencia entre fuentes.
- Dispersión y consistencia dentro del equipo.
- Comparación entre equipos, siempre con datos agregados.
- Evolución entre mediciones compatibles.
- Puntuación transversal de inteligencia aumentada y colaboración humano IA.
## 9.3 Informe individual
El informe individual incluirá identificación, campaña, fecha, fuentes utilizadas, radar de dimensiones, resultados por MetaCompetencia, IA transversal, fortalezas, prioridades y plan de desarrollo. Si existen varias fuentes, diferenciará visualmente la autopercepción y la percepción externa. No incluirá comparaciones nominales con otras personas.
## 9.4 Informe de equipo
El informe de equipo presentará participación, radar colectivo, mapa de calor, fortalezas, prioridades, dispersión, Agile Flow, IA transversal y evolución. Solo se generará cuando se alcance el umbral mínimo de anonimato. Los filtros que reduzcan el grupo por debajo del umbral quedarán bloqueados.
## 9.5 Informe de liderazgo
El informe de liderazgo mostrará las MetaCompetencias aplicables, la diferencia entre percepción propia y del equipo, y su relación descriptiva con autonomía, colaboración, bienestar y flow. Las relaciones serán interpretativas y no se presentarán como causalidad demostrada.
## 9.6 Informe organizativo
El informe organizativo agregará resultados por dimensión, MetaCompetencia, área y equipo. Incluirá madurez, brechas, dispersión, evolución, IA transversal y prioridades. El sistema impedirá bajar a un nivel que permita identificar respuestas individuales.
## 9.7 Reglas de publicación y compartición
- Los informes se generan inicialmente en estado Borrador.
- Un usuario autorizado debe revisar y publicar cada informe.
- El PDF mostrará versión del modelo, campaña, fecha y alcance de los datos.
- Los enlaces compartidos serán revocables y tendrán caducidad.
- Las exportaciones de datos detallados quedarán reservadas al Superadministrador y estarán registradas.
# 10 Seguridad y protección de datos
La plataforma manejará información identificable sobre competencias y percepciones profesionales. La protección de datos debe incorporarse desde el diseño y no añadirse al terminar. Antes del piloto con personas reales, Agile Institute deberá aprobar la finalidad, las bases de legitimación, los periodos de conservación, la información a participantes y los contratos con proveedores.
## 10.1 Requisitos mínimos
| Control | Requisito |
| --- | --- |
| Separación organizativa | Filtros y reglas de acceso aplicados en servidor o base de datos, no solo en la interfaz. |
| Mínimo privilegio | Cada rol recibe únicamente los permisos necesarios. |
| Cifrado | Datos cifrados en tránsito y en reposo por el proveedor. |
| Contraseñas | Gestionadas por el sistema de autenticación; nunca visibles para administradores. |
| Auditoría | Registro de cambios de rol, exportaciones, publicación y acceso administrativo. |
| Anonimato | Umbral inicial de cinco respuestas para resultados colectivos. |
| Conservación | Plazos configurables y procedimiento documentado de eliminación. |
| Copias | Copias de seguridad y procedimiento de recuperación comprobado. |
| Incidencias | Canal y procedimiento para comunicar y gestionar brechas. |
| Pruebas | Revisión de permisos con cada rol y escaneo de seguridad antes de publicar. |

## 10.2 Reglas durante el desarrollo
- Utilizar exclusivamente usuarios y respuestas ficticias.
- No copiar bases de datos de clientes en el entorno de pruebas.
- Conceder acceso de edición solo a las personas que construyen la aplicación.
- Mantener las cuentas principales, el dominio y el repositorio bajo propiedad de Agile Institute.
- Retirar accesos al finalizar las prácticas o la colaboración.
- No introducir información personal en prompts externos salvo autorización y contrato adecuados.
# 11 Experiencia de usuario
La interfaz utilizará la identidad visual de Agile Institute: Montserrat, azul oscuro 0B3A4A, turquesa 1FA3A3, gris 2B2B2B, blanco y gris claro F4F7F8. La estética será profesional y sobria, con prioridad para la lectura y la comprensión de resultados.
## 11.1 Principios de diseño
- Cada pantalla tendrá una acción principal reconocible.
- Los términos del modelo se utilizarán de forma consistente.
- El cuestionario mostrará avance y permitirá continuar más tarde.
- La escala de respuesta incluirá número, nombre y descriptor cuando resulte necesario.
- Los errores indicarán qué debe corregirse y conservarán la información ya introducida.
- Los gráficos siempre estarán acompañados por valores y una explicación breve.
- El color no será el único recurso para comunicar diferencias.
- Las pantallas funcionarán con teclado y mantendrán contraste y tamaños legibles.
## 11.2 Navegación por rol
| Rol | Menú inicial |
| --- | --- |
| Superadministrador | Resumen, organizaciones, modelo, campañas, informes, usuarios, auditoría y configuración. |
| Administrador | Resumen, equipos, usuarios, campañas, resultados e informes. |
| Consultor | Organizaciones asignadas, campañas, seguimiento e informes. |
| Líder | Mis evaluaciones, mi informe, mis equipos y acciones. |
| Participante | Mis evaluaciones, mis resultados y mi plan. |
| Visor | Informes compartidos. |

# 12 Requisitos no funcionales
| ID | Área | Requisito del MVP |
| --- | --- | --- |
| RNF 01 | Rendimiento | Las pantallas habituales deben cargar en un tiempo aceptable con 500 usuarios y 50 usuarios concurrentes en el piloto ampliado. |
| RNF 02 | Disponibilidad | El proveedor gestionará alojamiento, certificados y operación básica. |
| RNF 03 | Compatibilidad | Últimas versiones de Chrome, Edge, Safari y Firefox. |
| RNF 04 | Adaptación | Uso completo en ordenador y tableta; cuestionarios utilizables en móvil. |
| RNF 05 | Accesibilidad | Contraste, etiquetas, navegación por teclado y textos alternativos cuando proceda. |
| RNF 06 | Trazabilidad | Versión del modelo y fórmula asociadas a cada resultado. |
| RNF 07 | Portabilidad | Exportación periódica de datos y sincronización del código con un repositorio de Agile Institute. |
| RNF 08 | Mantenibilidad | Configuración del modelo y textos sin modificar código. |
| RNF 09 | Idioma | Español en el MVP y estructura preparada para traducciones. |
| RNF 10 | Calidad | No se publica una función sin caso de prueba y validación funcional. |

# 13 Pruebas de aceptación
Las personas en prácticas registrarán cada prueba, el resultado obtenido, la evidencia y la incidencia asociada. La versión no podrá pilotarse con datos reales mientras exista un error crítico de permisos, pérdida de respuestas o cálculo incorrecto.
| ID | Área | Prueba | Resultado esperado |
| --- | --- | --- | --- |
| PA 01 | Separación | Crear dos organizaciones y verificar que sus administradores no ven datos cruzados. | Sin acceso cruzado. |
| PA 02 | Importación | Cargar un CSV con filas correctas, duplicadas e incompletas. | Vista previa y errores identificados. |
| PA 03 | Equipos | Asignar una persona a dos equipos. | Una cuenta y dos membresías. |
| PA 04 | Campaña | Crear, validar, activar, cerrar y publicar. | Transiciones correctas. |
| PA 05 | Guardado | Responder parcialmente, salir y volver. | Se conserva el avance. |
| PA 06 | Envío | Intentar enviar con respuestas obligatorias vacías. | El sistema bloquea y señala faltantes. |
| PA 07 | Cálculo | Comparar una muestra con cálculo manual. | Coincidencia dentro del redondeo. |
| PA 08 | Anonimato | Consultar un grupo con cuatro respuestas. | No se muestra el resultado. |
| PA 09 | Informe | Imprimir o guardar como PDF. | Sin cortes ni datos omitidos. |
| PA 10 | Permisos | Probar cada rol contra acciones autorizadas y denegadas. | Matriz cumplida. |
| PA 11 | Evolución | Comparar dos campañas compatibles. | Diferencias y fechas correctas. |
| PA 12 | Auditoría | Cambiar rol y exportar. | Ambas acciones quedan registradas. |

## 13.1 Clasificación de incidencias
| Nivel | Definición | Decisión |
| --- | --- | --- |
| Crítica | Acceso indebido, pérdida de datos, cálculo incorrecto general o imposibilidad de completar la evaluación. | Bloquea el piloto. |
| Alta | Función principal defectuosa sin alternativa razonable. | Debe corregirse antes del piloto. |
| Media | Problema con alternativa o impacto limitado. | Se corrige o acepta expresamente. |
| Baja | Detalle visual, texto o mejora menor. | Puede pasar a la siguiente iteración. |

# 14 Plan de construcción
| Semana | Bloque | Trabajo | Entregable |
| --- | --- | --- | --- |
| 1 | Preparación | Formación básica, revisión del documento, cuentas y tablero. | Entorno preparado y backlog aprobado. |
| 2 | Prototipo | Navegación, pantallas y datos ficticios. | Prototipo validado. |
| 3 | Organización | Organizaciones, usuarios, equipos, roles e importación. | Administración operativa. |
| 4 | Modelo | Carga y validación de la versión 3.0. | Diccionario versionado. |
| 5 | Evaluación | Campañas, asignaciones y cuestionarios. | Flujo completo de respuesta. |
| 6 | Cálculo | Motor de resultados y comprobación manual. | Resultados validados. |
| 7 | Paneles | Dashboards e indicadores. | Vistas por rol. |
| 8 | Informes | Informes, PDF, CSV y acciones. | Salidas compartibles. |
| 9 | Calidad | Pruebas, permisos, privacidad y correcciones. | Versión candidata. |
| 10 | Piloto | Carga real controlada, soporte y evaluación. | Informe de decisión. |

## 14.1 Organización del trabajo
El trabajo se gestionará en un tablero con los estados Pendiente, Esta semana, En construcción, En pruebas, Validado por Antonio y Terminado. Cada tarea tendrá una descripción, responsable, criterios de aceptación y evidencia. Ninguna función se considerará terminada por estar visualmente construida; deberá superar su prueba.
## 14.2 Responsabilidades
| Responsable | Decide o ejecuta |
| --- | --- |
| Antonio Cano | Aprueba alcance, modelo, preguntas, fórmulas, textos interpretativos e informes. |
| Prácticas funcional | Prepara contenidos, datos ficticios, pruebas, incidencias y manual. |
| Prácticas no code | Configura datos, pantallas, flujos, permisos, cálculos y paneles. |
| Tutor técnico | Revisa arquitectura, seguridad, permisos, rendimiento y portabilidad. |
| Asesor de privacidad | Revisa tratamiento, contratos, riesgos, información y conservación. |

## 14.3 Criterio de paso al piloto
- Todos los requisitos críticos y altos están aceptados.
- La revisión de permisos no detecta acceso cruzado.
- Los cálculos coinciden con el juego de resultados esperado.
- Las políticas e información de privacidad están aprobadas.
- Existe copia exportable del código y de los datos.
- El manual permite crear una campaña sin asistencia del constructor.
# 15 Riesgos y decisiones pendientes
## 15.1 Riesgos principales
| Riesgo | Efecto | Respuesta |
| --- | --- | --- |
| Alcance excesivo | Retraso y funciones incompletas. | Mantener el alcance del MVP y aplazar extras. |
| Modelo cambiante | Resultados no comparables. | Versionar el modelo y bloquear versiones publicadas. |
| Permisos mal configurados | Exposición de información. | Pruebas por rol y revisión técnica externa. |
| Fórmulas no documentadas | Resultados difíciles de auditar. | Registrar pesos, redondeo y versión de cálculo. |
| Dependencia de una persona | Dificultad de continuidad. | Trabajo compartido, manuales y repositorio propiedad de Agile Institute. |
| Datos insuficientes | Interpretaciones poco sólidas. | Mostrar tamaño de muestra y limitar conclusiones. |
| Confundir diagnóstico y validación | Uso excesivo de los resultados. | Incluir alcance y limitaciones en informes. |

## 15.2 Decisiones que deben cerrarse antes de programar el cálculo
| ID | Decisión | Responsable | Fecha límite |
| --- | --- | --- | --- |
| D 01 | Número definitivo de ítems por comportamiento o competencia. | Antonio Cano | Antes de semana 4 |
| D 02 | Pesos de comportamientos, competencias y dimensiones. | Antonio Cano | Antes de semana 6 |
| D 03 | Pesos de fuentes en resultados combinados. | Antonio Cano | Antes de semana 6 |
| D 04 | Umbral de anonimato definitivo. | Producto y privacidad | Antes del piloto |
| D 05 | Reglas para compartir el informe individual con la organización. | Producto y privacidad | Antes del piloto |
| D 06 | Plazos de conservación y eliminación. | Privacidad | Antes del piloto |
| D 07 | Textos interpretativos y recomendaciones. | Antonio Cano | Antes de semana 8 |
| D 08 | Condiciones de comparabilidad entre versiones. | Producto y validación | Antes de medición 2 |


# Anexo A Plantilla de importación de usuarios
| Campo | Obligatorio | Ejemplo | Regla |
| --- | --- | --- | --- |
| email | Sí | persona@empresa.com | Formato válido y sin espacios. |
| nombre | Sí | Ana Pérez | Texto entre 2 y 120 caracteres. |
| organization_code | Sí | ORG001 | Debe existir y estar activa. |
| area_code | No | VENTAS | Debe pertenecer a la organización. |
| team_code | Sí | VENTAS_NORTE | Debe existir o crearse previamente. |
| app_role | Sí | participant | Valor permitido por catálogo. |
| leader_email | No | lider@empresa.com | Debe identificar una cuenta válida. |
| language | No | es | Por defecto es. |

# Anexo B Plantilla de importación del modelo
| Campo | Uso |
| --- | --- |
| model_version | Identifica la versión, por ejemplo 3.0. |
| dimension_code y dimension_name | Identifican la dimensión. |
| meta_code y meta_name | Identifican la MetaCompetencia. |
| is_transversal | Marca la MetaCompetencia 13 como transversal. |
| competency_code y competency_name | Identifican la competencia asociada. |
| behavior_code y behavior_text | Identifican el comportamiento observable. |
| item_code y item_text | Identifican la pregunta. |
| source_type | Indica en qué fuente o cuestionario se utiliza. |
| weight | Peso configurable dentro de su nivel. |
| active y order | Controlan publicación y presentación. |

# Anexo C Lista de verificación antes del piloto
☐  El propietario de todas las cuentas es Agile Institute.
☐  El modelo cargado coincide con la versión 3.0 aprobada.
☐  Las fórmulas están documentadas y verificadas.
☐  Las campañas de prueba se han realizado con todos los roles.
☐  La separación entre organizaciones está comprobada.
☐  El umbral de anonimato funciona también al aplicar filtros.
☐  Los informes muestran fuente, muestra, versión y fecha.
☐  La información de privacidad está publicada.
☐  El procedimiento de incidencias está disponible.
☐  El código y los datos tienen una copia exportable.
☐  Los accesos de las personas en prácticas están identificados y limitados.
☐  Antonio Cano ha aprobado por escrito el inicio del piloto.
# Anexo D Glosario
| Término | Definición |
| --- | --- |
| MVP | Versión mínima que permite probar el valor y funcionamiento esenciales del producto. |
| Campaña | Conjunto de evaluaciones con un alcance, periodo, modelo y participantes definidos. |
| Asignación | Relación que indica quién evalúa, a quién, con qué fuente y en qué campaña. |
| Fuente | Perspectiva desde la que se responde, como autoevaluación, líder o equipo. |
| Umbral de anonimato | Número mínimo de respuestas necesario para mostrar un resultado agregado. |
| Modelo versionable | Estructura que conserva cada edición del modelo sin alterar resultados históricos. |
| Agile Flow Maturity | Sistema de lectura de madurez A1 a A5 aplicado al desarrollo y al flujo. |
| IA transversal | MetaCompetencia 13 aplicada a las cuatro dimensiones y presentada sin duplicar su peso. |

# Aprobación
La aprobación de este documento autoriza la construcción del MVP conforme al alcance y las reglas descritas. Cualquier cambio que afecte a permisos, datos, cálculos, informes o alcance deberá registrarse como una nueva decisión de producto.
| Rol | Nombre | Fecha | Aprobación |
| --- | --- | --- | --- |
| Product Owner | Antonio Cano García |  |  |
| Responsable técnico |  |  |  |
| Responsable de privacidad |  |  |  |

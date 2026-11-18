<!-- converted from Documento_Funcional_MVP_Centro_de_Test_v1_0 23092026 (1).docx -->



Documento Funcional del MVP
Centro de Test
MVP escalable hacia la plataforma de MetaCompetencias Agile®
| Campo | Información |
| --- | --- |
| Propietario | Agile Institute |
| Product Owner | Antonio Cano García |
| Equipo de construcción | Paula y Roberto |
| Versión | 1.0 |
| Fecha | 23 de septiembre de 2026 |
| Estado | Base de construcción y piloto |

Uso interno y para colaboradores autorizados

# Resumen ejecutivo
La primera versión no intentará construir todavía toda la plataforma de MetaCompetencias. Creará un Centro de Test sencillo que permita registrar personas, enviar enlaces individuales por correo, recoger respuestas, calcular resultados, generar informes estandarizados y consultar el estado y los indicadores. Esta decisión reduce el riesgo, acelera el aprendizaje y deja preparada la arquitectura para evolucionar posteriormente hacia la plataforma completa.
| Decisión recomendada Construir el MVP con Base44 Builder, correo transaccional mediante Resend y un repositorio GitHub propiedad de Agile Institute. La puntuación será determinista; la IA solo redactará una síntesis controlada a partir de puntuaciones e interpretaciones previamente aprobadas. |
| --- |

# Visión de producto
Para profesionales, consultores y organizaciones que necesitan administrar evaluaciones de forma rápida y ordenada, el Centro de Test de Agile Institute será una aplicación privada que automatiza el envío, seguimiento, corrección e informe de distintos test. A diferencia de una colección de formularios y hojas sueltas, conservará la ficha técnica, versión, reglas de puntuación y trazabilidad de cada resultado en un único entorno preparado para escalar.
## Propuesta de valor
- Enviar un test en menos de dos minutos.
- Evitar cálculos manuales y errores de copia.
- Entregar el informe automáticamente después de completar el test.
- Conocer en todo momento qué test está pendiente, realizado o caducado.
- Descargar un Excel visual con los indicadores medidos.
- Incorporar nuevos test sin rehacer la aplicación.
- Preparar la base para el futuro assessment de MetaCompetencias Agile.
## Criterios de éxito del piloto
| Indicador | Objetivo |
| --- | --- |
| Finalización | Al menos el 80 % completa el test sin ayuda. |
| Exactitud | El 100 % de una muestra de cálculos coincide con la comprobación manual. |
| Entrega | El informe o su enlace seguro llega automáticamente después de finalizar. |
| Seguimiento | Todos los envíos muestran correctamente pendiente, realizado o caducado. |
| Autonomía | Paula puede cargar usuarios y enviar un test sin ayuda técnica. |
| Escalabilidad | Roberto puede incorporar un segundo test sin modificar el código del primero. |
| Privacidad | Ningún enlace permite consultar datos de otra persona. |

# 1 Alcance del MVP
## 1.1 Incluido
- Administración de empresas y usuarios.
- Catálogo versionable de test y fichas técnicas.
- Carga de indicadores, ítems, opciones y reglas de puntuación.
- Envío individual de un enlace seguro por correo electrónico.
- Enlace personal, no predecible, de un solo uso y con 30 días de validez.
- Recordatorio automático al tercer día si el test sigue pendiente.
- Estados pendiente, realizado y caducado.
- Cálculo automático, informe individual y envío automático.
- Repositorio de informes individuales.
- Cuadro de mando agregado y descarga Excel.
- Síntesis asistida por IA, configurable por test y con alternativa sin IA.
- Registro básico de auditoría y exportación de datos.
## 1.2 Fuera del MVP
- Evaluaciones 180º, 270º o 360º.
- Comparaciones entre equipos o áreas de varias organizaciones.
- Benchmarks sectoriales y baremos propios.
- Venta y pago online de test.
- Aplicación móvil nativa.
- SSO corporativo, SAP, Workday u otras integraciones de RR. HH.
- Motor psicométrico avanzado o validación científica de instrumentos.
- Decisiones automatizadas de selección, promoción o despido.
# 2 Menú del producto
| N.º | Módulo | Función principal |
| --- | --- | --- |
| 1 | Usuarios | Crear, importar, buscar, editar y desactivar personas y empresas. |
| 2 | Enviar test | Elegir test y destinatario; crear el usuario si no existe; definir si puede ver su informe; enviar el enlace por correo. |
| 3 | Informes | Consultar informes individuales generados y enviados, por persona, empresa, test y fecha. |
| 4 | Estado de los test | Controlar pendiente, realizado o caducado; reenviar y lanzar recordatorio manual autorizado. |
| 5 | Informes y cuadros de mando | Analítica agregada, indicadores, filtros y descarga de un Excel visual. |
| 6 | Tests | Cargar, versionar y activar test, ficha técnica, indicadores, ítems, escalas, cálculo e informe. |

| Diferencia entre los menús 3 y 5 Informes es el archivo de documentos individuales. Informes y cuadros de mando es la analítica agregada y la exportación a Excel. Esta separación evita que dos pantallas hagan lo mismo. |
| --- |

# 3 Roles y permisos
| Rol | Acceso |
| --- | --- |
| Administrador Agile Institute | Usuarios, envíos, informes, estados, cuadros de mando, test, configuración y auditoría. |
| Gestor de test | Usuarios, envíos, informes y estados; no puede alterar reglas publicadas. |
| Consultor | Acceso solo a empresas o envíos asignados. |
| Destinatario | Acceso únicamente al test mediante su enlace y, si está autorizado, a su informe mediante otro enlace seguro. |
| Visor | Solo cuadros de mando o informes expresamente compartidos. |

# 4 Recorridos funcionales
## 4.1 Alta de usuario
Todos los test deben vincularse a una persona registrada. Los campos mínimos son empresa, nombre, apellidos, posición y correo. El correo será único dentro del MVP para evitar duplicados. Si el usuario ya existe, el sistema reutilizará su ficha y conservará su historial.
| Campo | Regla |
| --- | --- |
| Empresa | Obligatoria; debe existir o crearse. |
| Nombre y apellidos | Obligatorios; visibles en informe. |
| Posición | Obligatoria; texto libre en el MVP. |
| Correo | Obligatorio, validado y sin duplicados. |
| Estado | Activo o inactivo. |
| Consentimiento / información | Estado registrado cuando sea aplicable. |

## 4.2 Enviar test
1.  Seleccionar el test activo.
2.  Elegir si el test es para la propia persona administradora o para otra persona.
3.  Elegir si el destinatario podrá consultar su informe.
4.  Seleccionar un usuario o crear uno nuevo.
5.  Confirmar empresa, nombre, apellidos, posición y correo.
6.  Crear una invitación con fecha de envío, fecha de caducidad, estado pendiente y token seguro.
7.  Enviar un correo con el enlace personal.
8.  Registrar el resultado del envío en el historial.
| Seguridad del enlace El correo no incluirá identificadores correlativos. El enlace contendrá un token aleatorio de alta entropía; en la base de datos se conservará su huella, no el token en texto plano. El enlace dejará de funcionar al completarse o caducar. |
| --- |

## 4.3 Realizar test
1.  El destinatario abre el enlace sin necesidad de crear contraseña.
2.  El sistema valida token, caducidad, estado y test asociado.
3.  Se muestran finalidad, privacidad, instrucciones y tiempo estimado.
4.  La persona confirma sus datos y acepta la información requerida.
5.  Responde por bloques con barra de progreso y guardado seguro.
6.  El envío final bloquea respuestas, calcula resultados y marca realizado.
7.  Se genera el informe y se envía un correo con enlace seguro al informe cuando esté permitido.
## 4.4 Estados y automatizaciones
| Estado | Regla | Acciones |
| --- | --- | --- |
| Pendiente | No hay completed_at y la fecha actual no supera expires_at. | Ver, reenviar invitación, recordar, cancelar. |
| Realizado | Existe completed_at. | Abrir informe, reenviar informe, descargar, exportar. |
| Caducado | No hay completed_at y la fecha actual supera expires_at. | Renovar mediante una nueva invitación; no reactivar el token anterior. |

Una automatización diaria actualizará las invitaciones vencidas. Otra enviará un único recordatorio cuando hayan transcurrido tres días desde sent_at, el estado siga pendiente y reminder_sent_at esté vacío. Todos los envíos se registrarán en EmailLog.
## 4.5 Informes
Al completar el test se ejecutará primero el cálculo determinista. Después se seleccionarán los textos aprobados según los rangos de resultado. Si el test permite IA, el sistema solicitará una síntesis breve y personalizada usando exclusivamente esos datos. La IA no podrá alterar puntuaciones, niveles ni propiedades psicométricas.
| Bloque | Contenido |
| --- | --- |
| Cabecera | Empresa, nombre y apellidos, posición, test, versión y fecha. |
| Resumen | Resultado global, nivel y explicación de alcance. |
| Indicadores | Puntuación, rango, gráfico y texto aprobado por indicador. |
| Fortalezas | Hasta tres indicadores superiores, si el test lo permite. |
| Prioridades | Hasta tres indicadores inferiores, formulados como desarrollo. |
| Síntesis IA | Texto controlado y marcado como síntesis asistida; opcional. |
| Limitaciones | Finalidad, carácter no diagnóstico y condiciones de interpretación. |
| Trazabilidad | Versión del test, reglas y fecha de generación. |

Para el MVP, el envío automático será un correo con un enlace seguro al informe y un botón Descargar PDF. El PDF se obtiene desde una vista imprimible. Adjuntarlo físicamente al correo se deja como mejora posterior si la generación y entrega de adjuntos resulta estable.
# 5 Modelo de datos
| Entidad | Contenido principal |
| --- | --- |
| Company | Nombre, identificador, estado y datos básicos. |
| Person | Empresa, nombre, apellidos, posición, correo y consentimiento. |
| TestDefinition | Código, nombre, versión, estado, finalidad, plazos y configuración IA. |
| TestTechnicalSheet | Autores, año, ítems, escalas, propiedades, interpretación, referencias y licencia. |
| TestIndicator | Indicadores, orden, peso y rango. |
| TestItem | Texto, indicador, escala, orden, obligatoriedad e inversión. |
| ResponseOption | Valor, etiqueta y descriptor. |
| ScoringRule | Fórmula, pesos, redondeo y versión. |
| InterpretationRule | Rangos, nivel, texto aprobado y acción. |
| Invitation | Persona, test, token hash, fechas, estado, recordatorio y permiso de informe. |
| Response | Invitación, ítem, valor y fecha. |
| Result | Puntuación por indicador y global, versión y cálculo. |
| Report | Contenido, estado, enlace, fecha de envío y versión. |
| EmailLog | Tipo, destinatario, resultado, proveedor y fecha. |
| AuditEvent | Actor, acción, entidad, fecha y detalle mínimo. |

# 6 Reglas de test y puntuación
- Cada test tiene un código y una versión inmutables una vez publicados.
- Los ítems pertenecen a un indicador y a una escala de respuesta.
- Los ítems invertidos se transforman antes de agregar.
- La puntuación por indicador se calcula según su regla aprobada.
- El resultado global solo se calcula si la ficha del test lo define.
- Los rangos de interpretación no pueden solaparse ni dejar huecos.
- El cálculo guarda test_version y scoring_version.
- Un cambio de ítem, peso o interpretación genera una nueva versión.
- El sistema no denominará “validado” a un instrumento que no lo esté.
# 7 Cuadros de mando y Excel
| Indicador | Filtro mínimo |
| --- | --- |
| Test enviados | Empresa, test y periodo. |
| Realizados, pendientes y caducados | Empresa, test y periodo. |
| Tasa de finalización | Realizados / enviados. |
| Tiempo medio de respuesta | Desde sent_at hasta completed_at. |
| Recordatorios enviados | Empresa, test y periodo. |
| Resultado medio por indicador | Solo test, empresa y muestra autorizados. |
| Distribución por niveles | Test e indicador. |
| Evolución temporal | Cuando exista más de una medición comparable. |

La descarga Excel contendrá un resumen visual, una tabla filtrable de resultados y los indicadores agregados autorizados. No incluirá respuestas ítem a ítem salvo exportación administrativa expresamente autorizada.
# 8 Inteligencia artificial
## 8.1 Uso incluido
- Redactar una síntesis clara a partir de puntuaciones y textos aprobados.
- Ordenar fortalezas y prioridades ya calculadas.
- Adaptar la redacción al tono profesional de Agile Institute.
- Proponer una o dos acciones de desarrollo vinculadas a recomendaciones aprobadas.
## 8.2 Límites obligatorios
- No calcular ni corregir el test.
- No inventar diagnósticos, rasgos, baremos, causas o predicciones.
- No usar datos no incluidos en el paquete autorizado.
- No tomar decisiones de empleo.
- Guardar versión de prompt, proveedor/modelo y fecha.
- Permitir desactivar IA por test.
- Generar un informe estándar si la IA falla o no está disponible.
| Regla de oro Primero se calcula; después se interpreta con reglas; al final la IA redacta. Nunca al revés. |
| --- |

# 9 Tecnología recomendada
| Componente | Recomendación | Motivo |
| --- | --- | --- |
| Aplicación | Base44 Builder | Base de datos, autenticación, interfaz, backend, automatizaciones y GitHub en un entorno accesible para perfiles no técnicos. |
| Correo | Resend | Envío a destinatarios externos desde dominio propio, trazabilidad y adjuntos futuros. |
| Repositorio | GitHub privado de Agile Institute | Copia del código y salida futura de la plataforma. |
| Dominio | tests.agileinstitute.es | Identidad y confianza para los enlaces. |
| Informes | Vista web imprimible + PDF | Reduce integraciones del MVP y permite automatizar el envío de un enlace. |
| IA | Integración IA de Base44 o API aprobada | Síntesis acotada con consumo controlado. |
| Excel | Exportación desde Base44 | Entrega el cuadro de mando y datos autorizados. |
| Analítica | Cuadro interno del MVP | Suficiente para el piloto; sin herramienta BI externa. |

Base44 permite construir la interfaz, el backend, la base de datos, la autenticación y las automatizaciones en una misma plataforma. El plan Builder incorpora dominio y sincronización con GitHub; sus automatizaciones programadas sirven para caducidad y recordatorios. La integración Resend permite utilizar un dominio propio para el correo.
# 10 Qué necesitamos contratar
| Necesidad | Opción MVP | Momento |
| --- | --- | --- |
| Base44 | Plan Builder anual; subir a Pro solo si faltan créditos o capacidad. | Semana 1 o al pasar de prototipo a construcción continuada. |
| Correo transaccional | Cuenta Resend; plan gratuito para piloto y Pro si aumenta el volumen. | Semana 3. |
| Dominio/subdominio | Configurar tests.agileinstitute.es y registros DNS. | Semana 3. |
| Repositorio | GitHub privado propiedad de Agile Institute. | Semana 1. |
| Revisión técnica | Especialista externo 8-12 horas para arquitectura, permisos y seguridad. | Semanas 2, 6 y 8. |
| Privacidad | Revisión RGPD, contratos, textos, conservación y análisis de riesgos. | Antes del piloto real. |
| Licencias de test | Autorización o compra cuando el instrumento no sea propio. | Antes de cargar ítems o utilizarlo. |

# 11 Presupuesto
| Concepto | Estimación |
| --- | --- |
| Base44 Builder | 480 USD/año con facturación anual; Pro: 960 USD/año si fuera necesario. |
| Resend | 0 € en piloto hasta el límite del plan gratuito; Pro: 240 USD/año. |
| Dominio y DNS | 0-30 €/año si se utiliza un subdominio existente. |
| Consumo de IA | 100-500 €/año, según volumen y longitud de informes. |
| Revisión técnica externa | 800-1.500 € una vez. |
| Revisión de privacidad y textos | 600-1.200 € una vez. |
| Pruebas, certificados o contingencia | 300-800 €. |
| Licencias de test de terceros | No incluida; depende de cada instrumento. |

| Previsión económica Primer año sin personal ni licencias de terceros: aproximadamente 2.300-4.800 €, más IVA en servicios profesionales. Operación posterior: aproximadamente 700-1.800 € al año, dependiendo del uso de IA, correo y plan de Base44. |
| --- |

# 12 Reparto entre Paula y Roberto
| Persona | Responsabilidad |
| --- | --- |
| Paula · funcional y calidad | Usuarios de prueba, catálogo y fichas, textos, emails, casos de prueba, comprobación manual, revisión de informes, manual de usuario e incidencias. |
| Roberto · construcción no-code | Entidades, pantallas, permisos, enlaces, correo, automatizaciones, cálculo, IA, informes, Excel, auditoría, GitHub y correcciones técnicas. |
| Antonio · Product Owner | Aprueba alcance, test, licencias, fórmulas, textos, informe, privacidad y paso al piloto. |
| Apoyo externo | Revisa seguridad, arquitectura, rendimiento y RGPD sin asumir el desarrollo diario. |

# 13 Plan y entregables semanales
| Semana | Bloque | Trabajo | Entregable |
| --- | --- | --- | --- |
| 1 | Base y prototipo | Paula: valida campos, menú y casos. Roberto: crea app, entidades, roles y GitHub. | Navegación aprobada y datos ficticios. |
| 2 | Usuarios y test | Paula: carga Excel maestro y revisa fichas. Roberto: CRUD, importación y versión de test. | Usuarios y un test demo cargados. |
| 3 | Enviar test | Paula: aprueba correos. Roberto: token, invitación, Resend y registro. | Correo real de prueba con enlace seguro. |
| 4 | Cuestionario y cálculo | Paula: valida recorrido y cálculo manual. Roberto: formulario, guardado, envío y motor. | Test completo con resultado correcto. |
| 5 | Estados y recordatorios | Paula: casos de pendiente/caducado. Roberto: automatizaciones y acciones. | Estados y recordatorio de tres días operativos. |
| 6 | Informes e IA | Paula: aprueba textos. Roberto: informe, PDF, IA controlada y alternativa estándar. | Informe automático enviado. |
| 7 | Cuadro de mando y Excel | Paula: valida lectura. Roberto: filtros, gráficos y exportación. | Dashboard y Excel visual descargable. |
| 8 | Seguridad y piloto | Paula: ejecuta pruebas. Roberto: corrige, documenta y publica. | Versión candidata y decisión de piloto. |

# 14 Pruebas de aceptación
| ID | Prueba | Resultado esperado |
| --- | --- | --- |
| PA-01 | Crear una persona con todos los campos. | Aparece una sola vez en Usuarios. |
| PA-02 | Enviar un test. | Llega un correo con enlace individual y estado pendiente. |
| PA-03 | Abrir token inexistente, completado o caducado. | Se bloquea sin mostrar datos personales. |
| PA-04 | Completar y enviar el test. | Se guardan respuestas, se calcula y cambia a realizado. |
| PA-05 | Comparar cálculo automático con Excel manual. | Coincidencia dentro del redondeo. |
| PA-06 | Esperar tres días con estado pendiente. | Se envía un único recordatorio y queda registrado. |
| PA-07 | Superar 30 días sin completar. | Estado caducado y enlace bloqueado. |
| PA-08 | Generar informe con IA desactivada o fallida. | Se entrega el informe estándar. |
| PA-09 | Descargar Excel. | Contiene filtros, datos autorizados y gráfico legible. |
| PA-10 | Intentar acceder a otra invitación cambiando URL. | Acceso denegado. |
| PA-11 | Modificar un test publicado. | El sistema obliga a crear nueva versión. |
| PA-12 | Eliminar o desactivar usuario. | Se conserva la trazabilidad histórica según política. |

# 15 Seguridad, privacidad y propiedad intelectual
- Usar solo datos ficticios durante la construcción.
- No guardar el token de acceso en texto plano.
- Aplicar permisos en backend, no solo ocultar botones.
- Evitar incluir resultados sensibles en el asunto o cuerpo visible del correo.
- Definir finalidad, base jurídica, información, conservación, acceso y eliminación antes del piloto.
- Firmar o revisar los contratos de encargado de tratamiento con proveedores.
- Registrar exportaciones, cambios de reglas y reenvíos de informe.
- Comprobar licencias y derechos antes de cargar preguntas de terceros.
- No presentar los resultados como diagnóstico clínico ni como instrumento validado si no lo es.
- Las cuentas, dominio, repositorio y claves pertenecerán a Agile Institute.
# 16 Evolución hacia MetaCompetencias Agile
| Incremento | Contenido | Condición de entrada |
| --- | --- | --- |
| Incremento 1 · Centro de Test ampliado | Varios test, informes comparables, campañas, empresas, equipos sencillos, medición antes/después, plantillas por cliente y planes de desarrollo. | MVP estable, al menos dos test operativos y uso repetido por clientes. |
| Incremento 2 · Plataforma MetaCompetencias | Modelo 13/59/177, dimensiones Persona-Equipo-Líder-Organización, IA transversal, 180º/270º/360º, equipos, agregación, anonimato, Agile Flow y dashboards organizativos. | Modelo e ítems aprobados, reglas cerradas, revisión psicométrica, privacidad y demanda comercial. |

La arquitectura del MVP ya incorpora empresa, test versionable, indicadores, reglas y resultados. Por eso los incrementos amplían entidades y recorridos sin sustituir el núcleo. La MetaCompetencia de IA seguirá siendo transversal y no una quinta dimensión.
# 17 Decisiones que Antonio debe aprobar
| ID | Decisión | Fecha límite |
| --- | --- | --- |
| D-01 | Qué test entran en el piloto y qué licencias requieren. | Semana 2 |
| D-02 | Fórmulas, pesos, rangos y textos de interpretación. | Semana 4 |
| D-03 | Si el informe automático se entrega por enlace, PDF o ambos. | Semana 5 |
| D-04 | Qué resultados puede ver la empresa además del usuario. | Semana 6 |
| D-05 | Uso de IA por test y prompt aprobado. | Semana 6 |
| D-06 | Plazo de conservación y procedimiento de eliminación. | Antes del piloto |
| D-07 | Dominio de envío y remitente. | Semana 3 |
| D-08 | Criterio de éxito y continuidad al Incremento 1. | Semana 8 |

# Fuentes técnicas consultadas
- Base44 Docs: https://docs.base44.com/
- Base44 Pricing: https://base44.com/pricing
- Base44 · Sending emails: https://docs.base44.com/documentation/building-your-app/sending-emails
- Base44 · Automations: https://docs.base44.com/developers/backend/resources/backend-functions/automations
- Base44 · Security overview: https://docs.base44.com/Setting-up-your-app/security-overview
- Resend Pricing: https://resend.com/pricing
Los precios y capacidades indicados corresponden a la consulta realizada el 23/09/2026 y deben confirmarse antes de contratar.
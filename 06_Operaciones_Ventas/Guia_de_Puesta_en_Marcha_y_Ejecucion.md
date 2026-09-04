# Guía paso a paso: puesta en marcha y ejecución de EIOS-Sales v3.0

## Qué puede ejecutarse hoy

Este repositorio contiene la especificación operativa, de gobernanza y los contratos técnicos de EIOS-Sales; todavía no incluye una aplicación, servidor, base de datos ni conector ERP instalable. Por ello no existe aún un comando de inicio. Esta guía explica cómo dejarlo listo para operar y qué debe estar implementado antes de abrirlo a comerciales.

## Fase 1 — Preparar la empresa

1. Cree una copia de [Plantilla_Perfil_Empresa.md](../09_Recursos_Ventas/Plantilla_Perfil_Empresa.md) fuera del núcleo para su empresa.
2. Complete y apruebe el margen mínimo, margen objetivo, límites de descuento, plazos de pago, prioridad, fórmulas y roles. No use aproximaciones.
3. Asigne un `parameter_set_id`, versión, vigencia y aprobador al perfil.
4. Guarde el perfil aprobado como la única configuración activa de esa empresa. Un cambio posterior crea una nueva versión; no se edita la vigente retrospectivamente.

## Fase 2 — Conectar los datos

1. Decida el modo inicial: `SNAPSHOT` para un extracto limpio CSV/Excel o `LIVE` para consulta directa al ERP/CRM.
2. Complete [Plantilla_Mapeo_de_Fuentes.md](../09_Recursos_Ventas/Plantilla_Mapeo_de_Fuentes.md) para clientes, productos, costes, condiciones, histórico y señales financieras.
3. Implemente o configure un adaptador que entregue los objetos definidos en [Contrato_Integracion_Datos_EIOS.md](../../Contrato_Integracion_Datos_EIOS.md).
4. Compruebe que cada dato utilizable contiene sistema de origen, identificador de registro, momento de obtención, vigencia y calidad. Si no puede aportarlos, ese dato no puede sostener una oferta verde o amarilla.
5. Conserve el identificador de carga (`data_snapshot_id`) o de consulta (`live_query_id`) en cada evaluación.

## Fase 3 — Implementar la aplicación

1. Construya la interfaz de captura contra [operation-input.schema.json](../../07_Desarrollo_Ventas/esquemas/operation-input.schema.json).
2. Implemente el orquestador con la secuencia definida en [Arquitectura_Referencia.md](../../03_Arquitectura_Ventas/Arquitectura_Referencia.md): entrada → evidencia → evaluación → decisión humana.
3. Implemente el motor conforme a [Especificacion_del_Motor_de_Evaluacion.md](../../04_Inteligencia_Ventas/Especificacion_del_Motor_de_Evaluacion.md). El motor no puede conectarse directamente al ERP/CRM.
4. Valide cada resultado contra [evaluation-result.schema.json](../../07_Desarrollo_Ventas/esquemas/evaluation-result.schema.json).
5. Almacene evaluaciones y decisiones en un registro append-only; genere un Trace ID en la primera evaluación y una nueva revisión ante cualquier cambio.
6. Restrinja permisos: administración de parámetros, consulta, decisión comercial y auditoría son roles distintos.

## Fase 4 — Validar antes de producción

1. Prepare un entorno de prueba con datos sintéticos etiquetados o datos autorizados.
2. Ejecute todos los casos de [Plan_de_Aceptacion.md](../../08_Pruebas_Ventas/Plan_de_Aceptacion.md).
3. Compruebe especialmente que una operación sin datos queda ⚪, que un margen bajo mínimo queda 🔴 y que ninguna concesión sin contrapartida se puede presentar.
4. Compruebe que una respuesta modificada del cliente conserva el Trace ID y genera una revisión nueva.
5. Obtenga aprobación formal del responsable de negocio y del responsable de datos antes de habilitar comerciales.

## Fase 5 — Ejecutar una operación cuando la aplicación esté desplegada

1. Inicie sesión con una identidad autorizada.
2. Seleccione el perfil de empresa vigente; verifique su versión y fecha de vigencia.
3. Introduzca literalmente producto o servicio, cantidad, cliente, precio o condiciones, suministro y condiciones de pago.
4. Solicite la evaluación. La interfaz debe mostrar un máximo de tres opciones, cada una con color, condiciones, margen disponible, riesgo, contrapartida y Trace ID.
5. Si el resultado es ⚪, aporte únicamente los datos solicitados y vuelva a evaluar.
6. Si es 🟡, negocie exactamente las condiciones o contrapartidas indicadas. Registre la respuesta del cliente de forma literal.
7. Solicite una reevaluación tras cualquier cambio. No modifique ni borre la evaluación anterior.
8. Si es 🟢, el comercial decide si presentar, aceptar o confirmar la oferta. Registre su decisión y motivo.
9. Si es 🔴, no venda bajo esas condiciones. Solo un cambio verificable de los hechos o condiciones puede crear una nueva evaluación.

## Lista rápida de salida a producción

- [ ] Perfil empresarial aprobado y vigente.
- [ ] Adaptador `SNAPSHOT` o `LIVE` validado contra el contrato común.
- [ ] Esquemas de entrada y salida validados.
- [ ] Auditoría append-only y revisiones por Trace ID comprobadas.
- [ ] Casos de aceptación críticos superados.
- [ ] Roles y conservación de datos configurados.
- [ ] Formación comercial completada.

Hasta completar las fases 1 a 4, EIOS-Sales es una especificación preparada para implementación, no una aplicación que pueda iniciarse desde la consola.

# Especificación del motor de evaluación

El motor recibe operación literal, evidencias canónicas, perfil vigente y versión de reglas. Devuelve hasta tres opciones separadas en `realidad_datos`, `escenarios` y `decision_acciones`.

## Algoritmo determinista

1. Asignar `trace_id`, revisión y versiones de reglas/parámetros.
2. Validar esquema, datos esenciales y vigencia de evidencia.
3. Clasificar carencias como ⚪ antes de calcular lo que dependa de ellas.
4. Calcular ingreso, coste, margen, condiciones y efecto financiero solo con datos trazables; guardar fórmula y unidades.
5. Evaluar bloqueos: margen mínimo, riesgo, tesorería y cumplimiento críticos.
6. Generar escenarios explícitos de precio, cantidad, pago, financiación o alcance cuando los datos lo permitan.
7. Validar concesión y contrapartida; comprobar de nuevo el margen mínimo.
8. Aplicar prioridad de empresa solo a opciones no bloqueadas.
9. Emitir color, taxonomía, límites, evidencias, limitaciones y acciones permitidas.

La fórmula de margen, base de coste, coste financiero, redondeo, impuestos y conversión de moneda son reglas versionadas por empresa. Un escenario declara cambio supuesto, resultado, evidencias reutilizadas, desconocidos y condición resultante; nunca modifica realidad u origen.

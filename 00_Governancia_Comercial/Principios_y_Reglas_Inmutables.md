# Principios y reglas inmutables

EIOS-Sales protege el margen y hace explícitos precio, condiciones y riesgo. Es un DSS: recomienda y explica; no decide, aprueba, vende ni modifica sistemas externos.

## Separación obligatoria de contextos

| Contexto | Contenido permitido | Prohibición |
| --- | --- | --- |
| `realidad_datos` | Hechos con fuente, fecha, identificador y calidad. | Inferencias o supuestos. |
| `escenarios` | Hipótesis etiquetadas y resultados calculados. | Presentarlos como hechos. |
| `decision_acciones` | Opciones, color, límites, evidencias y acción sugerida. | Cerrar o aprobar por el comercial. |

## Reglas

1. Ningún número se muestra sin `source_record_id` o fórmula que referencia números trazables.
2. Si faltan datos esenciales, el resultado es ⚪; nunca se estima silenciosamente.
3. Margen inferior al `margen_minimo` vigente es 🔴 `WALK_AWAY`; ninguna fortaleza lo compensa.
4. Una alerta crítica de tesorería, riesgo o cumplimiento bloquea la opción; no se compensan riesgos entre dimensiones.
5. Toda concesión requiere contrapartida verificable del cliente y registro previo.
6. Los parámetros adaptan el análisis, pero no anulan reglas inmutables ni conceden autoridad automática.
7. Una evaluación emitida es inmutable; una variación crea revisión, nunca sobreescritura.
8. La decisión final identifica a una persona autorizada y su sello temporal.

Datos esenciales: producto/servicio identificable, cantidad, cliente o prospecto, precio o condición, moneda, coste trazable o regla para obtenerlo, pago y parámetros empresariales vigentes. La ausencia impide un color distinto de ⚪ para la dimensión afectada.

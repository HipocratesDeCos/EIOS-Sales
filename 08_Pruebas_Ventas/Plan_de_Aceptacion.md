# Plan de aceptación

Las pruebas usan datos sintéticos etiquetados o un entorno autorizado. Nunca se reutilizan datos personales o financieros productivos sin autorización.

| ID | Caso | Resultado exigido |
| --- | --- | --- |
| AT-01 | Falta coste, pago o parámetro. | ⚪, lista exacta de ausencias y cero valores inventados. |
| AT-02 | Margen bajo mínimo. | 🔴 `WALK_AWAY`, aun con volumen/histórico favorables. |
| AT-03 | Concesión sin contrapartida. | 🔴 o ⚪ si no se puede evaluar; nunca ofertable. |
| AT-04 | Concesión con contrapartida y límites cumplidos. | `ACCEPTED_WITH_CONCESSION`, color basado en todas las dimensiones. |
| AT-05 | Riesgo crítico y margen favorable. | 🔴, sin compensación automática. |
| AT-06 | Respuesta de cliente modificada. | Mismo Trace ID, nueva revisión e historial conservado. |
| AT-07 | Misma operación en `SNAPSHOT` y `LIVE`. | Resultado equivalente y metadatos de origen distintos. |
| AT-08 | Intento de cierre por motor. | Rechazado; requiere acción humana autorizada. |

No hay salida a producción hasta aprobar casos críticos, validar esquemas, comprobar inmutabilidad y obtener revisión humana de negocio sobre claridad de explicaciones.

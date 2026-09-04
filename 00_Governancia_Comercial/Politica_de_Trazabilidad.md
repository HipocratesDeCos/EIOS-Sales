# Política de trazabilidad y conservación

- `trace_id`: identificador estable de una negociación; formato recomendado `EIOS-SALES-<fecha UTC>-<uuid>`.
- `revision`: entero desde `0`; una presentación puede usar `trace_id-R<revision>`.
- `evaluation_id`, `parameter_set_id`, `rule_set_version` y `data_snapshot_id` identifican exactamente el marco utilizado.

Cada evaluación conserva operación literal, normalización, referencias de fuentes, fecha de extracción/consulta, parámetros, reglas, escenarios, cálculos, resultado, usuario solicitante y decisión humana posterior. Una respuesta del cliente o cambio relevante crea una revisión con `parent_evaluation_id`. Los registros son append-only: una corrección de origen crea evento y reevaluación, no altera el informe histórico. Los datos personales y financieros se minimizan, se acceden por rol y se retienen según la política legal empresarial.

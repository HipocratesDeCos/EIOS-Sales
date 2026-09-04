# Contrato de integración de datos EIOS

Contrato canónico, neutro y compartible entre EIOS-Sales y futuros productos EIOS. Define datos y procedencia; no contiene reglas de decisión ni parámetros de empresa.

| Modo | Uso | Requisito |
| --- | --- | --- |
| `SNAPSHOT` | CSV, Excel, exportación API o almacén. | `data_snapshot_id`, momento de corte, origen y validación. |
| `LIVE` | Consulta directa a ERP/CRM. | Identificador de consulta, momento, versión/ETag si existe y campos devueltos. |

El motor recibe los mismos objetos canónicos en ambos modos y nunca consulta tablas o APIs de proveedor directamente.

| Objeto | Clave | Campos funcionales mínimos |
| --- | --- | --- |
| Cliente | `customer_id` | nombre mostrado, estado, pago, señales de riesgo y vigencia. |
| Producto/servicio | `product_id` | descripción, unidad, disponibilidad, coste trazable y vigencia. |
| Condición comercial | `commercial_term_id` | precio, moneda, descuento, pago, suministro y validez. |
| Venta/histórico | `sales_record_id` | cliente, producto, cantidad, precio, fecha y condición. |
| Coste | `cost_record_id` | producto, importe, moneda, unidad, método y vigencia. |
| Tesorería/riesgo | `financial_signal_id` | tipo, valor/estado, periodo, fuente, calidad y vigencia. |
| Parámetros | `parameter_set_id` | empresa, versión, vigencia, aprobador y valores. |

Todo campo empleado aporta `source_system`, `source_record_id`, `retrieved_at`, `effective_at` si aplica, `data_quality` y `data_snapshot_id` o `live_query_id`. El adaptador traduce y valida; no calcula margen ni toma decisiones. Cambios incompatibles exigen nueva versión mayor y coexistencia durante migración.

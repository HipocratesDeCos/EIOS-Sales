# Modelo de dominio comercial

| Entidad | Responsabilidad | Fuente de verdad |
| --- | --- | --- |
| Operación | Solicitud literal y condiciones solicitadas. | Comercial/interfaz. |
| Oferta | Propuesta evaluada por líneas y condiciones. | EIOS, derivada. |
| Cliente | Identidad, histórico, límites y señales. | CRM/ERP o extracto validado. |
| Producto/servicio | Identidad, disponibilidad, coste y reglas. | Maestro/ERP o extracto validado. |
| Parámetros empresariales | Límites y prioridad temporal. | Administrador autorizado. |
| Regla | Política versionada. | Gobernanza EIOS. |
| Escenario | Cambio hipotético frente a realidad. | Motor EIOS. |
| Evaluación | Resultado reproducible. | Motor EIOS. |
| Decisión humana | Acción final y motivo. | Comercial autorizado. |

`BORRADOR → DATOS_PENDIENTES/EN_EVALUACION → EVALUADA → EN_NEGOCIACION → REEVALUADA* → CERRADA`

Solo una persona puede cerrar mediante `ACEPTADA`, `RECHAZADA`, `WALK_AWAY` o `CANCELADA`. Una concesión registra tipo, impacto trazable, condición de activación y contrapartida; sin ambos elementos no es ofertable.

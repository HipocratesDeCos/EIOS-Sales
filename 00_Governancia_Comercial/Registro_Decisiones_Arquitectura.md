# Registro de decisiones de arquitectura y criterio de consolidación

| ID | Decisión | Criterio aplicado |
| --- | --- | --- |
| ADR-001 | La versión es **v3.0**. | El superprompt v3/v3.0 es la fuente de gobernanza más reciente. Las menciones v2.0 del brief son antecedentes históricos. |
| ADR-002 | Se mantiene la estructura acordada y se omite `02`. | Decisión previa explícita; preserva compatibilidad organizativa con EIOS Compras. |
| ADR-003 | Semáforo de cuatro colores y taxonomía de cinco salidas. | El color expresa viabilidad; la taxonomía, estado comercial. |
| ADR-004 | Toda concesión exige contrapartida. | La regla inmutable del superprompt prevalece sobre el proceso resumido. Crédito, portes, regalos, descuentos o servicios se registran con coste y contrapartida verificable. |
| ADR-005 | Núcleo separado de interfaces de datos. | Un extracto o ERP/CRM en vivo puede cambiar sin reescribir reglas ni motor. |
| ADR-006 | Sin dependencia de proveedor, LLM o base de datos. | El entorno sigue abierto y se requiere portabilidad. |
| ADR-007 | Sin datos empresariales ficticios. | El diseño no debe confundirse con realidad ni inducir fabricación de datos. |

## Correspondencia

| Resultado comercial | Color | Significado |
| --- | --- | --- |
| OFERTA ACEPTADA (TARGET) | 🟢 | Límites, objetivos y evidencia suficientes. |
| OFERTA ACEPTADA CON CONCESIÓN | 🟢 | Concesión y contrapartida verificadas. |
| OFERTA CONDICIONADA | 🟡 | Viable si se cumplen condiciones explícitas. |
| NO VENDER (WALK-AWAY) | 🔴 | Límite infranqueable o riesgo crítico. |
| INFORMACIÓN INSUFICIENTE | ⚪ | Falta evidencia. |

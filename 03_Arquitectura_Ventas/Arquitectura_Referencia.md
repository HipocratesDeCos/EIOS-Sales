# Arquitectura de referencia

```text
Interfaz comercial ─┐
                    ├─ Aplicación/orquestación ─ Motor ─ Reglas y parámetros
Adaptadores de datos┘                             │
ERP/CRM, extractos y finanzas ─ Contrato canónico ┘
                                                   │
                                      Auditoría append-only
```

| Componente | Hace | No hace |
| --- | --- | --- |
| Interfaz | Captura literal, muestra capas y registra decisión. | Inventar datos o cerrar ventas. |
| Orquestador | Crea revisión, solicita datos y persiste evidencia. | Reglas de margen o lógica de proveedor. |
| Motor | Calcula, crea escenarios y clasifica. | Consultar ERP/CRM. |
| Reglas/perfil | Versiona políticas y parámetros vigentes. | Guardar datos operativos. |
| Adaptador | Traduce `SNAPSHOT`/`LIVE` al contrato. | Decidir comercialmente. |
| Auditoría | Conserva eventos/artefactos inmutables. | Alterar resultados. |

`OperationInput → EvidenceBundle → EvaluationRequest → EvaluationResult → HumanDecision`. Cada frontera valida esquema y conserva evidencia. El motor depende solo de dominio, reglas y perfiles; los adaptadores dependen del contrato raíz.

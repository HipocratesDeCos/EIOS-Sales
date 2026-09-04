# Guía de implementación

Los esquemas son contratos, no una elección de lenguaje o proveedor. Todo servicio valida entrada y salida, conserva evidencia y rechaza valores no soportados. Los adaptadores ERP/CRM entregan `EvidenceBundle`; el motor solo consume ese bundle. Los eventos se publican append-only y no sustituyen revisiones previas.

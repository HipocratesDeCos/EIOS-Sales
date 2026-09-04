# Ejecutar el prototipo EIOS-Sales

## Requisitos ya instalados

El proyecto usa un entorno aislado `.venv` con Streamlit. El prototipo no requiere ERP, CRM ni acceso a internet durante su uso.

## Inicio local

Desde la carpeta `EIOS-Sales v3.0`, ejecutar:

```powershell
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

El navegador abrirá la dirección local que muestre Streamlit. Para detenerlo, usar `Ctrl+C` en la consola.

## Uso inicial

1. Cargar el perfil de empresa aprobado `perfil_empresa_v1.0.json`.
2. Introducir solo información conocida de la operación.
3. Declarar el estado del cliente y el riesgo; si no se han verificado, dejar ambos como pendientes.
4. Evaluar. Cada nueva evaluación de la misma negociación crea una revisión del Trace ID.
5. Registrar la decisión humana y descargar el registro de auditoría.

## Límites del prototipo

Actualmente la información de una operación se introduce manualmente y el registro se descarga como JSON. La conexión con `clientes.xlsx`, `artículos.xlsx` y futuros ERP/CRM se implementará después de cerrar y normalizar el mapeo de la Fase 2.

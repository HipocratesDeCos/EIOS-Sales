# Cómo completar `perfil_empresa_v1.0.json`

1. Descarga o copia `perfil_empresa_v1.0.json` a la carpeta externa del perfil de tu empresa, dentro de `01_Configuracion`.
2. Sustituye todos los textos que comienzan por `PENDIENTE_`; no dejes ninguno.
3. Introduce los tres porcentajes como números, sin símbolo `%`. Introduce los plazos como números enteros de días.
4. Usa para `current_priority` exactamente uno de estos valores: `MARGIN`, `SALES`, `STOCK`, `LIQUIDITY`, `RISK` o `GROWTH`.
5. Guarda el archivo con el mismo nombre para la primera versión. Cuando cambien parámetros, copia el archivo, cambia `version`, `parameter_set_id`, `effective_from` y `approved_by`, y guárdalo como `perfil_empresa_v1.1.json`, `perfil_empresa_v1.2.json` y así sucesivamente.
6. Tras completarlo, valida el archivo contra `company-profile.schema.json`; antes de completar los campos es una plantilla, no un perfil activo.

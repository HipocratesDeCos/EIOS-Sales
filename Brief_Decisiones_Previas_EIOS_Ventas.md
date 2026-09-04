# Brief de Decisiones Previas — EIOS Ventas / EIOS-Sales

Este documento recoge las decisiones de arquitectura y gobernanza ya acordadas en fases anteriores del proyecto EIOS Ventas, antes de la construcción de EIOS-Sales v2.0. No sustituye a `SUPERPROMPT EIOS-SALES v3.md` ni a `EIOS-Sales-Flujo_Comercial.md` (que definen la lógica de negocio del DSS): los complementa fijando el marco de proyecto en el que esa lógica debe encajar. Ante cualquier conflicto de detalle entre este brief y los dos archivos de negocio, prevalece el criterio que tú mismo apliques y documentes, pero respetando los principios de fondo aquí descritos.

## 1. Relación con EIOS Compras

- EIOS Ventas es una iniciativa hermana de EIOS Vertical MVP (EIOS Compras), pero con foco distinto: Compras está orientado a la negociación de compras; Ventas está orientado al comercial que vende, con foco en salvaguardar el margen de la empresa.
- Ambos proyectos se mantienen **separados** (repos/carpetas independientes) por ahora, pero deben diseñarse **pensando en una posible fusión futura**: el motivo es que, cuando se conecte un ERP/CRM, ese ERP/CRM servirá datos a los dos proyectos, y no tiene sentido duplicar la integración.
- Consecuencia de diseño: aísla el acoplamiento entre ambos proyectos en un único archivo neutro y compartido — `Contrato_Integracion_Datos_EIOS.md` — que define nombres de campo canónicos, fuente de verdad, cadencia de refresco y modo de conexión (extracto estructurado limpio o consulta directa en vivo al ERP/CRM; ambos modos deben soportarse). Todo lo demás (motor de decisión, escalera de negociación, parámetros, taxonomía de decisión) permanece independiente entre los dos proyectos.
- Objetivo explícito: evitar en Ventas los errores de estructuración/organización que se dieron en el proyecto EIOS Compras, siendo más eficiente y ordenado desde el inicio.

## 2. Estructura de carpetas acordada

Mirror de la estructura real del repo de EIOS Compras, renombrada con sufijos `_Ventas`/`_Comercial`, saltando el número 02 (reservado):

- `00_Governancia_Comercial`
- `01_Negocio_Ventas`
- `03_Arquitectura_Ventas`
- `04_Inteligencia_Ventas`
- `05_Aplicacion_Ventas`
- `06_Operaciones_Ventas`
- `07_Desarrollo_Ventas`
- `08_Pruebas_Ventas`
- `09_Recursos_Ventas`

Esta numeración y nomenclatura ya están decididas; no es necesario reabrir esta decisión, solo respetarla al ubicar los documentos que se generen.

## 3. Taxonomía de decisión adoptada

Se adoptó una taxonomía de 5 salidas posibles (en vez de solo el semáforo de 4 colores del superprompt), que debe conciliarse con el semáforo 🟢🟡🔴⚪ definido en `SUPERPROMPT EIOS-SALES v3.md`:

1. OFERTA ACEPTADA (TARGET)
2. OFERTA ACEPTADA CON CONCESIÓN
3. OFERTA CONDICIONADA
4. NO VENDER (WALK-AWAY)
5. INFORMACIÓN INSUFICIENTE

## 4. Decisión abierta, no resuelta — resolver de forma autónoma

No se resolvió si las concesiones (crédito, regalos, portes) que el comercial puede ofrecer al cliente **requieren siempre una contrapartida del cliente** (como exige la regla "NO CONCEDER NADA SIN CONTRAPARTIDA" en el superprompt de Ventas, calcada de la escalera de negociación de Compras), o si en Ventas pueden ofrecerse de forma unilateral, tal como sugiere la descripción del proceso real (ver punto 5). Al construir EIOS-Sales v2.0, debe tomarse esta decisión de forma autónoma y quedar documentada explícitamente, ya que afecta directamente a la regla inmutable de gobernanza del sistema.

## 5. Proceso comercial real descrito

Cliente pide un producto → el comercial consulta precio en EIOS → el cliente acepta, o el comercial renegocia ofreciendo crédito, regalos o portes (todo ello calculado por EIOS) → siempre bajo la premisa de salvaguardar los intereses económicos, financieros y legales de la empresa.

## 6. Naturaleza de los datos y su origen

- No hay un ERP o CRM concreto definido todavía para este proyecto.
- El sistema debe soportar **dos modos de origen de datos** de forma indistinta: (a) un extracto estructurado limpio (p. ej. Excel/CSV), o (b) una consulta directa en vivo contra un CRM/ERP. Esta dualidad debe quedar reflejada en el `Contrato_Integracion_Datos_EIOS.md` mencionado en el punto 1, no resuelta de forma distinta en cada proyecto.

## 7. Diseño company-agnostic

El proyecto no está atado a ninguna empresa concreta actualmente y debe diseñarse de forma **generalista**, para poder trasladarse a otra empresa en el futuro sin rehacer el núcleo. Esto implica: la lógica central (reglas, motor de decisión, escalera de negociación, taxonomía) debe mantenerse genérica; los datos y parámetros específicos de una empresa concreta (márgenes mínimos, prioridades, catálogo, clientes) deben aislarse en un **perfil instanciable** separado del núcleo.

## 8. Entorno de trabajo (sin decidir todavía)

Existe interés en trabajar localmente con Claude Cowork (por protección de datos) y también en un modo "SDK" (proyecto de Claude alimentado directamente con datos de Excel). Esta decisión de entorno sigue abierta y no condiciona el diseño del sistema en sí; no es necesario resolverla para construir EIOS-Sales v2.0, pero conviene no diseñar nada que dependa en exclusiva de una de las dos opciones.

# 📓 Data Journal - Pipeline Retail Automation (CSV to Google Sheets)

---

## [Fase 1: Ingesta, Diagnóstico y Gobernanza de Datos]

### 1. Auditoría de Estructura y Estandarización de Encabezados (Pandas)

* **[P] Problema:** El dataset original trae encabezados en inglés, nombres con espacios invisibles (*Non-Breaking Spaces* / caracteres ocultos), capitalización inconsistente (ej. `cogs` vs `Gross margin percentage`) y símbolos especiales como `%` (`Tax 5%`). Esto bloquea la automatización con APIs de Google Sheets y rompe las consultas de agregación en Python.
* **[D] Decisión:** Aplicar una política estricta de gobernanza de datos: limpiar caracteres invisibles mediante `.str.strip()`, mapear todas las columnas al español en formato `snake_case` y sustituir el símbolo `%` por `pct` para garantizar compatibilidad con sintaxis de código y la API de carga.
* **[A] Acción:** Ejecución del diccionario de renombrado explícito y limpieza de strings en el DataFrame inicial:
  ```python
  # Limpieza de espacios invisibles en nombres de columnas
  df.columns = df.columns.str.strip()

  # Estandarización a Español (Snake Case)
  columnas_espanol = {
      'Invoice ID': 'ID_Factura',
      'Branch': 'Sucursal',
      'City': 'Ciudad',
      'Customer type': 'Tipo_Cliente',
      'Gender': 'Genero',
      'Product line': 'Linea_Producto',
      'Unit price': 'Precio_Unitario',
      'Quantity': 'Cantidad',
      'Tax 5%': 'Impuesto_5pct',  # Evita errores con el símbolo % en API
      'Total': 'Ventas_Totales',
      'Date': 'Fecha',
      'Time': 'Hora',
      'Payment': 'Metodo_Pago',
      'cogs': 'Costo_Bienes_Vendidos',
      'gross margin percentage': 'Porcentaje_Margen_Bruto',
      'gross income': 'Ganancia_Bruta',
      'Rating': 'Evaluacion',
  }
  df = df.rename(columns=columnas_espanol)

[R] Resultado: Un DataFrame estandarizado con 17 columnas traducidas, libres de caracteres invisibles y listas para ser procesadas sin errores sintácticos.

[Fase 2: Transformación y Modelado de Data Marts]
1. Generación de Resúmenes Estratégicos vía Agregación Nombrada (Named Aggregation)
[P] Problema: El dataset crudo consta de 1,000 transacciones individuales. Analizar datos a nivel de fila dificulta la toma de decisiones gerenciales sobre el rendimiento financiero de tiendas, la rotación de inventarios y los hábitos de pago.

[D] Decisión: Diseñar 3 Data Marts (tablas resumidas) agregando métricas clave (sum, mean) mediante la técnica moderna de Named Aggregation de Pandas para renombrar y consolidar campos en un solo paso, incluyendo el cálculo derivado del porcentaje de margen bruto.

[A] Acción: Construcción de las 3 consultas analíticas en Python:
  
  ```python
# 1. Rendimiento y Margen por Sucursal
resumen_sucursal = (
    df.groupby('Sucursal')
    .agg(
        Ventas_Totales=('Ventas_Totales', 'sum'),
        Costo_Total=('Costo_Bienes_Vendidos', 'sum'),
        Ganancia_Bruta=('Ganancia_Bruta', 'sum'),
        Ticket_Promedio=('Ventas_Totales', 'mean'),
        Rating_Promedio=('Evaluacion', 'mean'),
    )
    .reset_index()
)

# Cálculo de variable derivada de Margen Bruto %
resumen_sucursal['Pct_Margen_Bruto'] = (
    resumen_sucursal['Ganancia_Bruta'] / resumen_sucursal['Ventas_Totales']
) * 100
resumen_sucursal = resumen_sucursal.round(2)

# 2. Rotación por Línea de Producto
resumen_productos = (
    df.groupby('Linea_Producto')
    .agg(
        Ventas_Totales=('Ventas_Totales', 'sum'),
        Cantidad_Vendida=('Cantidad', 'sum'),
        Ganancia_Bruta=('Ganancia_Bruta', 'sum'),
    )
    .reset_index()
    .sort_values(by='Ventas_Totales', ascending=False)
    .round(2)
)

# 3. Preferencias de Pago por Sucursal
resumen_pagos = (
    df.groupby(['Sucursal', 'Metodo_Pago'])
    .agg(
        Transacciones=('ID_Factura', 'count'),
        Ventas_Totales=('Ventas_Totales', 'sum'),
    )
    .reset_index()
    .sort_values(
        by=['Sucursal', 'Ventas_Totales'], ascending=[True, False]
    )
    .round(2)
) 
  ```

[R] Resultado: Tres DataFrames independientes, limpios y redondeados a 2 decimales, optimizados estructuralmente para ser inyectados
directamente vía API a la capa de visualización en Google Sheets.

---
### [Fase 3: Carga Cloud e Integración API]

* **[P] Problema:** 
  Necesidad de automatizar la actualización periódica de datos en la nube sin intervención manual, garantizando que el Dashboard consuma siempre la versión procesada y limpia de los DataFrames de Python.

* **[D] Decisión:** 
  Implementar una arquitectura de integración continua utilizando la API de Google Sheets (`gspread`) con credenciales de cuenta de servicio (`Service Account`), aplicando un método de reemplazo atómico por pestaña para mantener la integridad referencial de los gráficos.

* **[A] Acción:** 
  1. Configuración de cliente `gspread` autenticado mediante OAuth2 / Service Account.
  2. Implementación de la función `update_sheet_tab()` para ejecutar una limpieza (`clear()`) e inyección de datos (`update()`) automatizada sobre las 4 pestañas de datos (`datos_ventas`, `ventas_sucursal`, `ventas_producto`, `ventas_clientes`).
  3. Aislamiento de la capa de datos mediante la ocultación de pestañas internas en la hoja de cálculo.

* **[R] Resultado:** 
  Pipeline de datos 100% automatizado en la nube con tiempo de sincronización menor a 5 segundos, permitiendo que el Frontend en Google Sheets refleje cambios inmediatamente al ejecutar el script en Python.

---

### [Fase 4: Visualización, Maquetación y Reporte Ejecutivo]

* **[P] Problema:** 
  Presentar métricas complejas de ventas y comportamiento operativo a nivel ejecutivo sin saturar al usuario con tablas masivas de datos.

* **[D] Decisión:** 
  Diseñar un Dashboard interactivo centralizado bajo la regla de jerarquía visual (KPIs principales en la parte superior, comparativas por sucursal/producto al centro y comportamiento operativo al pie) acompañado de un Resumen Ejecutivo de negocio.

* **[A] Acción:** 
  1. Ocultación de cuadrículas en Google Sheets y creación de tarjetas de puntuación (*Scorecards*) para KPIs clave: Ventas Totales ($322.9K), Ganancia Bruta y Ticket Promedio ($322.96).
  2. Construcción de gráficos de barras ordenados descendentemente por volumen monetario.
  3. Incorporación de minigráficos comparativos de Métodos de Pago (Ventas vs. Frecuencia de Transacciones).
  4. Publicación Web configurada con rango delimitado para eliminar scroll infinito y proteger celdas.

* **[R] Resultado:** 
  Panel de control ejecutivo de interfaz limpia, seguro y publicado en la web, que permite a la gerencia responder preguntas estratégicas en menos de 10 segundos.

---

### [Resumen del Informe Ejecutivo / Insights de Negocio]

1. **Rendimiento por Sucursal: La Sucursal C lidera el volumen de ventas con $110.5K, seguida muy de cerca por la Sucursal A ($106.2K) y la Sucursal B ($106.1K), mostrando un desempeño comercial sumamente equilibrado entre las tres filiales.
2. **Líneas de Producto:** Alimentos/Bebidas y Deportes/Viajes son los principales motores de volumen de venta.
3. **Comportamiento del Canal de Pago:** Divergencia clave entre monto monetario y frecuencia: *Cash* genera mayor ingreso financiero ($112K), pero *E-wallet* domina en volumen de transacciones (345 operaciones).

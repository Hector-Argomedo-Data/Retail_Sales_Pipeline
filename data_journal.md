📓 Data Journal - Proyecto Retail Analytics & Pipeline Google Sheets

[Fase 1: Ingesta, Limpieza y Estandarización de Variables con Python]

1. Verificación de Integridad y Estructura del Dataset
[P] Problema: El archivo fuente de transacciones (supermarket_Sales.csv) contiene 1,000 registros con nombres de variables en inglés y valores flotantes de alta precisión decimal que dificultan la lectura en reportes.
[D] Decisión: Realizar un Análisis Exploratorio de Datos (EDA) inicial en Python/Pandas para validar que no existan valores nulos y estandarizar la precisión numérica a 2 decimales.
[A] Acción: Inspección estructural mediante df.shape, df.info() y aplicación de df.describe().round(2) para auditar las variables cuantitativas.
[R] Resultado: Se confirmó un dataset limpio (1,000 filas × 17 columnas, 0 nulos), listo para la fase de transformación analítica.

2. Gobernanza y Traduccíón de Encabezados (Estandarización)
[P] Problema: Los nombres de columnas originales en inglés ('Branch', 'Product line', 'gross income') no se alinean con los estándares de reporte para los usuarios finales de la cadena.
[D] Decisión: Mapear y renombrar programáticamente todas las columnas del DataFrame a español con formato snake_case / PascalCase claro.
[A] Acción: Creación de un diccionario de mapeo en Python (columnas_espanol) y ejecución de df.rename(columns=...).
[R] Resultado: Encabezados estandarizados ('Sucursal', 'Linea_Producto', 'Ganancia_Bruta', 'Ventas_Totales') garantizando consistencia en todo el pipeline.

3. Agregación de Métricas y Creación de Data Marts Resumidos
[P] Problema: Las 1,000 filas de transacciones atómicas no proporcionan una visión ejecutiva inmediata sobre el rendimiento por tienda o categoría.
[D] Decisión: Utilizar operaciones de agrupación (groupby) en Pandas para calcular KPIs clave (Ventas Totales, Ganancia Bruta, Ticket Promedio y Rating) a nivel de Sucursal y Línea de Producto.
[A] Acción: Generación de los DataFrames 'resumen_sucursal' y 'resumen_productos' con agregaciones numéricas (.sum(), .mean()) redondeadas a 2 decimales.
[R] Resultado: Dos tablas consolidadas listas para ser transferidas automáticamente a Google Sheets vía API sin sobrecargar la hoja de cálculo con procesamiento pesado.

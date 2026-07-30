# =========================================================
# FASE 0: CARGA Y EXPLORACION INICIAL
# =========================================================

import pandas as pd
import numpy as np
df = pd.read_csv('/content/drive/MyDrive/Caso de estudio 2 Supermercado/CSV data/supermarket_Sales.csv')
df.shape
df.info()
df.describe().round(2)

# =========================================================
# FASE 1: LIMPIEZA (Renombrado a Español)
# =========================================================
# Diccionario con el mapeo de las columnas
columnas_espanol = {
    'Invoice ID': 'ID_Factura',
    'Branch': 'Sucursal',
    'City': 'Ciudad',
    'Customer type': 'Tipo_Cliente',
    'Gender': 'Genero',
    'Product line': 'Linea_Producto',
    'Unit price': 'Precio_Unitario',
    'Quantity': 'Cantidad',
    'Tax 5%': 'Impuesto_5pct',
    'Total': 'Ventas_Totales',
    'Date': 'Fecha',
    'Time': 'Hora',
    'Payment': 'Metodo_Pago',
    'Cost of goods sold': 'Costo_Bienes_Vendidos',
    'Gross margin percentage': 'Porcentaje_Margen_Bruto',
    'Gross income': 'Ganancia_Bruta',
    'Customer stratification rating': 'Evaluacion'
}

# Aplicamos el renombrado
df = df.rename(columns=columnas_espanol)

# Confirmacion
print("--- NOMBRES DE COLUMNAS ACTUALIZADOS ---")
print(df.columns.tolist())

# =========================================================
# FASE 2: TRANSFORMACIÓN Y AGREGACIÓN (Data Marts)
# =========================================================
# ---------------------------------------------------------
# CONSULTA 1: Rendimiento por Sucursal
# ---------------------------------------------------------

resumen_sucursal = df.groupby('Sucursal').agg(
    Ventas_Totales=('Ventas_Totales', 'sum'),
    Costo_Total=('Costo_Bienes_Vendidos', 'sum'),
    Ganancia_Bruta=('Ganancia_Bruta', 'sum'),
    Ticket_Promedio=('Ventas_Totales', 'mean'),
    Rating_Promedio=('Evaluacion', 'mean')
).reset_index()

# Calculamos el % de Margen Bruto
resumen_sucursal['Pct_Margen_Bruto'] = (
    (resumen_sucursal['Ganancia_Bruta'] / resumen_sucursal['Ventas_Totales']) * 100
)

# Redondeamos a 2 decimales para limpieza ejecutiva
resumen_sucursal = resumen_sucursal.round(2)

print("--- 1. RENDIMIENTO POR SUCURSAL ---")
print(resumen_sucursal)

# ---------------------------------------------------------
# CONSULTA 2: Análisis por Línea de Producto
# ---------------------------------------------------------

resumen_productos = df.groupby('Linea_Producto').agg(
    Ventas_Totales=('Ventas_Totales', 'sum'),
    Cantidad_Vendida=('Cantidad', 'sum'),
    Ganancia_Bruta=('Ganancia_Bruta', 'sum')
).reset_index().sort_values(by='Ventas_Totales', ascending=False)

resumen_productos = resumen_productos.round(2)

print("\n--- 2. RENDIMIENTO POR LÍNEA DE PRODUCTO ---")
print(resumen_productos)

# ---------------------------------------------------------
# CONSULTA 3: Preferencia de Pago por Sucursal
# ---------------------------------------------------------

resumen_pagos = df.groupby(['Sucursal', 'Metodo_Pago']).agg(
    Transacciones=('ID_Factura', 'count'),
    Ventas_Totales=('Ventas_Totales', 'sum')
).reset_index().sort_values(by=['Sucursal', 'Ventas_Totales'], ascending=[True, False])

resumen_pagos = resumen_pagos.round(2)

print("\n--- 3. MÉTODOS DE PAGO POR SUCURSAL ---")
print(resumen_pagos)

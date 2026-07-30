Python
# =========================================================
# FASE 1: INGESTA Y LIMPIEZA (Renombrado a Español)
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
# (Aquí van los 3 groupby de sucursal, productos y pagos)

# =========================================================
# FASE 3: CARGA CLOUD (Google Sheets API - gspread)
# =========================================================
# (Aquí irá el código de conexión a la API)

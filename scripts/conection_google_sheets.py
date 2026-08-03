# =========================================================
# FASE 3: CARGA CLOUD (Google Sheets API - gspread)
# =========================================================
import pandas as pd
import gspread
from google.colab import auth
from google.auth import default

NOMBRE_SPREADSHEET = "Retail_Sales_Dashboard"

try:
    # Abrir el libro de trabajo
    sh = gc.open(NOMBRE_SPREADSHEET)

    # A) Actualizar Pestaña de Datos Crudos / Procesados
    ws_datos = sh.worksheet("datos_ventas")
    ws_datos.clear()
    ws_datos.update([df.columns.values.tolist()] + df.fillna('').values.tolist())

    # B) Actualizar Pestaña de Resumen Sucursal
    ws_sucursal = sh.worksheet("ventas_sucursal")
    ws_sucursal.clear()
    ws_sucursal.update([resumen_sucursal.columns.values.tolist()] + resumen_sucursal.fillna('').values.tolist())

    # C) Actualizar Pestaña de Resumen Pagos
    ws_pago = sh.worksheet("metodos_pago")
    ws_pago.clear()
    ws_pago.update([resumen_pago.columns.values.tolist()] + resumen_pago.fillna('').values.tolist())

    print("✅ ¡Sincronización exitosa! Los datos se actualizaron en Google Sheets.")

except Exception as e:
    print(f"❌ Ocurrió un error al actualizar Google Sheets: {e}")

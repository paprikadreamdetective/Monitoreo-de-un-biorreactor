# --- Módulo de generación de Excel ---
import sqlite3
import os 
import pandas as pd
import flet as ft

class ExcelGenerator:
    def __init__(self, db_file="db/sensores.db"):
        self.db_file = db_file

    def generar_excel(self, e, page):
        conn = sqlite3.connect(self.db_file)
        query = "SELECT * FROM lecturas_sensores"  # Cambia esto al nombre de tu tabla
        df = pd.read_sql_query(query, conn)
        nombre_excel = "lecturas_sensores.xlsx"

        if os.path.exists(nombre_excel):
            os.remove(nombre_excel)

        df.to_excel(nombre_excel, index=False)
        page.snack_bar = ft.SnackBar(ft.Text(f"Archivo {nombre_excel} generado con éxito!"), open=True)
        page.update()
        conn.close()
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

        try:
            # Intentar eliminar el archivo si ya existe
            if os.path.exists(nombre_excel):
                os.remove(nombre_excel)

            # Intentar generar el archivo Excel
            df.to_excel(nombre_excel, index=False)
            mensaje = f"Archivo '{nombre_excel}' generado con éxito!"

        except PermissionError:
            # Error si el archivo está abierto
            mensaje = f"Error: El archivo '{nombre_excel}' está abierto. Ciérralo e inténtalo de nuevo."
        
        except Exception as e:
            # Captura de otros errores
            mensaje = f"Error al generar el archivo: {str(e)}"
        
        finally:
            conn.close()

        # Función para cerrar el diálogo
        def cerrar_dialogo(e):
            dialogo.open = False
            page.update()

        # Crear un cuadro de diálogo para mostrar el mensaje
        dialogo = ft.AlertDialog(
            title=ft.Text("Generación de Excel"),
            content=ft.Text(mensaje),
            actions=[ft.TextButton("Cerrar", on_click=cerrar_dialogo)],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Mostrar el diálogo
        page.dialog = dialogo
        dialogo.open = True
        page.update()


    '''
    def generar_excel(self, e, page):
        conn = sqlite3.connect(self.db_file)
        query = "SELECT * FROM lecturas_sensores"  # Cambia esto al nombre de tu tabla
        df = pd.read_sql_query(query, conn)
        nombre_excel = "lecturas_sensores.xlsx"

        if os.path.exists(nombre_excel):
            os.remove(nombre_excel)

        df.to_excel(nombre_excel, index=False)
        
        def cerrar_diaglogo():
            dialogo.open = False


        # Crear un contenedor con tamaño fijo y scrollbar
        container = ft.Container(
            width=600,
            height=400,
            content=ft.Text(""),
        )

        dialogo = ft.AlertDialog(
            title=ft.Text("Datos de Sensores"),
            content=container,
            actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo())],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        #page.snack_bar = ft.SnackBar(ft.Text(f"Archivo {nombre_excel} generado con éxito!"), open=True)
        #page.update()
        conn.close()
        '''
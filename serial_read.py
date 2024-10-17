from proxydb import SensorDataInserterSQLite
from SerialConnection import SerialConnection
from ExcelGenerator import ExcelGenerator
from Chart import Chart
from SensorDataReader import SensorDataReader


import time
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import sqlite3
import threading
# --- Módulo principal de la interfaz gráfica ---
def main(page: ft.Page):
    # Tamaño de la ventana
    page.title = "Gráfica de Sensores en Tiempo Real"
    page.window_width = 1000
    page.window_height = 600
    # Crear instancias de las clases
    serial_connection = SerialConnection()
    inserter = SensorDataInserterSQLite(db_file="db/sensores.db")
    sensor_graph = Chart()
    excel_generator = ExcelGenerator()
    
    # Conectar el puerto serial
    #ser = serial_connection.begin()
    data_reader = SensorDataReader(serial_connection, sensor_graph, inserter)
    # Crear gráfica y agregarla a la página
    chart = MatplotlibChart(sensor_graph.fig, expand=True)
    page.add(chart)

   
    # Función de actualización del gráfico
    def update_chart():
        sensor_graph.update(chart)
    
    # Función de inicio de lectura serial
    def start_reading_serial(e):
        if serial_connection.is_connected():
            print("La conexión serial ya está activa.")
            return

        if serial_connection.begin():
            data_reader.start_reading()
            threading.Thread(target=read_data_loop, daemon=True).start()
            global start_time
            start_time = time.time()  # Iniciar cronómetro
        else:
            print("Error al iniciar la conexión serial.")

    # Bucle de lectura de datos en un hilo separado
    def read_data_loop():
        while data_reader.reading_active:
            data_reader.read_serial_data()
            update_chart()

    # Función para detener la lectura serial
    def stop_reading_serial(e=None):
        data_reader.stop_reading()
        serial_connection.disconnect()
        print("Lectura serial detenida.")

    # Función para mostrar la ventana con los datos de la base de datos en formato de tabla
    def mostrar_datos(e):
        # Conectar a la base de datos SQLite
        conn = sqlite3.connect('db/sensores.db')
        cursor = conn.cursor()

        # Ejecutar consulta
        cursor.execute("SELECT * FROM lecturas_sensores")  # Ajustar la consulta según la estructura de tu tabla
        datos = cursor.fetchall()

        # Crear encabezados de la tabla
        encabezados = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Sensor MQ-135")),
            ft.DataColumn(ft.Text("Sensor MQ-3")),
        ]

        # Crear filas con los datos de la consulta
        filas = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(fila[0]))),  # ID
                    ft.DataCell(ft.Text(fila[1])),       # Fecha
                    ft.DataCell(ft.Text(str(fila[2]))),  # MQ-135
                    ft.DataCell(ft.Text(str(fila[3]))),  # MQ-3
                ]
            )
            for fila in datos
        ]

        # Crear la tabla con los encabezados y filas
        tabla = ft.DataTable(
            columns=encabezados,
            rows=filas,
            column_spacing=10,
            heading_row_height=30,
            
        )

        # Crear un contenedor con tamaño fijo y scrollbar
        container = ft.Container(
            width=600,
            height=400,
            content=ft.ListView(
                controls=[tabla],   # Incluir la tabla en el ListView
                expand=True,
                auto_scroll=False,  # Desactivar autoscroll para usar scrollbar manual
            )
        )

        # Crear un diálogo para mostrar la tabla
        dialogo = ft.AlertDialog(
            title=ft.Text("Datos de Sensores"),
            content=container,
            actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo())],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Función para cerrar el diálogo
        def cerrar_dialogo():
            dialogo.open = False
            page.update()

        # Mostrar el diálogo
        page.dialog = dialogo
        dialogo.open = True
        page.update()

   
    exit_button = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.EXIT_TO_APP, color="white"),
                ft.Text("Salir", color="white"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5,
        ),
        width=150,  # Hacer el botón más ancho
        bgcolor="red",
        on_click=lambda e: page.window_close(),  # Acción para cerrar la aplicación
    )

    # Añadir el botón de salida con alineación inferior izquierda
    

    # Crear botones con íconos y centrarlos
    botones = ft.Row(
        [
            ft.ElevatedButton(
                content=ft.Row(
                    [
                        ft.Icon(name=ft.icons.SENSOR_WINDOW, color="blue"),
                        ft.Text("Mostrar Datos de Sensores"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                ),
                on_click=mostrar_datos,
            ),
            ft.ElevatedButton(
                content=ft.Row(
                    [
                        ft.Icon(name=ft.icons.START, color="green"),
                        ft.Text("Iniciar Lectura Serial"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                ),
                on_click=start_reading_serial,
            ),
            ft.ElevatedButton(
                content=ft.Row(
                    [
                        ft.Icon(name=ft.icons.STOP, color="red"),
                        ft.Text("Terminar Lectura Serial"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                ),
                on_click=stop_reading_serial,
            ),
            ft.ElevatedButton(
                content=ft.Row(
                    [
                        ft.Icon(name=ft.icons.FILE_DOWNLOAD, color="purple"),
                        ft.Text("Generar Excel"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                ),
                on_click=lambda e: excel_generator.generar_excel(e, page),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,  # Centrar todos los botones
        spacing=10,
    )

    # Añadir los botones centrados a la página
    page.add(botones)

     # Añadir el botón de salida sin bloquear los demás elementos
    page.add(
        ft.Container(
            content=exit_button,
            alignment=ft.alignment.bottom_left,
            padding=ft.padding.only(left=5, bottom=1),
        )
    )
     # Crear un botón de salida más ancho en la esquina inferior izquierda
    

    # Al cerrar la página, desconectar el puerto serial
    page.on_close = lambda _: serial_connection.disconnect()

# Ejecutar la aplicación Flet
ft.app(target=main)
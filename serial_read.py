from proxydb import SensorDataInserterSQLite
from SerialConnection import SerialConnection
from ExcelGenerator import ExcelGenerator
from Chart import Chart
from SensorDataReader import SensorDataReader


import time
import flet as ft
from flet.matplotlib_chart import MatplotlibChart


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
    ser = serial_connection.begin()

    # Crear gráfica y agregarla a la página
    chart = MatplotlibChart(sensor_graph.fig, expand=True)
    page.add(chart)

    # Función de actualización del gráfico
    def update_chart():
        sensor_graph.update(chart)

    # Función de lectura de datos seriales
    def start_reading_serial(e):
        data_reader = SensorDataReader(ser, sensor_graph, inserter)
        while data_reader.read_serial_data():
            update_chart()
    
    def stop_reading_serial(e):
        serial_connection.disconnect(ser)

    # Botón para iniciar la lectura serial
    page.add(ft.ElevatedButton("Iniciar Lectura Serial", on_click=start_reading_serial))
    page.add(ft.ElevatedButton("Terminar Lectura Serial", on_click=stop_reading_serial))
    # Botón para generar el archivo Excel
    page.add(ft.ElevatedButton("Generar Excel", on_click=lambda e: excel_generator.generar_excel(e, page)))
    
    # Al cerrar la página, desconectar el puerto serial
    page.on_close = lambda _: serial_connection.disconnect(ser)

# Ejecutar la aplicación Flet
ft.app(target=main)
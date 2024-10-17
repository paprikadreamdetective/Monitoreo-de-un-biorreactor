import serial
import time
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import matplotlib.pyplot as plt
from collections import deque
import pandas as pd
import sqlite3
import os

# Importar la clase para insertar datos en SQLite
from proxydb import SensorDataInserterSQLite

# --- Módulo de configuración del puerto serial ---
class SerialConfig:
    def __init__(self, port='COM6', baud_rate=9600, timeout=1):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout

    def connect(self):
        try:
            ser = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            print(f"Conectado al puerto {self.port}")
            return ser
        except serial.SerialException as e:
            print(f"Error de conexión: {e}")
            return None

    def disconnect(self, ser):
        if ser and ser.is_open:
            ser.close()
            print(f"Conexión serial cerrada en {self.port}")

# --- Módulo de manejo de gráficas ---
class SensorGraph:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.line_mq135, = self.ax.plot([], [], label="MQ-135 (Calidad del aire)")
        self.line_mq3, = self.ax.plot([], [], label="MQ-3 (Etanol)")
        self.mq135_buffer = deque(maxlen=100)
        self.mq3_buffer = deque(maxlen=100)
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 1023)
        self.ax.legend(loc="upper right")
    
    def update(self, chart):
        self.line_mq135.set_xdata(range(len(self.mq135_buffer)))  # Eje X para MQ-135
        self.line_mq135.set_ydata(self.mq135_buffer)  # Eje Y para MQ-135
        self.line_mq3.set_xdata(range(len(self.mq3_buffer)))  # Eje X para MQ-3
        self.line_mq3.set_ydata(self.mq3_buffer)  # Eje Y para MQ-3
        self.ax.relim()  # Recalcular límites
        self.ax.autoscale_view()  # Ajustar la vista
        chart.update()  # Actualizar la gráfica en Flet
    
    def add_data(self, mq135_value, mq3_value):
        self.mq135_buffer.append(mq135_value)
        self.mq3_buffer.append(mq3_value)

# --- Módulo de lectura de datos seriales ---
class SensorDataReader:
    def __init__(self, serial_connection, graph, inserter):
        self.serial_connection = serial_connection
        self.graph = graph
        self.inserter = inserter
    
    def read_serial_data(self):
        try:
            while True:
                if self.serial_connection.in_waiting > 0:
                    data = self.serial_connection.readline().decode('utf-8').strip()
                    print(f"Datos recibidos: {data}")
                    valores = data.split(',')
                    if len(valores) == 2:
                        mq135_valor = int(valores[0])
                        mq3_valor = int(valores[1])
                        fecha_valor = time.ctime()
                        self.graph.add_data(mq135_valor, mq3_valor)
                        self.inserter.insertar_datos(fecha_valor, mq135_valor, mq3_valor)
                        return True
        except serial.SerialException as e:
            print(f"Error en la lectura serial: {e}")
            return False
        return False

# --- Módulo de generación de Excel ---
class ExcelGenerator:
    def __init__(self, db_file="sensores.db"):
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

# --- Módulo principal de la interfaz gráfica ---
def main(page: ft.Page):
    # Configuración de la página
    page.title = "Gráfica de Sensores en Tiempo Real"
    page.window_width = 800
    page.window_height = 600

    # Crear instancias de los módulos
    serial_config = SerialConfig()
    inserter = SensorDataInserterSQLite(db_file="sensores.db")
    sensor_graph = SensorGraph()
    excel_generator = ExcelGenerator()

    # Conectar el puerto serial
    ser = serial_config.connect()

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

    # Botón para iniciar la lectura serial
    page.add(ft.ElevatedButton("Iniciar Lectura Serial", on_click=start_reading_serial))

    # Botón para generar el archivo Excel
    page.add(ft.ElevatedButton("Generar Excel", on_click=lambda e: excel_generator.generar_excel(e, page)))

    # Al cerrar la página, desconectar el puerto serial
    page.on_close = lambda _: serial_config.disconnect(ser)

# Ejecutar la aplicación Flet
ft.app(target=main)



'''

import serial
import time
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import matplotlib.pyplot as plt
from collections import deque
from proxydb import SensorDataInserterSQLite
import pandas as pd
import sqlite3
import os

def main(page: ft.Page):
    # Configurar el puerto serial
    arduino_port = 'COM6'  # Cambia esto según tu puerto
    baud_rate = 9600  # Velocidad de transmisión (baud rate)
    timeout = 1  # Tiempo de espera en segundos para la lectura
    ser = serial.Serial(arduino_port, baud_rate, timeout=timeout)

    # Buffer para los datos (almacenará los últimos 100 valores)
    mq135_buffer = deque(maxlen=100)
    mq3_buffer = deque(maxlen=100)

    inserter = SensorDataInserterSQLite(db_file="sensores.db")
    # Configuración inicial de la ventana
    page.title = "Gráfica de Sensores en Tiempo Real"
    page.window_width = 800
    page.window_height = 600
    
    # Crear una figura de matplotlib
    fig, ax = plt.subplots()
    line_mq135, = ax.plot([], [], label="MQ-135 (Calidad del aire)")
    line_mq4, = ax.plot([], [], label="MQ-3 (Etanol)")
    
    ax.set_xlim(0, 100)  # Eje X de 0 a 100
    ax.set_ylim(0, 1023)  # Eje Y ajustado para un valor de 10 bits (0 a 1023)
    ax.legend(loc="upper right")  # Mostrar la leyenda de los sensores

    # Inicializar la gráfica en la app de Flet
    chart = MatplotlibChart(fig, expand=True)

    # Agregar el gráfico a la página
    page.add(chart)

    def update_chart():
        # Actualizar la gráfica con los nuevos datos
        line_mq135.set_xdata(range(len(mq135_buffer)))  # Eje X para MQ-135
        line_mq135.set_ydata(mq135_buffer)  # Eje Y para MQ-135
        
        line_mq4.set_xdata(range(len(mq3_buffer)))  # Eje X para MQ-4
        line_mq4.set_ydata(mq3_buffer)  # Eje Y para MQ-4
        
        ax.relim()  # Recalcular límites de los datos
        ax.autoscale_view()  # Ajustar la vista de la gráfica
        chart.update()  # Actualizar la gráfica en Flet

    def read_serial_data():
        try:
            print(f"Conectado al puerto {arduino_port}")
            time.sleep(2)  # Esperar a que el Arduino se inicialice
            while True:
                if ser.in_waiting > 0:  # Verificar si hay datos disponibles
                    data = ser.readline().decode('utf-8').strip()  # Leer y decodificar los datos
                    print(f"Datos recibidos: {data}")
                    # Separar los valores usando la coma como delimitador
                    valores = data.split(',')
                    if len(valores) == 2:
                        mq135_valor = valores[0]  # Ejemplo de valor del sensor MQ-135
                        mq4_valor = valores[1]    # Ejemplo de valor del sensor MQ-4
                        fecha_valor = time.ctime()
                        mq135_buffer.append(int(mq135_valor))
                        mq3_buffer.append(int(mq4_valor))
                        inserter.insertar_datos(fecha_valor, mq135_valor, mq4_valor)
                        update_chart()  # Actualizar la gráfica en tiempo real
        except serial.SerialException as e:
            print(f"Error de conexión: {e}")
        finally:
            if ser.is_open:
                ser.close()  # Cerrar el puerto serial si está abierto
                print("Conexión serial cerrada")

    def generar_excel(e):
        # Conexión a la base de datos SQLite
        conn = sqlite3.connect("sensores.db")
        query = "SELECT * FROM lecturas_sensores"  # Ajusta esto al nombre de tu tabla
        df = pd.read_sql_query(query, conn)

        # Nombre del archivo Excel
        nombre_excel = "lecturas_sensores.xlsx"
        
        # Si el archivo existe, sobrescribirlo
        if os.path.exists(nombre_excel):
            os.remove(nombre_excel)
        
        # Generar el archivo Excel
        df.to_excel(nombre_excel, index=False)
        
        # Mostrar una notificación en la GUI
        page.snack_bar = ft.SnackBar(ft.Text(f"Archivo {nombre_excel} generado con éxito!"), open=True)
        page.update()
        
        # Cerrar la conexión a la base de datos
        conn.close()

    # Botón para iniciar la lectura serial
    page.add(ft.ElevatedButton("Iniciar Lectura Serial", on_click=lambda _: read_serial_data()))
    
    # Botón para generar el archivo Excel
    page.add(ft.ElevatedButton("Generar Excel", on_click=generar_excel))

# Correr la aplicación Flet
ft.app(target=main)
'''
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
import serial
import time
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import matplotlib.pyplot as plt
from collections import deque
from proxydb import SensorDataInserterSQLite

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
    #ig, ax = plt.subplots()
    #line, = ax.plot([], [], label="Datos del sensor")
    #ax.set_xlim(0, 100)  # Eje X de 0 a 100
    #ax.set_ylim(0, 1023)  # Eje Y ajustado para un valor de 10 bits (0 a 1023)

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
        #line.set_xdata(range(len(data_buffer)))  # Actualizar los valores del eje X
        #line.set_ydata(data_buffer)  # Actualizar los valores del eje Y
        #ax.relim()  # Recalcular límites de los datos
        #ax.autoscale_view()  # Ajustar la vista de la gráfica
        #chart.update()  # Actualizar la gráfica en Flet
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
                    #if data.isdigit():  # Verificar que los datos sean números
                    if len(valores) == 2:
                        #data_buffer.append(int(data))  # Agregar los datos al buffer
                        print(f"Datos recibidos: {data}")  # Imprimir datos recibidos
                        mq135_valor = valores[0]  # Ejemplo de valor del sensor MQ-135
                        mq4_valor = valores[1]    # Ejemplo de valor del sensor MQ-4
                        fecha_valor = time.ctime()
                        # Agregar los valores a tu buffer o hacer lo que sea necesario con ellos
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

    # Iniciar el proceso de lectura serial en otro hilo
    page.add(ft.ElevatedButton("Iniciar Lectura Serial", on_click=lambda _: read_serial_data()))

# Correr la aplicación Flet
ft.app(target=main)
'''
# --- Módulo de manejo de gráficas ---
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import matplotlib.pyplot as plt
from collections import deque
import time
'''
class State:
    toggle = True

class Chart:
    def __init__(self):
        self.mq135_buffer = deque(maxlen=100)
        self.mq3_buffer = deque(maxlen=100)
        self.time_buffer = deque(maxlen=100)
        self.start_time = time.time()
    
    def update(self, chart):
        data_mq135 = [
            ft.LineChartDataPoint(x, y) for x, y in zip(self.time_buffer, self.mq135_buffer)
        ]
        data_mq3 = [
            ft.LineChartDataPoint(x, y) for x, y in zip(self.time_buffer, self.mq3_buffer)
        ]

        chart.data_series = [
            ft.LineChartData(data_points=data_mq135, stroke_width=4, color=ft.colors.LIGHT_GREEN, curved=True),
            ft.LineChartData(data_points=data_mq3, stroke_width=4, color=ft.colors.PINK, curved=True),
        ]
        chart.update()
    
    def add_data(self, mq135_value, mq3_value):
        #current_time = time.time() - self.start_time
        current_time = round(time.time() - self.start_time, 2)  # Redondear el tiempo a 2 decimales
        self.time_buffer.append(current_time)
        self.mq135_buffer.append(mq135_value)
        self.mq3_buffer.append(mq3_value)

'''
class Chart:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.line_mq135, = self.ax.plot([], [], label="MQ-135 (Calidad del aire)")
        self.line_mq3, = self.ax.plot([], [], label="MQ-3 (Etanol)")
        self.mq135_buffer = deque(maxlen=100)
        self.mq3_buffer = deque(maxlen=100)
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 5)
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

# --- Módulo de manejo de gráficas ---
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import matplotlib.pyplot as plt
from collections import deque

class Chart:
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
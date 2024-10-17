import serial
import time
# --- Módulo de lectura de datos seriales ---


class SensorDataReader:
    def __init__(self, serial_connection, graph, inserter):
        self.serial_connection = serial_connection
        self.graph = graph
        self.inserter = inserter
        self.reading_active = False
    
    def read_serial_data(self):
        try:
            while self.reading_active and self.serial_connection.serial_conn.in_waiting > 0:
                data = self.serial_connection.serial_conn.readline().decode('utf-8').strip()
                print(f"Datos recibidos: {data}")
                valores = data.split(',')
                if len(valores) == 2:
                    mq135_valor = float(valores[0])
                    mq3_valor = float(valores[1])
                    fecha_valor = time.ctime()
                    self.graph.add_data(mq135_valor, mq3_valor)
                    self.inserter.insertar_datos(fecha_valor, mq135_valor, mq3_valor)
            return True
        except serial.SerialException as e:
            print(f"Error en la lectura serial: {e}")
            return False

    def start_reading(self):
        self.reading_active = True

    def stop_reading(self):
        self.reading_active = False

    '''
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
    '''

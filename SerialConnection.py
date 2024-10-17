import serial

class SerialConnection:
    def __init__(self, port='COM6', baud_rate=9600, timeout=1):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout

    def begin(self):
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
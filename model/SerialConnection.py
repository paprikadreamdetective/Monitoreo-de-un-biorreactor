import serial

class SerialConnection:
    def __init__(self, port='COM6', baud_rate=9600, timeout=1):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.serial_conn = None

    def is_connected(self):
        return self.serial_conn is not None and self.serial_conn.is_open

    def begin(self):
        try:
            self.serial_conn = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            print(f"Conectado al puerto {self.port}")
            return True
        except serial.SerialException as e:
            print(f"Error de conexión: {e}")
            return False

    def disconnect(self):
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print(f"Conexión serial cerrada en {self.port}")
            self.serial_conn = None
            #ser.close()
            #print(f"Conexión serial cerrada en {self.port}")
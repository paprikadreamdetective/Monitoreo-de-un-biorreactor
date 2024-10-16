import serial
import time

# Configurar el puerto serial
# Asegúrate de que el puerto COM sea el correcto, puede ser COM3, COM4, etc.
# Baudrate debe coincidir con la velocidad de transmisión configurada en el Arduino
arduino_port = 'COM6'  # Cambia esto según tu puerto
baud_rate = 9600  # Velocidad de transmisión (baud rate)
timeout = 1  # Tiempo de espera en segundos para la lectura
ser = serial.Serial(arduino_port, baud_rate, timeout=timeout)
try:
    # Abrir el puerto serial

    print(f"Conectado al puerto {arduino_port}")

    time.sleep(2)  # Esperar a que el Arduino se inicialice

    while True:
        # Leer línea del puerto serial
        if ser.in_waiting > 0:  # Verificar si hay datos disponibles
            data = ser.readline().decode('utf-8').strip()  # Leer y decodificar los datos
            print(f"Datos recibidos: {data}")  # Imprimir datos recibidos

except serial.SerialException as e:
    print(f"Error de conexión: {e}")
finally:
    if ser.is_open:
        ser.close()  # Cerrar el puerto serial si está abierto
        print("Conexión serial cerrada")

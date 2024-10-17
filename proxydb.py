import sqlite3
import time

class SensorDataInserterSQLite:
    def __init__(self, db_file):
        # Conexión a la base de datos SQLite
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        print("Conectado a la base de datos SQLite")
        
        # Crear la tabla si no existe
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS lecturas_sensores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                sensor_mq135 INTEGER NOT NULL,
                sensor_mq3 INTEGER NOT NULL
            )
        ''')
        self.connection.commit()

    def insertar_datos(self, fecha_valor, mq135_valor, mq4_valor):
        try:
            # Crear la consulta SQL para insertar los datos
            sql = "INSERT INTO lecturas_sensores (fecha, sensor_mq135, sensor_mq3) VALUES (?, ?, ?)"
            values = (fecha_valor, mq135_valor, mq4_valor)
            
            # Ejecutar la consulta
            self.cursor.execute(sql, values)
            
            # Confirmar cambios en la base de datos
            self.connection.commit()
            print(f"{fecha_valor} - Datos insertados: MQ-135 = {mq135_valor}, MQ-3 = {mq4_valor}")
        
        except sqlite3.Error as e:
            print(f"Error al insertar los datos: {e}")
            self.connection.rollback()
    
    def cerrar_conexion(self):
        # Cerrar cursor y conexión
        self.cursor.close()
        self.connection.close()
        print("Conexión a la base de datos cerrada")

'''
# Ejemplo de uso de la clase
if __name__ == "__main__":
    # Crear un objeto de la clase e insertar un dato de prueba
    inserter = SensorDataInserterSQLite(db_file="sensores.db")
    
    # Simulación de datos de sensores
    mq135_valor = 300  # Ejemplo de valor del sensor MQ-135
    mq4_valor = 200    # Ejemplo de valor del sensor MQ-4
    
    inserter.insertar_datos(mq135_valor, mq4_valor)
    
    # Cerrar la conexión
    inserter.cerrar_conexion()
'''
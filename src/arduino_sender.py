import serial
import time
from config import ARDUINO_PORT, ARDUINO_BAUDRATE

class ArduinoSender:
    def __init__(self, sensores_identificados):
        self.arduino = serial.Serial(ARDUINO_PORT, ARDUINO_BAUDRATE, timeout=1)
        time.sleep(2)  # Esperar que Arduino reinicie
        self.sensores_identificados = sensores_identificados

    def enviar_datos(self, datos_sensores: dict):
        mensaje = "<"
        partes = []
        for nombre, valor in datos_sensores.items():
            partes.append(f"{nombre}:{valor:.2f}")
        mensaje += ",".join(partes) + ">\n"
        self.arduino.write(mensaje.encode('utf-8'))
        print(f"Datos enviados a Arduino: {mensaje.strip()}")

    def cerrar(self):
        self.arduino.close()
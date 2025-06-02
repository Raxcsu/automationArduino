import serial
import time
from datetime import datetime
from config import SERIAL_PORT, BAUDRATE, TIME_DELAY, SEND_INTERVAL
from sensors.factory import SensorFactory
from arduino_sender import ArduinoSender
from logger import configurar_logger

class Manager:
    def __init__(self, sensores):
        self.sensores = sensores
        self.logger = configurar_logger()
        self.sensores_identificados = self.asignar_nombres_sensores()
        self.sender = ArduinoSender(self.sensores_identificados)

    def asignar_nombres_sensores(self):
        nombres = {}
        ph_count, ox_count = 1, 1
        for sensor in self.sensores:
            if sensor.__class__.__name__ == 'SensorPH':
                nombre = f"PH{ph_count}"
                ph_count += 1
            elif sensor.__class__.__name__ == 'SensorOxigeno':
                nombre = f"OX{ox_count}"
                ox_count += 1
            else:
                nombre = sensor.codigo_sensor
            nombres[sensor.codigo_sensor] = nombre
        return nombres

    def run(self):
        with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1) as ser:
            print(f"Conectado a {SERIAL_PORT}")
            last_send_time = time.time()
            datos_sensores = {}

            while True:
                raw = ser.readline()
                if raw:
                    linea = raw.decode('utf-8', errors='replace').strip()
                    sensor = SensorFactory.crear_sensor(linea)
                    if sensor:
                        data = sensor.parsear_linea(linea)
                        nombre = self.sensores_identificados.get(sensor.codigo_sensor, None)
                        if nombre:
                            if nombre.startswith("PH"):
                                datos_sensores[nombre] = data['ph']
                            elif nombre.startswith("OX"):
                                datos_sensores[nombre] = data['oxigeno']

                        if time.time() - last_send_time >= SEND_INTERVAL:
                            self.sender.enviar_datos(datos_sensores)
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            self.logger.info(f"{timestamp} | Datos sensores enviados: {datos_sensores}")
                            last_send_time = time.time()

                time.sleep(TIME_DELAY)

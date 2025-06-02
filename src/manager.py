# import serial
# import time
# import threading
# from datetime import datetime
# from config import SERIAL_PORTS, BAUDRATE, TIME_DELAY, SEND_INTERVAL
# from sensors.factory import SensorFactory
# from arduino_sender import ArduinoSender
# from logger import configurar_logger

# class Manager:
#     def __init__(self, sensores):
#         self.sensores = sensores
#         self.logger = configurar_logger()
#         self.sensores_identificados = self.asignar_nombres_sensores()
#         self.sender = ArduinoSender(self.sensores_identificados)
#         self.datos_sensores = {}
#         self.lock = threading.Lock()

#     def asignar_nombres_sensores(self):
#         nombres = {}
#         ph_count, ox_count = 1, 1
#         for sensor in self.sensores:
#             if sensor.__class__.__name__ == 'SensorPH':
#                 nombre = f"PH{ph_count}"
#                 ph_count += 1
#             elif sensor.__class__.__name__ == 'SensorOxigeno':
#                 nombre = f"OX{ox_count}"
#                 ox_count += 1
#             else:
#                 nombre = sensor.codigo_sensor
#             nombres[sensor.codigo_sensor] = nombre
#         return nombres

#     def run(self):
#         with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1) as ser:
#             print(f"Conectado a {SERIAL_PORT}")
#             last_send_time = time.time()
#             datos_sensores = {}

#             while True:
#                 raw = ser.readline()
#                 if raw:
#                     linea = raw.decode('utf-8', errors='replace').strip()
#                     sensor = SensorFactory.crear_sensor(linea)
#                     if sensor:
#                         data = sensor.parsear_linea(linea)
#                         nombre = self.sensores_identificados.get(sensor.codigo_sensor, None)
#                         if nombre:
#                             if nombre.startswith("PH"):
#                                 datos_sensores[nombre] = data['ph']
#                             elif nombre.startswith("OX"):
#                                 datos_sensores[nombre] = data['oxigeno']

#                         if time.time() - last_send_time >= SEND_INTERVAL:
#                             self.sender.enviar_datos(datos_sensores)
#                             timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                             self.logger.info(f"{timestamp} | Datos sensores enviados: {datos_sensores}")
#                             last_send_time = time.time()

#                 time.sleep(TIME_DELAY)

import serial
import time
import threading
from datetime import datetime
from config import SERIAL_PORTS, BAUDRATE, TIME_DELAY, SEND_INTERVAL
from sensors.factory import SensorFactory
from arduino_sender import ArduinoSender
from logger import configurar_logger

class Manager:
    def __init__(self, sensores):
        self.sensores = sensores
        self.logger = configurar_logger()
        self.sensores_identificados = self.asignar_nombres_sensores()
        self.sender = ArduinoSender(self.sensores_identificados)
        self.datos_sensores = {}
        self.lock = threading.Lock()

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

    def leer_puerto(self, puerto):
        try:
            with serial.Serial(puerto, BAUDRATE, timeout=1) as ser:
                print(f"Escuchando en {puerto}")
                while True:
                    raw = ser.readline()
                    if raw:
                        linea = raw.decode('utf-8', errors='replace').strip()
                        sensor = SensorFactory.crear_sensor(linea)
                        if sensor:
                            data = sensor.parsear_linea(linea)
                            nombre = self.sensores_identificados.get(sensor.codigo_sensor)
                            if nombre:
                                with self.lock:
                                    if nombre.startswith("PH"):
                                        self.datos_sensores[nombre] = data['ph']
                                    elif nombre.startswith("OX"):
                                        self.datos_sensores[nombre] = data['oxigeno']
        except Exception as e:
            print(f"Error en puerto {puerto}: {e}")

    def run(self):
        threads = []
        for puerto in SERIAL_PORTS:
            t = threading.Thread(target=self.leer_puerto, args=(puerto,))
            t.daemon = True
            t.start()
            threads.append(t)

        last_send_time = time.time()
        while True:
            if time.time() - last_send_time >= SEND_INTERVAL:
                with self.lock:
                    self.sender.enviar_datos(self.datos_sensores)
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.logger.info(f"{timestamp} | Datos sensores enviados: {self.datos_sensores}")
                last_send_time = time.time()
            time.sleep(TIME_DELAY)
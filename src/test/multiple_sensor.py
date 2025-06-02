#!/usr/bin/env python3
import RPi.GPIO as GPIO
import serial
import time
from config import SERIAL_PORT, BAUDRATE, PH_MIN, PH_MAX, TIME_DELAY

GPIO.setmode(GPIO.BCM)

class Valvula:
    def __init__(self, gpio_pin: int):
        self.gpio_pin = gpio_pin
        GPIO.setup(self.gpio_pin, GPIO.OUT)

    def abrir(self):
        GPIO.output(self.gpio_pin, GPIO.HIGH)
        print(f"VALVULA en pin {self.gpio_pin} ABIERTA")

    def cerrar(self):
        GPIO.output(self.gpio_pin, GPIO.LOW)
        print(f"VALVULA en pin {self.gpio_pin} CERRADA")

class SensorPH:
    def __init__(self, puerto_serial: str, baudrate: int):
        self.puerto_serial = puerto_serial
        self.baudrate = baudrate

    def parsear_linea(self, linea: str):
        try:
            partes = linea.strip().split(';')
            ph = float(partes[4])
            temp = float(partes[7])
            return ph, temp
        except Exception as e:
            print(f"Error parseando linea: {e}")
            return None, None

    def leer(self):
        with serial.Serial(self.puerto_serial, self.baudrate, timeout=1) as ser:
            raw = ser.readline()
            if raw:
                try:
                    linea = raw.decode('utf-8', errors='replace').strip()
                    return self.parsear_linea(linea)
                except Exception:
                    return None, None
            return None, None

class Controlador:
    def __init__(self, sensor: SensorPH, valvula: Valvula, ph_min: float, ph_max: float):
        self.sensor = sensor
        self.valvula = valvula
        self.ph_min = ph_min
        self.ph_max = ph_max

    def ejecutar(self):
        ph, temp = self.sensor.leer()
        if ph is not None:
            print(f"[Sensor en {self.sensor.puerto_serial}] pH: {ph} | Temp: {temp}C")
            if ph < self.ph_min:
                self.valvula.cerrar()
            elif ph > self.ph_max:
                self.valvula.abrir()
            else:
                self.valvula.cerrar()
        else:
            print(f"No se obtuvo lectura válida en {self.sensor.puerto_serial}")

class Manager:
    def __init__(self, controladores: list, delay: int):
        self.controladores = controladores
        self.delay = delay

    def run(self):
        while True:
            for controlador in self.controladores:
                controlador.ejecutar()
            time.sleep(self.delay)

if __name__ == "__main__":
    sensores_y_valvulas = [
        Controlador(SensorPH("/dev/ttyUSB0", BAUDRATE), Valvula(17), PH_MIN, PH_MAX),
        Controlador(SensorPH("/dev/ttyUSB1", BAUDRATE), Valvula(27), PH_MIN, PH_MAX),
        # Puedes agregar más sensores/válvulas aquí
    ]

    manager = Manager(sensores_y_valvulas, TIME_DELAY)
    manager.run()

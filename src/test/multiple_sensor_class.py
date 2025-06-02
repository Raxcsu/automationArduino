#!/usr/bin/env python3
import RPi.GPIO as GPIO
import serial
import time
from config import SERIAL_PORT, BAUDRATE, PH_MIN, PH_MAX, TIME_DELAY

GPIO.setmode(GPIO.BCM)

class BaseSensor:
    def __init__(self, codigo_sensor: str):
        self.codigo_sensor = codigo_sensor

    @classmethod
    def detectar_sensor(cls, linea: str):
        """Decidir si esta clase puede parsear la línea"""
        raise NotImplementedError

    def parsear_linea(self, linea: str):
        """Extraer datos de la línea"""
        raise NotImplementedError

class SensorPH(BaseSensor):
    PH_MIN = 6.0
    PH_MAX = 8.0

    @classmethod
    def detectar_sensor(cls, linea: str):
        return ";pH;" in linea

    def parsear_linea(self, linea: str):
        partes = linea.strip().split(';')
        ph = float(partes[4])
        temp = float(partes[7])
        return {'ph': ph, 'temp': temp}

class SensorOxigeno(BaseSensor):
    OX_MIN = 5.0
    OX_MAX = 10.0

    @classmethod
    def detectar_sensor(cls, linea: str):
        return ";Ox;" in linea

    def parsear_linea(self, linea: str):
        partes = linea.strip().split(';')
        oxigeno = float(partes[4])
        temp = float(partes[7])
        salinidad = self.extraer_salinidad(linea)
        return {'oxigeno': oxigeno, 'temp': temp, 'salinidad': salinidad}

    def extraer_salinidad(self, linea: str):
        if "Sal = " in linea:
            inicio = linea.find("Sal = ") + len("Sal = ")
            fin = linea.find(" ", inicio)
            return float(linea[inicio:fin])
        return None

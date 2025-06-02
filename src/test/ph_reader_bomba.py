#!/usr/bin/env python3
import RPi.GPIO as GPIO
import serial
import time
from config import SERIAL_PORT, BAUDRATE, PH_MIN, GPIO_RELAY, TIME_DELAY

DELAY_SECONDS = 1
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_RELAY, GPIO.OUT)

def parse_sensor_line(line: str):
	"""
	Extraer el valor de pH y temperatura de una lídea cruda
	Ejemplo:
		b'Multi 3630 IDS; 22420796;1;31.03.2025 17:51:12;
		6.736;;pH;
		24.1;\xb0C;Temp;AR; ;;SenTix 940-3; C212631040;\r\n'
	"""
	try:
		parts = line.strip().split(';')
		ph = float(parts[4])
		temp = float(parts[7])
		return ph, temp
	except Exception as e:
		print(f"Error al parsear la linea: {e}")
		return None, None

def controlar_rele(ph_value):
	if ph_value < PH_MIN:
		GPIO.output(GPIO_RELAY, GPIO.LOW)
		print("VALVULA CERRADA")
		
	elif ph_value > PH_MAX:
		GPIO.output(GPIO_RELAY, GPIO.HIGH)
		print("VALVULA ABIERTA")
		
	else:
		GPIO.output(GPIO_RELAY, GPIO.LOW)
		print("VALVULA CERRADA")

def test_solenoide(ph_value):
	if ph_value > 6:
		GPIO.output(GPIO_RELAY, GPIO.HIGH)
		print("SOLENOIDE PRENDIDO")
	else:
		GPIO.output(GPIO_RELAY, GPIO.LOW)
		print("SOLENOIDE APAGADO")

def get_ph_reading():
	try:
		with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1) as ser:
			print(f"Conectado a {SERIAL_PORT} a {BAUDRATE} baud.")
			while True:
				raw = ser.readline()
				if raw:
					try:
						decoded = raw.decode('utf-8', errors = 'replace').strip()
						ph, temp = parse_sensor_line(decoded)
						#print(raw)
						if ph is not None:
							print(f"pH: {ph} | Temperatura: {temp}C")
							controlar_rele(ph)
							#test_solenoide(ph)
						else:
							print("Formato no reconocido")
					except ValueError:
						print("No data")
						time.sleep(DELAY_SECONDS)
				else:
					print("No se recibio data")
				time.sleep(DELAY_SECONDS)
	except Exception as e:
		print("Error al abrir un puerto")


if __name__ == "__main__":
	get_ph_reading()



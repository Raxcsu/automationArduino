import serial
import time
from config import SERIAL_PORT, BAUDRATE

DELAY_SECONDS = 1

def parse_sensor_line(line: str):
	"""
	Extraer el valor de pH y temperatura de una lídea cruda
	"""
	try:
		parts = line.strip().split(';')
		ph = float(parts[4])
		temp = float(parts[7])
		return ph, temp
	except Exception as e:
		print(f"Error al parsear la linea: {e}")
		return None, None
		
"""
AMARILLO:
	SenTix 940-3
	C212631040
ROJO: AR +++
	SenTix 940
	C161102048
VERDE:
	SenTix 940-3
	08520001
OXIGENO: Sal = 35.0   SC-FDO 925   11143527;FDO 925-3; 11151020;
	SC-FDO 925
	11143527
	FDO 925-3
	11151020
"""

def get_ph_reading():
	try:
		with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1) as ser:
			print(f"Conectado a {SERIAL_PORT} a {BAUDRATE} baud.")
			while True:
				raw = ser.readline()
				if raw:
					try:
						decoded = raw.decode('utf-8', errors = 'replace').strip()
						#ph, temp = parse_sensor_line(decoded)
						print(raw)
						"""
						if ph is not None and temp is not None:
							print(f"pH: {ph} | Temperatura: {temp}C")
						else:
							print("Formato no reconocido")
						"""
					except ValueError:
						print("No data")
				else:
					print("No se recibio data")
				time.sleep(DELAY_SECONDS)
	except Exception as e:
		print("Error al abrir un puerto")


if __name__ == "__main__":
	get_ph_reading()

# b'Multi 3630 IDS; 22420796;1;31.03.2025 17:51:12;6.736;;pH;24.1;\xb0C;Temp;AR; ;;SenTix 940-3; C212631040;\r\n'

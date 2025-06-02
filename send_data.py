import serial
import time
import random

# Configura aquí el puerto donde está conectado tu Arduino
# Windows: "COM3", Linux: "/dev/ttyACM0", Mac: "/dev/tty.usbmodemXXXX"
ARDUINO_PORT = "COM6"  # <-- cambia si es necesario
BAUD_RATE = 9600

# Función para generar datos aleatorios de pH y oxígeno
def generate_sensor_data():
    ph1 = round(random.uniform(7.2, 7.6), 1)
    ph2 = round(random.uniform(7.2, 7.6), 1)
    ox1 = round(random.uniform(10.0, 40.0), 1)
    ox2 = round(random.uniform(10.0, 40.0), 1)
    return f"<PH1:{ph1},PH2:{ph2},OX1:{ox1},OX2:{ox2}>"
    # return f"<OX1:{ox1},PH1:{ph1}>"

def main():
    try:
        print(f"Conectando a {ARDUINO_PORT} a {BAUD_RATE} baud...")
        with serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1) as ser:
            time.sleep(4)  # Esperar a que Arduino reinicie

            while True:
                data = generate_sensor_data()
                ser.write((data + '\n').encode('utf-8'))
                print("Enviado:", data)
                time.sleep(2)  # Enviar cada 2 segundos
                ser.write((data + '\n').encode('utf-8'))

                # Leer respuesta si hay
                if ser.in_waiting:
                    response = ser.readline().decode().strip()
                    print("Arduino respondió:", response)

    except serial.SerialException as e:
        print("Error al conectar con el Arduino:", e)

if __name__ == "__main__":
    main()

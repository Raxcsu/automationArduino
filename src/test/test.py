import serial
from config import SERIAL_PORT, BAUDRATE

def get_ph_reading():
    try:
        with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1) as ser:
            line = ser.readline() #.decode('utf-8').strip()
            if line:
                try:
                    #ph = float(line)
                    ph = line
                    return ph
                except ValueError:
                    print(f"No se pudo convertir la lectura a float: {line}")
    except Exception as e:
        print(f"Error al leer el sensor: {e}")
    return None



# --------------------------------------
# --------------------------------------
#!/usr/bin/env python3
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)

# Right Motor
in1 = 17
in2 = 27
en_a = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en_a,GPIO.OUT)

q=GPIO.PWM(en_a,100)
q.start(75)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

# Wrap main content in a try block so we can  catch the user pressing CTRL-C and run the
# GPIO cleanup function. This will also prevent the user seeing lots of unnecessary error messages.
try:
# Create Infinite loop to read user input
    while(True):
        # Get user Input
        user_input = input()

        # To see users input
        # print(user_input)

        if user_input == 'w':
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)

            print("Forward")

        elif user_input == 's':
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)

            print('Back')

        # Press 'c' to exit the script
        elif user_input == 'c':
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)

            print('Stop')

# If user press CTRL-C
except KeyboardInterrupt:
    # Reset GPIO settings
    GPIO.cleanup()
    print("GPIO Clean up")


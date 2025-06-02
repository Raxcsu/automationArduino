#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)

for i in range(3):
	GPIO.output(PIN, GPIO.HIGH)
	print("RELE ACTIVADO")
	time. sleep(3)

	GPIO.output(PIN, GPIO.LOW)
	print("RELE DESACTIVADO")
	time. sleep(3)

GPIO.cleanup()

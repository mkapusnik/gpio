#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.OUT)

while True:
    GPIO.output(7, 1)
    time.sleep(1)
    GPIO.output(7, 0)
    time.sleep(1)	

GPIO.cleanup()
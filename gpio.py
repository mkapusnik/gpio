#!/usr/bin/python
import RPi.GPIO as GPIO
import time
#import logging

#logging.basicConfig(format='%(levelname)s-%(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG,filename='/App/gpio.log')

GPIO.setmode(GPIO.BCM)
GPIO.setup(11, GPIO.OUT)

while True:
	GPIO.output(11, 1)
  time.sleep(1)
	GPIO.output(11, 0)
  time.sleep(1)	

GPIO.cleanup()
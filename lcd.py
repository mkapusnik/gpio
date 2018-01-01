import easyi2c
import RPi.GPIO as GPIO
import time

dev = easyi2c.IIC(0x3c, 1)
dev.i2c([31, 1], 0)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21, GPIO.IN)

counter = 0

def handleKey(argument):
  global counter
  count = dev.i2c([2],1)
  counter += count[0]

  if counter % 16 == 0:
    dev.i2c([31, 0xc0], 0)
  if counter % 32 == 0:
    dev.i2c([31, 1], 0)

  keys = dev.i2c([3], count[0])
  dev.i2c([32] + [64+key for key in keys] + [0], 0)

try:
  dev.i2c([1],0)
  GPIO.add_event_detect(21, GPIO.FALLING, callback=handleKey)
  raw_input("Press Enter to continue...")
finally:
  dev.i2c([31, 1], 0)
  dev.close()
  GPIO.remove_event_detect(21)
  GPIO.cleanup()

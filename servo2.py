import RPi.GPIO as GPIO
from gpiozero import AngularServo
from time import sleep
import sys
import os
import termios
import fcntl

servoPin = 18
ledPin = 17
min = -90
max = 70

def getch():
  fd = sys.stdin.fileno()

  oldterm = termios.tcgetattr(fd)
  newattr = termios.tcgetattr(fd)
  newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
  termios.tcsetattr(fd, termios.TCSANOW, newattr)

  oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
  fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

  try:
    while 1:
      try:
        c = sys.stdin.read(1)
        break
      except IOError: pass
  finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
  return c

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(ledPin, True)

servo = AngularServo(servoPin, min_pulse_width=0.00045, max_pulse_width=0.00245, frame_width=0.02)

for arg in sys.argv[1:]:
  try:
    servo.angle = int(arg)
  except (ValueError, RuntimeError):
    print "Not a valid angle"

if len(sys.argv) <= 1:
  current = 0
  servo.angle = current
  print "Interactive mode"
  while True:
    key = ord(getch())
    if key == 113: #(q)uit
      break
    elif key == 27:
      key = ord(getch())
      if key == 91:
        key = ord(getch())
        if key == 67:
          current += 10
        elif key == 68:
          current -= 10
    if current > max:
      current = max
    elif current < min:
      current = min
    servo.angle = int(current)

GPIO.output(ledPin, False)

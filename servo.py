import RPi.GPIO as GPIO
from time import sleep
import sys
import os
import termios
import fcntl

servoPin = 12
ledPin = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(servoPin, GPIO.OUT)
GPIO.setup(ledPin, GPIO.OUT)
pwm=GPIO.PWM(servoPin, 60)
pwm.start(0)

def SetAngle(angle):
  GPIO.output(ledPin, True)
  duty = angle / 18 + 2.5
  GPIO.output(servoPin, True)
  pwm.ChangeDutyCycle(duty)
  sleep(1)
  GPIO.output(servoPin, False)
  pwm.ChangeDutyCycle(0)
  GPIO.output(ledPin, False)

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

for arg in sys.argv[1:]:
  try:
    SetAngle(int(arg))
  except (ValueError, RuntimeError):
    print "Not a valid angle"

if len(sys.argv) <= 1:
  current = 90
  SetAngle(current)
  print "Interactive mode"
  GPIO.output(servoPin, True)
  while True:
    key = ord(getch())
    if key == 113: #(q)uit
      break
    elif key == 27:
      key = ord(getch())
      if key == 91:
        key = ord(getch())
        if key == 68:
          current += 10
        elif key == 67:
          current -= 10
    SetAngle(current)

GPIO.output(servoPin, False)
GPIO.output(ledPin, False)
pwm.stop()
GPIO.cleanup()

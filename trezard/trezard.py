#!/usr/bin/env python
import RPi.GPIO as GPIO
import socket
import sys
from time import sleep
from daemonize import Daemonize

ledPin = 17
pid = "/tmp/trezard.pid"

def main():
  try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.output(ledPin, False)
    while True:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      GPIO.output(ledPin, sock.connect_ex(('127.0.0.1', 17298)) == 0)
      sleep(5)
  finally:
    print "asdas"
    GPIO.cleanup()


if len(sys.argv) == 1:
  main()
elif sys.argv[1] == 'start':
  daemon = Daemonize(app="trezard", pid=pid, action=main)
  daemon.start()
#elif sys.argv[1] == 'stop':
#  daemon = Daemonize(app="trezard", pid=pid, action=main)
#  daemon.exit()

#!/usr/bin/env python
import RPi.GPIO as GPIO
import socket
import sys
import smtplib
import ConfigParser
import traceback
from time import sleep
from daemonize import Daemonize

ledPin = 21
pid = "/tmp/trezard.pid"

configParser = ConfigParser.ConfigParser()
configParser.readfp(open(r'/etc/trezard.conf'))

username = configParser.get('mail', 'username')
password = configParser.get('mail', 'password')
address = configParser.get('mail', 'address')

def sendmail():
  try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.ehlo()
    server.login(username, password)
    server.sendmail('tzc@raspberry.pi', address, 'Subject: Wallet Crashed\nSorry ...')
    server.quit()
  except Exception:
    print(traceback.format_exc())
    

def main():
  try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.output(ledPin, False)
    prev_status = True
    while True:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      status = sock.connect_ex(('127.0.0.1', 17298)) == 0
      GPIO.output(ledPin, status)
      if prev_status and not status:
        sendmail()
      prev_status = status
      sleep(1)
  finally:
    GPIO.cleanup()


if len(sys.argv) == 1:
  main()
elif sys.argv[1] == 'start':
  daemon = Daemonize(app="trezard", pid=pid, action=main)
  daemon.start()
#elif sys.argv[1] == 'stop':
#  daemon = Daemonize(app="trezard", pid=pid, action=main)
#  daemon.exit()

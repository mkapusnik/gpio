#!/usr/bin/env python
import RPi.GPIO as GPIO
import socket
import sys
import smtplib
import ConfigParser
import traceback
import easyi2c
from time import sleep
from daemonize import Daemonize
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

ledPin = 4
pid = "/tmp/trezard.pid"

configParser = ConfigParser.ConfigParser()
configParser.readfp(open(r'/etc/trezard.conf'))

username = configParser.get('mail', 'username')
password = configParser.get('mail', 'password')
address = configParser.get('mail', 'address')

rpcuser = configParser.get('rpc', 'username')
rpcpass = configParser.get('rpc', 'password')

dev = easyi2c.IIC(0x3c, 1)

def sendmail(message):
  try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.ehlo()
    server.login(username, password)
    server.sendmail('tzc@raspberry.pi', address, 'Subject: TZC Wallet\n'+message)
    server.quit()
  except Exception:
    print(traceback.format_exc())

def lcd(message):
  try:
    dev.i2c([31, 1], 0)
    dev.i2c([33] + [ord(x) for x in message] + [0], 0)
  except Exception:
    print(traceback.format_exc())    

def main():
  try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.output(ledPin, False)
    prev_status = False
    while True:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      status = sock.connect_ex(('127.0.0.1', 17298)) == 0
      GPIO.output(ledPin, status)
      if prev_status and not status:
        sendmail('Crashed')
        lcd('Wallet Crashed')
      if not prev_status and status:
        sendmail('Started')
        lcd('Wallet Started')
      if status:
        print "Get balance"
        try:
          rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:17299"%(rpcuser, rpcpass))
          #rpc_connection.getinfo()
          balance = 0
          lcd("Balance: $balance")
        except:
          pass

      prev_status = status
      sleep(1)
  finally:
    lcd('Shutting Down')
    dev.close()
    GPIO.cleanup()

if len(sys.argv) == 1:
  main()
elif sys.argv[1] == 'start':
  daemon = Daemonize(app="trezard", pid=pid, action=main)
  daemon.start()
#elif sys.argv[1] == 'stop':
#  daemon = Daemonize(app="trezard", pid=pid, action=main)
#  daemon.exit()
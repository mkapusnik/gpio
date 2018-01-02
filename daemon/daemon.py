import RPi.GPIO as GPIO
from time import sleep
from daemonize import Daemonize

pid = "/tmp/api.pid"

def moveUp(arg):
  print "Move UP"

def moveDown(arg):
  print "Move DOWN"

def main():
  try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(26, GPIO.FALLING, callback=moveDown)
    GPIO.add_event_detect(21, GPIO.FALLING, callback=moveUp)
    while True:
      sleep(5)
#    raw_input("Initialized, service running ...")
  finally:
    GPIO.remove_event_detect(26)
    GPIO.remove_event_detect(21)
    GPIO.cleanup()

daemon = Daemonize(app="api_app", pid=pid, action=main)
daemon.start()

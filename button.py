import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#GPIO.setup(20, GPIO.IN)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def moveUp(arg):
  print "Move up"

def moveDown(arg):
  print "Move down"

try:
#  GPIO.add_event_detect(20, GPIO.FALLING, callback=moveUp)
  GPIO.add_event_detect(21, GPIO.FALLING, callback=moveDown)
  raw_input("Press Enter to continue...")
finally:
#  GPIO.remove_event_detect(20)
  GPIO.remove_event_detect(21)
  GPIO.cleanup()


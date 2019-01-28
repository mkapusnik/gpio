from gpiozero import AngularServo
from time import sleep

s = AngularServo(18, min_pulse_width=0.00045, max_pulse_width=0.00245, frame_width=0.02, min_angle=-90, max_angle=90)

for x in range(-9, 9):
  s.angle = x * 10
  sleep(1)

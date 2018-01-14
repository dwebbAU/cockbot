from __future__ import division
import time
import sys
import RPi.GPIO as GPIO
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=2)

# Configure min and max servo pulse lengths
servo_closed = 600  # Min pulse length out of 4096
servo_open = 160  # Max pulse length out of 4096

#Ingredients
vodka = 0
kahlua = 3
milk = 2
water = 4
air = 5
Enable = 19
Motor = 26
shot = 5

mode=GPIO.getmode()

GPIO.cleanup()

sleeptime=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(Motor, GPIO.OUT)
GPIO.setup(Enable, GPIO.OUT)
GPIO.output(Enable, GPIO.LOW)
GPIO.output(Motor, GPIO.LOW)

def run_motor(x):
    GPIO.output(Enable, GPIO.HIGH)
    GPIO.output(Motor, GPIO.LOW)
    time.sleep(x)
    GPIO.output(Motor, GPIO.HIGH)
    GPIO.output(Enable, GPIO.LOW)


# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

def close_servo(servo):
  print('closing ' + str(servo))
  pwm.set_pwm(servo,0, servo_closed)
  time.sleep(0.1)

def open_servo(servo):
  print('open ' + str(servo))
  pwm.set_pwm(servo,0, servo_open)
  time.sleep(0.1)



# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(50)

try:
  close_servo(vodka)
  close_servo(milk)
  close_servo(kahlua)
  close_servo(water)
  close_servo(air)
  print('opening ' + str(sys.argv[1]))
  open_servo(int(sys.argv[1]))
  run_motor(100)

except KeyboardInterrupt:
  
  GPIO.output(Enable, GPIO.LOW)
  close_servo(sys.argv[1])
  print('closing')
  GPIO.cleanup()

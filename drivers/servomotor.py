import RPi.GPIO as GPIO
from time import sleep

class ServoMotor:
    def __init__(self, config):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self._pin = config['pwmPin']
        self._min = 0
        self._max = 180

        GPIO.setup(self._pin, GPIO.OUT)
        self._pwmPin = GPIO.PWM(self._pin, 50)
        self._pwmPin.start(0)
    
    def clean(self):
        self._pwmPin.stop()

    def rotate(self, angle):
        angle = 180 - angle
        if angle >= self._min and angle <= self._max:
            self._setAngle(angle)
            return angle
        elif angle < self._min:
            self._setAngle(self._min)
            return self._min
        elif angle > self._max:
            self._setAngle(self._max)
            return self._max

    def _setAngle(self, angle):
        dutycycle = (angle / 18.0) + 2.5
        self._pwmPin.ChangeDutyCycle(dutycycle)

    def rotate2Min(self):
        self.rotate(self._min)

    def rotate2Max(self):
        self.rotate(self._min)

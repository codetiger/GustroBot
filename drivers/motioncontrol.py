import RPi.GPIO as GPIO
from time import sleep
import math

from .multisteppercontrol import MultiStepperControl

class MotionControl:
    _rotationsPerDegree = 1.0 / 180.0
    _rotationsPerMeter = (100.0 - 4.5) / (2 * math.pi * 5.0) # 100cm / circumference of wheel with diameter 10cm and 4cm is calibration correction.
    
    def __init__(self, config):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self._motorControl = MultiStepperControl(config['enablePin'], config['stepType'])
        self._motorControl.addStepperMotor("wheelLeft", config['wheelLeft'])
        self._motorControl.addStepperMotor("wheelRight", config['wheelRight'])

    def rotate(self, angle):
        if angle > 180:
            angle = angle - 360
        elif angle < -180:
            angle = angle + 360
            
        directions = {'wheelLeft':False, 'wheelRight':False}
        if angle < 0:
            angle = -angle
            directions = {'wheelLeft':True, 'wheelRight':True}
        
        self._motorControl.rotate(angle * self._rotationsPerDegree, directions)
        
    def setSpeed(self, speed:float):
        self._motorControl.setSpeed(speed)
        
    def move(self, distance:float):
        directions = {'wheelLeft':False, 'wheelRight':True}
        if distance < 0:
            distance = -distance
            directions = {'wheelLeft':True, 'wheelRight':False}

        self._motorControl.rotate(distance * self._rotationsPerMeter, directions)
        
    def cleanup(self):
        self._motorControl.cleanup()

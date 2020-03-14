import RPi.GPIO as GPIO
from time import sleep
from multistepper import MultiStepperController

class MotionController:
    _rotationsPerDegree = 1.0 / 180.0
    _rotationsPerMeter = 5.0
    
    def __init__(self, config):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self._motorControl = MultiStepperController(config['enablePin'], config['stepType'])
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

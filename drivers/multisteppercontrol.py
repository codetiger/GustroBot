import RPi.GPIO as GPIO
from time import sleep

class MultiStepperControl:
    _microsteps =  { 'Full'  :   1.0,
                    'Half'  :   2.0,
                    '1/4'   :   4.0,
                    '1/8'   :   8.0,
                    '1/16'  :   16.0,
                    '1/32'  :   32.0}

    def __init__(self, enablePin, stepType):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        self._enablePin = enablePin
        GPIO.setup(self._enablePin, GPIO.OUT)
        self._stepperMotors = {}
        self._stepType = stepType
        self.setSpeed(1.0)
 
    def setSpeed(self, speed:float):
        self._speed = speed
        self._delay = .005 / (self._microsteps[self._stepType] * self._speed)
        
    def addStepperMotor(self, name, config):
        motor = {'stepPin':config['stepPin'], 'dirPin': config['dirPin']}
        self._stepperMotors[name] = motor
        GPIO.setup(config['stepPin'], GPIO.OUT)
        GPIO.setup(config['dirPin'], GPIO.OUT)

    def rotate(self, noOfRots:float, motorDirections):
        GPIO.output(self._enablePin, False)

        for name, clockwise in motorDirections.items():
            GPIO.output(self._stepperMotors[name]['dirPin'], clockwise)

        stepPins = []
        for name in motorDirections.keys():
            stepPins.append(self._stepperMotors[name]['stepPin'])

        steps = noOfRots * 200.0 * self._microsteps[self._stepType]
        for i in range(int(steps)):
            GPIO.output(stepPins, GPIO.HIGH)
            sleep(self._delay)
            GPIO.output(stepPins, GPIO.LOW)
            sleep(self._delay)

        GPIO.output(self._enablePin, True)

    def cleanup(self):
        GPIO.cleanup()

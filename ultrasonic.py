import RPi.GPIO as GPIO
import time

class UltrsonicSensor:
    def __init__(self, config):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self._triggerPin = config['triggerPin']
        self._echoPin = config['echoPin']

        GPIO.setup(self._triggerPin, GPIO.OUT)
        GPIO.setup(self._echoPin, GPIO.IN)
    
    def clean(self):
        pass

    def getDistance(self):
        # Triggering
        GPIO.output(self._triggerPin, False)
        time.sleep(0.01)
        GPIO.output(self._triggerPin, True)
        time.sleep(0.00001)
        GPIO.output(self._triggerPin, False)

        # Reading values from echopin
        startTime = time.time() 
        while GPIO.input(self._echoPin) == 0:
            startTime = time.time()
    
        stopTime = time.time()
        while GPIO.input(self._echoPin) == 1:
            stopTime = time.time()
    
        # time difference between start and arrival
        timeElapsed = stopTime - startTime

        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (timeElapsed * 34300.0) / 2
        distance = round(distance, 2)                    

        if distance > 2 and distance < 400:
            distance = distance
        else:
            distance = 0
        return distance

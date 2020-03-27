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

    def getAverageDistance(self, count):
        avgDist = 0
        for i in range(count):
            dist = self.getDistance()
            avgDist += dist
        return avgDist / count
            
    def getDistance(self):
        GPIO.output(self._triggerPin, True)
        time.sleep(0.00001)
        GPIO.output(self._triggerPin, False)

        startTime = time.time() 
        while GPIO.input(self._echoPin) == 0:
            startTime = time.time()
    
        stopTime = time.time()
        while GPIO.input(self._echoPin) == 1:
            stopTime = time.time()
    
        timeElapsed = stopTime - startTime
        distance = (timeElapsed * 34300.0) / 2
        distance = round(distance, 2)

        if distance > 2 and distance < 400:
            distance = distance
        else:
            distance = 0
        return distance

import RPi.GPIO as GPIO
import time
import statistics

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

    def getMedianDistance(self, count):
        avgDist = 0
        distances = [0] * count
        for i in range(count):
            distances[i] = 0
            while distances[i] > 400 or distances[i] < 2:
                distances[i] = self.getDistance()
        
        return statistics.median(distances)
            
    def getDistance(self):
        time.sleep(0.01) # Very important to reduce noise
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

        return distance

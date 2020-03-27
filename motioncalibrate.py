import time
import sys
import json

from servo import ServoMotor
from ultrasonic import UltrsonicSensor
from motioncontrol import MotionControl
from motionsensor import MotionSensor

config = {}
with open('config.json') as f:
    config = json.load(f)

ultrasonicSensorFront = UltrsonicSensor(config["FrontUltrsonicSensor"])
motionControl = MotionControl(config['MultiStepperController'])
servo = ServoMotor(config['HeadMountServo'])
servo.rotate(0)
motionSensor = MotionSensor()

def calibrateMovement(dist:float):
    startAvg = 0
    for i in range(10):
        distance = ultrasonicSensorFront.getDistance()
        time.sleep(0.1)
        startAvg += distance
    startAvg /= 10

    motionControl.move(dist)

    time.sleep(1)
    endAvg = 0
    for i in range(10):
        distance = ultrasonicSensorFront.getDistance()
        time.sleep(0.1)
        endAvg += distance
    endAvg /= 10
    print("Travel: ", startAvg - endAvg)
    
def calibrateRotation(angle:float):
    startAvg = 0
    for i in range(10):
        heading = motionSensor.getHeadingAngle()
        time.sleep(0.1)
        startAvg += heading
    startAvg /= 10

    motionControl.rotate(angle)

    time.sleep(1)
    endAvg = 0
    for i in range(10):
        heading = motionSensor.getHeadingAngle()
        time.sleep(0.1)
        endAvg += heading
    endAvg /= 10
    print("Rotation: ", startAvg - endAvg)
    
if __name__ == "__main__":
    time.sleep(1)
    calibrateRotation(10)

    servo.clean()
    ultrasonicSensorFront.clean()
    motionControl.cleanup()


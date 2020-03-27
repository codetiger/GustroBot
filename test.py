import time
import sys
import json
import math
import numpy as np
import matplotlib.pyplot as plt

from drivers.servomotor import ServoMotor
from drivers.ultrsonicsensor import UltrsonicSensor
from drivers.motionsensor import MotionSensor
from drivers.motioncontrol import MotionControl

from mapping.gridmap import GridMap

if __name__ == "__main__":
    config = {}
    with open('config.json') as f:
        config = json.load(f)

    ultrasonicSensorFront = UltrsonicSensor(config["FrontUltrsonicSensor"])
    ultrasonicSensorBack = UltrsonicSensor(config["BackUltrsonicSensor"])
    motionControl = MotionControl(config['MultiStepperController'])
    servo = ServoMotor(config['HeadMountServo'])
    motionSensor = MotionSensor()
    
    gridMap = GridMap()
    servo.rotate(0)
    time.sleep(2.0)
    
    position = [0, 0]

    def scanSurroundings(robotAngle):
        for angle in range(0, 180, 1):
            servo.rotate(angle)

            distance = ultrasonicSensorFront.getAverageDistance(2)
            theta = ((angle  + 90)) * math.pi / 180.0
            gridMap.addPoint(position, theta, distance)

            distance = ultrasonicSensorBack.getAverageDistance(2)
            theta = ((angle  + 270)) * math.pi / 180.0
            gridMap.addPoint(position, theta, distance)
            
    def moveStraight(distance:float):
        while distance > 0:
            motionControl.move(0.1)
            distance -= 0.1
            servo.rotate(0)
            visionDistance = ultrasonicSensorFront.getDistance()
            if visionDistance < 20:
                distance = 0

    headingAngle = motionSensor.getHeadingAngle()
    # print("Compass Angle: ", headingAngle)
    scanSurroundings(headingAngle)
    # motionControl.rotate(90)
    
    gridMap.recalculate()
    gridMap.saveImage("map.png")
    
    servo.clean()
    ultrasonicSensorFront.clean()
    ultrasonicSensorBack.clean()
    motionControl.cleanup()
    motionSensor.clean()


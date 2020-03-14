import time
import sys
import json
import math

from servo import ServoMotor
from ultrasonic import UltrsonicSensor
from MPU9250 import MPU9250

if __name__ == "__main__":
    config = {}
    with open('config.json') as f:
        config = json.load(f)

    try:
        mpu9250 = MPU9250()
        # while True:
        mag = mpu9250.readMagnet()
        heading = math.atan2(mag['y'], mag['x']) * 180.0 / math.pi;
        print("Compass Angle: ", heading)
        time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    except:
        pass

    ultrasonicSensorFront = UltrsonicSensor(config["FrontUltrsonicSensor"])
    ultrasonicSensorBack = UltrsonicSensor(config["BackUltrsonicSensor"])
    servo = ServoMotor(config['HeadMountServo'])
    servo.rotate(0)
    time.sleep(1)
    
    for angle in range(0, 181, 5):
        print("Set Head Angle: ", angle)
        servo.rotate(angle)
        
        distance = ultrasonicSensorFront.getDistance()
        print ("Measured Distance = %.1f cm in Front" % (distance))
        distance = ultrasonicSensorBack.getDistance()
        print ("Measured Distance = %.1f cm in Back" % (distance))

        time.sleep(0.1)

    servo.clean()
    ultrasonicSensorFront.clean()
    ultrasonicSensorBack.clean()


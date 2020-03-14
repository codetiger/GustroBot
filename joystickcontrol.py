from inputs import get_gamepad
import time
import sys
import json

from motioncontrol import MotionController
from MPU9250 import MPU9250
from servo import ServoMotor
from ultrasonic import UltrsonicSensor

if __name__ == "__main__":
    config = {}
    with open('config.json') as f:
        config = json.load(f)

    motionController = MotionController(config['MultiStepperController'])
    # mpu9250 = MPU9250()
    ultrasonicSensorFront = UltrsonicSensor(config["FrontUltrsonicSensor"])
    ultrasonicSensorBack = UltrsonicSensor(config["BackUltrsonicSensor"])
    servo = ServoMotor(config['HeadMountServo'])
    servoAngle = 90
    servo.rotate(servoAngle)
    
    try:
        while 1:
            events = get_gamepad()
            for event in events:
                # print(event.ev_type, event.code, event.state)
                if event.ev_type == 'Key' and event.code == 'BTN_NORTH' and event.state == 0:
                    print('Moving forward')
                    motionController.move(0.1)
                elif event.ev_type == 'Key' and event.code == 'BTN_EAST' and event.state == 0:
                    print('Moving backward')
                    motionController.move(-0.1)
                elif event.ev_type == 'Key' and event.code == 'BTN_Z' and event.state == 0:
                    print('Rotating')
                    motionController.rotate(10)
                elif event.ev_type == 'Key' and event.code == 'BTN_WEST' and event.state == 0:
                    print('Rotating')
                    motionController.rotate(-10)
                # elif event.ev_type == 'Key' and event.code == 'BTN_WEST1' and event.state == 0:
                #     accel = mpu9250.readAccel()
                #     print("ax=\t", accel['x'], "\tay=\t", accel['y'], "\taz=\t", accel['z'])
                # elif event.ev_type == 'Key' and event.code == 'BTN_WEST2' and event.state == 0:
                #     gyro = mpu9250.readGyro()
                #     print("gx=\t", gyro['x'], "\tgy=\t", gyro['y'], "\tgz=\t", gyro['z'])
                # elif event.ev_type == 'Key' and event.code == 'BTN_WEST3' and event.state == 0:
                #     mag = mpu9250.readMagnet()
                #     print("mx=\t", mag['x'], "\tmy=\t", mag['y'], "\tmz=\t", mag['z'])
                elif event.ev_type == 'Key' and event.code == 'BTN_TL' and event.state == 0:
                    servoAngle += 10
                    servoAngle = servo.rotate(servoAngle)
                    print("Servo Motor Angle:", servoAngle)
                elif event.ev_type == 'Key' and event.code == 'BTN_TR' and event.state == 0:
                    servoAngle -= 10
                    servoAngle = servo.rotate(servoAngle)
                    print("Servo Motor Angle:", servoAngle)
                elif event.ev_type == 'Key' and event.code == 'BTN_WEST6' and event.state == 0:
                    distance = ultrasonicSensorFront.getDistance()
                    print ("Measured Distance = %.1f cm in Front" % (distance))
                elif event.ev_type == 'Key' and event.code == 'BTN_WEST7' and event.state == 0:
                    distance = ultrasonicSensorBack.getDistance()
                    print ("Measured Distance = %.1f cm in Back" % (distance))
    except KeyboardInterrupt:
        motionController.cleanup()
        servo.clean()
        ultrasonicSensorFront.clean()
        ultrasonicSensorBack.clean()


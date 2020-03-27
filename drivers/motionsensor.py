import RPi.GPIO as GPIO
from time import sleep
import math
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

class MotionSensor:
    def __init__(self):
        self._mpu = MPU9250(
            address_ak=AK8963_ADDRESS, 
            address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
            address_mpu_slave=None, 
            bus=1, 
            gfs=GFS_1000, 
            afs=AFS_8G, 
            mfs=AK8963_BIT_16, 
            mode=AK8963_MODE_C8HZ)

        self._mpu.configure()

        self._mpu.abias = [-0.14861613948170732, 0.04269483612804878, 0.0027867759146340543]
        self._mpu.gbias = [-1.9508920064786586, -0.5945345250571646, -0.7832224776105182]
        self._mpu.magbias = [0.7719651240778002, 0.826867816091954, 2.0192982456140354]
        self._mpu.mbias = [42.44004407051282, 19.4276365995116, -94.42522512210013]
 
    def clean(self):
        pass
    
    def getCalibration(self):
        self._abias = self._mpu.abias
        self._gbias = self._mpu.gbias
        self._magScale = self._mpu.magScale
        self._mbias = self._mpu.mbias
        
        print("abias", self._abias)
        print("gbias", self._gbias)
        print("magbias", self._magScale)
        print("mbias", self._mbias)

    def calibrate(self):
        self._mpu.calibrate()
        self._mpu.configure()
        
    def getHeadingAngle(self):
        data = self._mpu.readMagnetometerMaster()
        return 180 + math.atan2(data[1], data[0]) * 180.0 / math.pi;
        
if __name__ == "__main__":
    motionSensor = MotionSensor("")
    
    while True:
        print("Heading Angle: ", motionSensor.getHeadingAngle())
        sleep(1)
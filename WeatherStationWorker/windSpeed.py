from gpiozero import Button
import time
import math
import statistics

CM_IN_KM = 100000.0
SECS_IN_HOUR = 3600
ADJUSTMENT = 1.18 # Calibration factor for anemometor -- may need to change

StoreSpeeds = []

WindCount = 0
CM_Radius = 9.0
WindInterval = 5

def Spin():
    global WindCount
    WindCount = WindCount + 1

def CalculateSpeed(TimeSeconds):
    global WindCount
    CM_Circumference = (2 * math.pi) * CM_Radius
    Rotations = WindCount / 2.0

    KM_Distance = (CM_Circumference * Rotations) / CM_IN_KM

    KM_PerSecond = KM_Distance / TimeSeconds
    KM_PerHour = KM_PerSecond * SECS_IN_HOUR

    return KM_PerHour * ADJUSTMENT

def WindReset():
    global WindCount
    WindCount = 0


WindSpeedSensor = Button(5)
WindSpeedSensor.when_pressed = Spin

while True:
    StartTime = time.time()
    while time.time() - StartTime <= WindInterval:
        WindReset()
        time.sleep(WindInterval)
        FinalSpeed = CalculateSpeed(WindInterval)
        StoreSpeeds.append(FinalSpeed)

    WindGust = max(StoreSpeeds)
    WindSpeed = statistics.mean(StoreSpeeds)
    print(WindSpeed, WindGust) 
    # TODO: Write values to database
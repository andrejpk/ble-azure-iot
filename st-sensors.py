import sys 
import time
import binascii
from bluepy import btle

devAddress = sys.argv[1]
print("connecting to {0}...".format(devAddress))

dev = btle.Peripheral(devAddress)

SENSORTAG_UUID_LIGHTSENSOR = "f000aa70-0451-4000-b000-000000000000"
SENSORTAG_UUID_BAROSENSOR =        btle.UUID("f000aa40-0451-4000-b000-000000000000")
SENSORTAG_UUID_BAROSENSOR_CONFIG = btle.UUID("f000aa42-0451-4000-b000-000000000000")
SENSORTAG_UUID_BAROSENSOR_DATA   = btle.UUID("f000aa41-0451-4000-b000-000000000000")

print("Services: ")
for svc in dev.services:
    print(str(svc))


def getLightSensorReader():
    lightSensor = btle.UUID("f000aa70-0451-4000-b000-000000000000")

    lightService = dev.getServiceByUUID(lightSensor)
    for ch in lightService.getCharacteristics():
        print(str(ch))

    uuidConfig = btle.UUID("f000aa72-0451-4000-b000-000000000000")
    lightSensorConfig = lightService.getCharacteristics(uuidConfig)[0]
    # Enable the sensor
    lightSensorConfig.write(b'\x01')

    uuidValue  = btle.UUID("f000aa71-0451-4000-b000-000000000000")
    lightSensorValue = lightService.getCharacteristics(uuidValue)[0]
    # Read the sensor
    
    def reader():
        val = lightSensorValue.read()
        valInt = int.from_bytes(val, byteorder='little', signed=False)
        return valInt

    return reader

def getBaroSensorReader():
    service = dev.getServiceByUUID(SENSORTAG_UUID_BAROSENSOR)
    sensorConfig = service.getCharacteristics(SENSORTAG_UUID_BAROSENSOR_CONFIG)[0]
    sensorConfig.write(b'\x01')  # enable the sensor
    sensorValue = service.getCharacteristics(SENSORTAG_UUID_BAROSENSOR_DATA)[0]
    def reader():
        val = sensorValue.read()
        print('raw baro data:', val)
        return {
                'temp': int.from_bytes(val[0:2], byteorder='little', signed=False),
                'press': int.from_bytes(val[3:5], byteorder='little', signed=False)
                }

    return reader

lightReader = getLightSensorReader()
baroReader = getBaroSensorReader()

while True:
    val = lightReader()
    print("Light sensor value: {0}".format(val))
    valBaro = baroReader()
    print("Baro: Temp: {0}".format(valBaro))
    time.sleep(0.5)

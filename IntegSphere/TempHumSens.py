#Interface to the AHT20 temperature and humidity sensor used for environment monitoring

# ----------------------------------------------------------------------------------------------#

import board
import adafruit_ahtx0

# ----------------------------------------------------------------------------------------------#

class TempHumSensor():
    i2c = None
    sensor = None

    # ----------------------------------------------------------------------------------------------#

    def __init__(self):
        self.i2c = board.I2C()
        self.sensor = adafruit_ahtx0.AHTx0(self.i2c)
        self.sensor.reset()
        self.sensor.calibrate()
        

    # ----------------------------------------------------------------------------------------------#

    def hum(self, prnt=False):
        val = self.sensor.relative_humidity
        if prnt:
            print("Current relative humidity: {:.2f}%".format(val))
        return val
    
    # ----------------------------------------------------------------------------------------------#

    def temp(self, prnt=False):
        val = self.sensor.temperature
        if prnt:
            print("Current temperature [C]: {:.2f}".format(val))
        return val

    # ----------------------------------------------------------------------------------------------#

    def tempHum(self):
        return self.sensor.temperature, self.sensor.relative_humidity

    # ----------------------------------------------------------------------------------------------#
    
# ----------------------------------------------------------------------------------------------#

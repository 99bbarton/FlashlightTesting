#Interface to the TSL2591 lux sensor mounted in the integrating sphere

# ----------------------------------------------------------------------------------------------#

import board
import adafruit_tsl2591

# ----------------------------------------------------------------------------------------------#

class LuxSensor():
    i2c = None
    sensor = None
    gain = None

    # ----------------------------------------------------------------------------------------------#

    def __init__(self, gain="LOW"):
        try:
            self.i2c = board.I2C()
        except:
            print("ERROR: I2C communication not operational!")
            exit(1)
        try:
            self.sensor = adafruit_tsl2591.TSL2591(self.i2c)
        except:
            print("ERROR: Could not establish connection with TSL2591 lux sensor!")
            exit(2)
        self.setGain(gain)

    # ----------------------------------------------------------------------------------------------#

    def read(self, whichSens=""):
        if whichSens == "" or whichSENS.UPPER() == "BOTH":
            return self.sensor.lux
        elif whichSens.upper() == "IR":
            return self.sensor.infrared
        elif whichSens.upper() == "VIS":
            return self.sensor.visible
        elif whichSens.upper() == "RAW":
            return self.sensor.raw_luminosity
        else:
            print("WARNING: Unrecognized sensor specified to LuxSensor::read()!")
            return 0

    # ----------------------------------------------------------------------------------------------#

    def getGain(self):
        if self.sensor.gain == adafruit_tsl2591.GAIN_LOW:
            return "LOW"
        elif self.sensor.gain == adafruit_tsl2591.GAIN_MED:
            return "MED"
        elif self.sensor.gain == adafruit_tsl2591.GAIN_HIGH:
            return "HIGH"
        elif self.sensor.gain == adafruit_tsl2591.GAIN_MAX:
            return "MAX"
        
    # ----------------------------------------------------------------------------------------------#

    def setGain(self, level):
        if level.upper() == "LOW" or level.upper() == "MIN":
            self.sensor.gain = adafruit_tsl2591.GAIN_LOW
        elif level.upper() == "MED":
            self.sensor.gain = adafruit_tsl2591.GAIN_MED
        elif level.upper() == "HIGH":
            self.sensor.gain = adafruit_tsl2591.GAIN_HIGH
        elif level.upper() == "MAX":
            self.sensor.gain = adafruit_tsl2591.GAIN_MAX
        else:
            print("WARNING: Unrecognized level passed to LuxSensor::setGain()! Will default to LOW")
            self.sensor.gain = afruit_tsl2591.GAIN_LOW


# ----------------------------------------------------------------------------------------------#

#TODO Add interface to control interrupts and thresholds
# enable/disable, measure fraction at each gain, etc

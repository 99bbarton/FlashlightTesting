# Tool to perform measurements with the integrating sphere

#TODO's and Possible improvements:
# - lux to lumen conversion
# - CCT correction, cd/lum correction. add arguments to toggle and receive info
# - dynamic sampling rate for turbo measurements
# - 

# ----------------------------------------------------------------------------------------------#

import argparse
import sys
import os
import time
from datetime import datetime

import LuxSensor as ls
import TempHumSens as ths 

# ----------------------------------------------------------------------------------------------#

def parseArgs():
    argparser = argparse.ArgumentParser(description="Perform measurements using the lux sensor in the integrating sphere")
    argparser.add_argument("-r", "--runtime", action="store_true", help="If specified, perform a runtime test")
    argparser.add_argument("-n", "--now", action="store_true", help="If specified, reads the current value")
    argparser.add_argument("-i", "--interval", type=float, default=1, help="For runtime tests, the interval in between measurements in seconds.")
    argparser.add_argument("-d", "--duration", type=int, help="For runtime test, a maximum duration in seconds.")
    argparser.add_argument("-o", "--outFile", type=str, help="A path and name for the output file.")
    argparser.add_argument("-l", "--lumens", action="store_true", help="If specied, output values will be converted to lumens.")
    argparser.add_argument("-g", "--gain", choices=["LOW", "MED", "HIGH", "MAX"], default="LOW", help="A gain level to set the sensor to.")
    argparser.add_argument("-a", "--absTime", action="store_true", help="For runtime tests, will use absolute time difference rather than nominal i.e. in steps of --interval")
    argparser.add_argument("--tempHum", action="store_true", help="If specified, will print the current temp and rel humidity.")
    args = argparser.parse_args()

    return args

# ----------------------------------------------------------------------------------------------#

def main(args):

    if args.tempHum:
        thSens = ths.TempHumSensor()
        thSens.temp(prnt=True)
        thSens.hum(prnt=True)
    
    if args.now:
        now(args)
    elif args.runtime:
        if args.outFile:
            runtimeTest(args)
        else:
            print("\n\nBeginning live runtime test")
            if not args.duration:
                print("No duration specified, use CTRL-C to end test when desired")
            tElapsed = 0
            while(True):
                now(args)
                time.sleep(args.interval)
                tElapsed += args.interval
                if args.duration:
                    if tElapsed >= args.duration:
                        break
            print("Runtime test complete\n")
            
# ----------------------------------------------------------------------------------------------#

def now(args):
    sens = ls.LuxSensor(gain=args.gain)
    luxVal = sens.read()

    if args.lumens:
        lumVal = luxToLumen(lux, args)
        print("Current lumen reading:", lumVal)
    else:
        print("Current lux reading:", luxVal)
        
# ----------------------------------------------------------------------------------------------#

def runtimeTest(args):
    sens = ls.LuxSensor(gain=args.gain)
    thSens = ths.TempHumSensor()
    
    with open(args.outFile, "w+") as outFile:
        
        if args.duration:
            nSteps = args.duration // args.interval

            wait = input("\nHit ENTER to begin runtime test: ")
            
            startTime = datetime.now()
            outFile.write("Start time: " + str(startTime).split(".")[0] + "\n")
            outFile.write("Air temp [C]: {:.1f}\n".format(thSens.temp()))
            outFile.write("Relative humidity: {:.1f}%\n".format(thSens.hum()))
            if args.lumens:
                outFile.write("time[s],lumens\n")
            else:
                outFile.write("time[s],lux\n")
            for step in range(nSteps):
                if args.absTime:
                    t = datetime.now() - startTime
                else:
                    t = step * args.interval

                val = sens.read()
                if args.lumens:
                    val = luxToLumen(val, args)

                outFile.write(str(t) + "," + "{:.4f}\n".format(val))    
                time.sleep(args.interval)

    print("Done runtime test. Outfile is ", args.outFile)
            
# ----------------------------------------------------------------------------------------------#

#TODO
def luxToLumen(lux, args):
    pass

# ----------------------------------------------------------------------------------------------#
        
if __name__ == "__main__":
    args = parseArgs()
    main(args)

# ----------------------------------------------------------------------------------------------#

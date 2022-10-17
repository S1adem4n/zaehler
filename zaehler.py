import time
import os
from datetime import datetime
import pandas as pd
import RPi.GPIO as GPIO

myGPIO = 18
last_count = float(os.popen("tail -n 1 %s" % "zaehlerstand.csv").read().split("\t")[0])
impulse = False

GPIO.setmode(GPIO.BOARD)
GPIO.setup(myGPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


try:
    while True:
        if GPIO.input(myGPIO):
            impulse = True
            time.sleep(0.5)
        if impulse:
            last_count = round(last_count+.001, 3)
            with open("zaehlerstand.csv", "a") as file:
                date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                file.write(f"{last_count}\t{date}\n")
            
            impulse = False

except Exception as e:
        print(f"Fehler: {e}")
        GPIO.cleanup()
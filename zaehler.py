import time
import os
from datetime import datetime
import pandas as pd
import RPi.GPIO as GPIO

myGPIO = 18
last_count = float(os.popen("tail -n 1 %s" % "zaehlerstand.csv").read().split("\t")[0])

GPIO.setmode(GPIO.BOARD)
GPIO.setup(myGPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


try:
    while True:
        if GPIO.input(myGPIO) == GPIO.HIGH:
            while GPIO.input(myGPIO) == GPIO.HIGH:
                time.sleep(0.1)
            last_count = round(last_count+.01, 2)
            with open("zaehlerstand.csv", "a") as file:
                date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                file.write(f"{last_count}\t{date}\n")
            time.sleep(5)
            

except Exception as e:
        print(f"Fehler: {e}")
        GPIO.cleanup()
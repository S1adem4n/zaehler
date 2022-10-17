import time
from datetime import datetime
import pandas as pd
import RPi.GPIO as GPIO

myGPIO = 18
count = 0
impulse = False

GPIO.setmode(GPIO.BOARD)
GPIO.setup(myGPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
        while True:
                if GPIO.input(myGPIO):
                        impulse = True
                        time.sleep(0.5)
                if impulse:
                        df = pd.read_csv("zaehlerstand.csv", delimiter="\t", names=["Zählerstand", "Datum"])
                        last_count = df.iloc[-1, 0]

                        to_add = pd.DataFrame({"Zählerstand": round(last_count+0.01, 2), "Datum": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}, index=[len(df)])
                        df = pd.concat([df, to_add])

                        df.to_csv("zaehlerstand.csv", sep="\t", header=False, index=False)
                        impulse = False
except:
        print("fehler")
        GPIO.cleanup()
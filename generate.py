import datetime
import csv
import random

with open("zaehlerstand.csv", "a") as file:
    writer = csv.writer(file, dialect="excel-tab")
    stand = 3.503
    time = datetime.datetime.now()
    count = 0
    while count < 150:
        time += datetime.timedelta(0, 0, 0, 0, random.randint(0, 60), random.randint(0, 12))
        stand += random.randint(1, 10) / 100
        writer.writerow([round(stand, 2), time.strftime("%Y-%m-%dT%H:%M:%S")])
        count += 1
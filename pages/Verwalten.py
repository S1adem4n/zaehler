import csv
import subprocess
import datetime
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Gaszähler: Testen",
    page_icon="📁",
    layout="wide",
)

st.title("Gaszähler")

real_count_input = st.number_input("\"Echten\" Zählerstand eintragen")
if st.button("In Datei eintragen"):
    df = pd.read_csv("zaehlerstand.csv", delimiter="\t", names=["Zählerstand", "Datum"])
    df["Verbrauch"] = round(df["Zählerstand"].diff(), 4)
    df['Datum'] = pd.to_datetime(df['Datum'], format="%Y-%m-%dT%H:%M:%S")

    df.loc[len(df)-1, ["Echter Zählerstand"]] = real_count_input
    st.success("Erfolgreich hinzugefügt!")

reset_count_input = st.number_input("Zählerstand zurücksetzen")
if st.button("Zurücksetzen"):
    with open("zaehlerstand.csv", "w+") as file:
        writer = csv.writer(file, dialect="excel-tab")
        time = datetime.datetime.now()
        writer.writerow([reset_count_input, time.strftime("%Y-%m-%dT%H:%M:%S")])
    subprocess.call(["systemctl", "restart", "zaehler.service"])
    st.success("Zählerstand erfolgreich zurückgesetzt!")

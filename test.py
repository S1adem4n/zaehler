import pandas as pd

df = pd.read_csv("zaehlerstand.csv", delimiter="\t", names=["Zählerstand", "Datum"])
df["Verbrauch"] = round(df["Zählerstand"].diff(), 4)
df['Datum'] = pd.to_datetime(df['Datum'], format="%Y-%m-%dT%H:%M:%S")

df.loc[len(df)-1, ["Echter Zählerstand"]] = 7
print(df)
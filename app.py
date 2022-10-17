import time
from datetime import datetime
import pandas as pd
import plotly.express as px
import streamlit as st
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly


st.set_page_config(
    page_title="Gaszähler",
    page_icon="⛽",
    layout="wide",
)

df = pd.read_csv("zaehlerstand.csv", delimiter="\t", names=["Zählerstand", "Datum"])
df["Verbrauch"] = round(df["Zählerstand"].diff(), 4)
df['Datum'] = pd.to_datetime(df['Datum'], format="%Y-%m-%dT%H:%M:%S")

st.title("Gaszähler")
placeholder = st.empty()
placeholder_prophet = st.empty()
show_prophet = placeholder_prophet.button("Vorhersagen berechnen")

if show_prophet:
    with placeholder_prophet.container():
        df_prophet = pd.read_csv("zaehlerstand.csv", sep="\t", names=["y", "ds"])
        m = Prophet()
        m.fit(df_prophet)

        future = m.make_future_dataframe(periods=365)
        forecast = m.predict(future)

        st.markdown("### Vorhersagen")
        predict_col1, predict_col2 = st.columns(2)
        with predict_col1:
            fig1 = plot_plotly(m, forecast)
            st.write(fig1)
        with predict_col2:
            fig2 = plot_components_plotly(m, forecast)
            st.write(fig2)
        
        export_with_prophet = st.download_button("Daten mit Vorhersagen exportieren", data=forecast.to_csv(sep="\t", index=False).encode("utf-8"), file_name="zaehlerstand.csv", mime="text/csv")

export_button = st.download_button("Daten exportieren", data=df.to_csv(sep="\t", index=False).encode("utf-8"), file_name="zaehlerstand.csv", mime="text/csv")

while True:
    with placeholder.container():
        df = pd.read_csv("zaehlerstand.csv", delimiter="\t", names=["Zählerstand", "Datum"])
        df["Verbrauch"] = round(df["Zählerstand"].diff(), 4)
        df['Datum'] = pd.to_datetime(df['Datum'], format="%Y-%m-%dT%H:%M:%S")
        
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            current_count_metric = st.metric(
                label="Aktueller Zählerstand",
                value=df.iloc[-1, 0]
            )
        with metric_col2:
            current_diff_metric = st.metric(
                label="Aktueller Verbrauch",
                value=df.iloc[-1, 2]
            )
        
        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.markdown("### Zählerstand")
            fig_count = px.line(df, x="Datum", y="Zählerstand")
            fig_count.update_layout(autosize=True)
            fig_count.update_yaxes(automargin="left+right")
            st.write(fig_count)
        with fig_col2:
            st.markdown("### Verbrauch")
            fig_diff = px.line(df, x="Datum", y="Verbrauch")
            fig_diff.update_layout(autosize=True)
            fig_diff.update_yaxes(automargin="left+right+bottom+top")
            st.write(fig_diff)
        
    time.sleep(5)
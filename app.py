import streamlit as st
import pandas as pd
from io import StringIO
import numpy as np
import io
from datetime import datetime
import seaborn as sns

from data_process import process_sensors_data

st.set_page_config(page_title='DATA: Data Analytics Tool for Africa')

st.title("DATA: Data Analytics Tool for Africa")

@st.cache_resource
def read_base_data():
	return pd.read_pickle('sample_hackathon_data.pkl')

@st.cache_data
def process_data(df):
	return process_sensors_data(df)


if 'all_data' not in st.session_state:
    st.session_state['all_data'] = []

uploaded_file = st.file_uploader("Upload new data")

if uploaded_file is not None:
    new_data = pd.read_csv(uploaded_file)
    st.session_state['all_data'].append(new_data)


df = pd.concat(st.session_state['all_data'] + [read_base_data()])

parameter = st.selectbox('Parameter', ['PM 10', 'Humidity', 'Temperature', 'PM 1', 'PM 2.5'], index=0)


df = process_data(df)
	
date = st.date_input(
    "Date",
    datetime.strptime(max(df.day_hour.str.slice(0, 10)), "%Y-%m-%d"),
    format="YYYY-MM-DD",
)

if date is not None and parameter is not None:
	df = df[(df.parameter == parameter) & (df.day_hour.str.slice(0, 10) == str(date))]
	df["hour"] = df.day_hour.str.slice(11,13)
	plot = sns.lineplot(data = df, x = "hour", y = "recorded_and_predicted_value", hue = "location")
	st.pyplot(plot.get_figure())



st.dataframe(data=df)

st.write("Sensor locations")

st.map(df, latitude='latitude',
	longitude='longitude',
	size='recorded_and_predicted_value')

	

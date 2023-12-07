import streamlit as st
import pandas as pd
from io import StringIO
import numpy as np
import io

st.set_page_config(page_title='air')

st.title("Air hack")

@st.cache_resource
def read_data():
	return pd.read_pickle('sensors_dataset.pkl')


if 'all_data' not in st.session_state:
    st.session_state['all_data'] = []

uploaded_file = st.file_uploader("Upload new data")

if uploaded_file is not None:
    new_data = pd.read_csv(uploaded_file)
    st.session_state['all_data'].append(new_data)


df = pd.concat(st.session_state['all_data'] + [read_data()])

param = st.selectbox('Parameter', np.sort(df.parameter.astype(str).unique()))

if param is not None:
	df = df[df.parameter == param]

hour_of_day = st.selectbox('Hour of day', np.sort(df.timestamp.str.slice(0,13).unique()))

if hour_of_day is not None:
	df = df[df.timestamp.str.slice(0,13) == hour_of_day]


df = df.iloc[:100]

st.map(df, latitude='latitude',
    longitude='longitude',
    size='value')


with st.expander('Raw data'):
	st.dataframe(data=df)

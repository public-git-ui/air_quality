import streamlit as st
import pandas as pd

st.title("Air hack")

df = pd.read_csv('small_sample.csv')

st.dataframe(data=df)
import streamlit as st
import pandas as pd
import numpy as np

dataframe = pd.read_csv('dados_entregas_last_mile.csv',sep=';')

st.write("Renner")
st.write("LastMile\n")
st.write("Luiz Eduardo de Souza")

# st.dataframe(dataframe.style.highlight_max(axis=0))
st.dataframe(dataframe)
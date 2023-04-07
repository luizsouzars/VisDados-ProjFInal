import streamlit as st
import pandas as pd
import numpy as np

dataframe = pd.read_csv('data\dados_entregas_last_mile.csv',sep=';')

st.title("___ Renner - LastMile ___")
st.subtitle("Projeto da disciplina de Visualização de Dados\nProfessora: Isabel")
st.write("Desenvolvido por:\nFlorensa Dimer, Leandra Torbes e Luiz Eduardo de Souza")

# st.dataframe(dataframe.style.highlight_max(axis=0))
st.dataframe(dataframe.head())
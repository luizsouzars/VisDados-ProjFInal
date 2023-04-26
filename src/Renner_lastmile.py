import streamlit as st
import pandas as pd
import numpy as np

dataframe = pd.read_csv(r'data/dados_entregas_last_mile.csv',sep=';')

st.title("___ Renner - LastMile ___")
st.subheader("Projeto da disciplina de Visualização de Dados\nProfessora: Isabel")
st.write("Desenvolvido por:\nFlorensa Dimer, Leandra Torbes e Luiz Eduardo de Souza")

# st.dataframe(dataframe.style.highlight_max(axis=0))
st.dataframe(dataframe.head())

# st.bar_chart(dataframe,x=dataframe['cep'],y=dataframe['remessa'].sum())
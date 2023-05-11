import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

st.set_page_config(
    page_title="Last Mile - Renner",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)

st.markdown("# Propostas para o andamento do trabalho")

st.markdown(
    """Para cada uma das perguntas a serem respondidas, será elaborado um gráfico que ajude a responder esta pergunta, seja uma resposta positiva ou negativa.  
    """
)

st.markdown(
    """#### **1 - Qual é a qualidade da roteirização em relação à sequência estabelecida?**"""
)
st.markdown(
    """Possivelmente utilizaremos um gráfico de pizza, pois por ser uma comparação binária, este tipo de gráfico consegue trazer uma ideia da divisão do todo e rapidamente se fazer uma comparação entre os valores."""
)
pizza = Image.open(r"img/pizza.jpg")
st.image(pizza, "Gráfico de Pizza (Ilustrativo)")

st.markdown(
    """#### **2 - Quais são as principais regiões, horários e dias em que há mais entregas?**"""
)
st.markdown(
    """Neste caso, utilizaremos gráfico de barras, capaz de comparar diversos valores. Será necessário plotar algumas subdivisões para representar os horários e dias da semana."""
)
barra = Image.open(r"img/barras.png")
st.image(barra, "Gráfico de Barras (Ilustrativo)")

st.markdown(
    """#### **3 - Quantas remessas estão sendo entregues na média e no máximo?**"""
)
st.markdown(
    """Pode-se utilizar um boxplot para avaliar outliers e densidade dos quartis. Uma versão simplifcada pode ser representada por cards com as informações necessárias, muito utilizados em dashboards de indicadores. """
)
box = Image.open(r"img/boxplot.png")
st.image(box, "Boxplot (Ilustrativo)")

st.markdown("""#### **4 - Quais as regiões com maior tempo médio de entrega?**""")
st.markdown(
    """Um gráfico de barras horizontal que efetue a comparação dos tempos pode ser uma maneira eficiente de se verificar estas diferenças."""
)
hbar = Image.open(r"img/hbar.png")
st.image(hbar, "Barras Horinzontais (Ilustrativo)")

st.markdown("""#### **5 - Maiores distâncias e tempo por transportadora e região?**""")
st.markdown(
    """Um heatmap pode representar a correlação entre distâncias e tempo, porém devemos avaliar qual a melhor maneira de apresentá-lo com boa capacidade de leitura e interpretabilidade sem que sejam perdidas informações."""
)
hm = Image.open(r"img/hm.png")
st.image(hm, "Heatmap (Ilustrativo)")

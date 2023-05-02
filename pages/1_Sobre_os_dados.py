import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import plotly.express as px
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

st.title("Sobre os dados")

st.markdown(
    """
A base traz dados das entregas realizadas durante o mês de novembro de 2022 em São Paulo e região metropolitana.

**codigo_rota**: Código da rota.  
**status_tracking**: Status do pedido. Esta base traz apenas o status “Delivered”, que são os pedidos que foram entregues.  
**rota_inicio**: Dia e hora de início da rota.  
**rota_final**: Dia e hora de término da rota.  
**hora_entrega**: Dia e hora em que ocorreu a entrega.  
**sq_plan**: Sequência de entrega planejada no momento da roteirização, para cada remessa.  
**cep**: Cabeça de CEP, ou seja, os três primeiros números de um CEP.  
**distancia**: Distância percorrida em km desde a última entrega (ou saída do TP, no caso da primeira entrega).  
**distancia_rota**: Distância total planejada para a rota no momento da roteirização, em km.  
**remessa**: Número de identificação da remessa entregue.  
**transportadora**: As entregas nesse período foram feitas por duas transportadoras diferentes, A e B.  
**veiculo**: Dois tipos de veículos foram utilizados para fazer as entregas, veículo médio e veículo pequeno."""
)

st.markdown("## Filtre os dados conforme sua necessidade")


@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(r"data/dados_entregas_last_mile.csv", sep=";")


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Adicionar filtros")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filtrar dados:", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Valores para {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Valores para {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Valores para {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Texto ou regex em {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df


df = get_data()

df["codigo_rota"] = pd.Categorical(df["codigo_rota"].astype("string"))
df["sq_plan"] = pd.Categorical(df["sq_plan"].astype("string"))
df["cep"] = pd.Categorical(df["cep"].astype("string"))
df["remessa"] = pd.Categorical(df["remessa"].astype("string"))
df["distancia"] = df["distancia"].astype("float")
df["distancia_rota"] = df["distancia_rota"].astype("float")
df["status_tracking"] = np.where(df["status_tracking"] == "Delivered", 1, 0)
df = df.rename(columns={"status_tracking": "Delivered"})
df_plot = filter_dataframe(df)
st.dataframe(df_plot)

dfg = df_plot
dfg = dfg.rename(columns={"status_tracking": "Delivered"})

fig = px.bar(
    x="cep",
    y="Delivered",
    data_frame=dfg,
    labels={"cep": "CEP", "Delivered": "Total de Entregas"},
    barmode="group",
)
fig.update_layout(barmode="group", xaxis={"categoryorder": "sum descending"})
fig.update_xaxes(type="category")
fig.update_traces(
    textfont_size=12, textangle=0, textposition="outside", cliponaxis=False
)

st.subheader("Total de entregas por CEP")
st.plotly_chart(fig, use_container_width=True)

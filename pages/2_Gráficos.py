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

st.title("Gráficos")

st.markdown(
    """
Segue abaixo os gráficos que podem nos ajudar a entender melhor as propostas feitas e indicar uma melhor decisão a ser tomada."""
)


@st.cache_data
def get_data() -> pd.DataFrame:
    df = pd.read_csv(r"data/dados_entregas_last_mile.csv", sep=";")

    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass
        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    df["codigo_rota"] = pd.Categorical(df["codigo_rota"].astype("string"))
    df["sq_plan"] = pd.Categorical(df["sq_plan"].astype("string"))
    df["cep"] = pd.Categorical(df["cep"].astype("string"))
    df["remessa"] = pd.Categorical(df["remessa"].astype("string"))
    df["distancia"] = df["distancia"].astype("float")
    df["distancia_rota"] = df["distancia_rota"].astype("float")
    df["status_tracking"] = np.where(df["status_tracking"] == "Delivered", 1, 0)
    df = df.rename(
        columns={"status_tracking": "delivered", "hora_entrega": "data_entrega"}
    )

    df["horas_entrega"] = df["data_entrega"] - df["rota_inicio"]
    df["horas_entrega"] = np.round((df["horas_entrega"].dt.seconds) / (60 * 60), 2)

    df["horas_rota"] = df["rota_final"] - df["rota_inicio"]
    df["horas_rota"] = np.round((df["horas_rota"].dt.seconds) / (60 * 60), 2)

    df = df[
        [
            "codigo_rota",
            "delivered",
            "rota_inicio",
            "rota_final",
            "horas_rota",
            "data_entrega",
            "horas_entrega",
            "cep",
            "distancia",
            "distancia_rota",
            "remessa",
            "transportadora",
            "veiculo",
        ]
    ]

    return df


def filter_dataframe(df: pd.DataFrame, modify=True) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    # modify = st.checkbox("Adicionar filtros")

    # if not modify:
    #     return df

    # df = df.copy()

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


ckb = st.checkbox("Mostrar Dataframe")

# Leitura e Plot do Dataframe
df = get_data()
df_plot = filter_dataframe(df)

# Exibe ou não o Dataframe
if ckb:
    st.dataframe(df_plot)

# Total de entregas por CEP
dfg = df_plot[["cep", "delivered"]].groupby("cep").agg("sum")

fig = px.bar(
    x=dfg.index,
    y="delivered",
    data_frame=dfg,
    labels={"cep": "CEP", "delivered": "Total de Entregas"},
    barmode="group",
)
fig.update_layout(barmode="group", xaxis={"categoryorder": "sum descending"})
fig.update_xaxes(type="category")
fig.update_traces(
    textfont_size=12, textangle=0, textposition="outside", cliponaxis=False
)

st.subheader("Total de entregas por CEP")
st.plotly_chart(fig, use_container_width=True)

# Média do tempo de entrega por CEP
dfmedEnt = df_plot[["cep", "horas_entrega"]].groupby("cep").agg("mean")

fig = px.bar(
    x=dfmedEnt.index,
    y="horas_entrega",
    data_frame=dfmedEnt,
    labels={"cep": "CEP", "horas_entrega": "Média de Horas"},
    barmode="group",
)
fig.update_layout(barmode="group", xaxis={"categoryorder": "sum descending"})
fig.update_xaxes(type="category")
fig.update_traces(
    textfont_size=12, textangle=0, textposition="outside", cliponaxis=False
)

st.subheader("Média do tempo de entrega por CEP")
st.plotly_chart(fig, use_container_width=True)

# Correlação entre dados
dfcorr = df_plot.drop(columns="delivered").corr(numeric_only=True)

fig = px.imshow(
    dfcorr,
    text_auto=True,
    aspect="auto",
)
st.subheader("Correlação entre Distâncias e Entregas")
st.plotly_chart(fig, use_container_width=True)

# Quantidade de entregas por dia
fig = px.histogram(
    df_plot,
    x="data_entrega",
    y="delivered",
    histfunc="sum",
    labels={"delivered": "Entregas", "data_entrega": "Data de Entrega"},
)
fig.update_layout(bargap=0.1, xaxis=dict(tickformat="%a(%d)"))
fig.update_xaxes(showgrid=True, rangeslider_visible=True, tickmode="linear")
fig.for_each_trace(
    lambda t: t.update(hovertemplate=t.hovertemplate.replace("sum of", ""))
)
fig.for_each_yaxis(lambda a: a.update(title_text=a.title.text.replace("sum of", "")))
st.subheader("Entregas por Dia")
st.plotly_chart(fig, use_container_width=True)

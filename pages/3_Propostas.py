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
    # df["sq_plan"] = pd.Categorical(df["sq_plan"].astype("string"))
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
            "sq_plan",
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


st.markdown("# Propostas para o andamento do trabalho")

st.markdown(
    """Para cada uma das perguntas a serem respondidas, será elaborado um gráfico que ajude a responder esta pergunta, seja uma resposta positiva ou negativa.  
    """
)

st.markdown(
    """#### **1 - Qualidade da roteirização em relação à sequência estabelecida**"""
)
df = get_data()

dfq1 = (
    df.groupby("codigo_rota")
    .apply(
        lambda x: x["sq_plan"].tolist()
        == list(range(min(x["sq_plan"]), max(x["sq_plan"]) + 1))
    )
    .reset_index()
)
dfq1.columns = ["codigo_rota", "sequencia_planejada"]

total_rotas = df["codigo_rota"].nunique()
total_sequencias_planejadas = dfq1[dfq1["sequencia_planejada"] == True][
    "codigo_rota"
].nunique()
total_variacoes_sequencias = dfq1[dfq1["sequencia_planejada"] == False][
    "codigo_rota"
].nunique()

labels = [
    "Total de rotas com sequência de entrega planejada",
    "Total de rotas com variação na sequência de entrega",
]
values = [total_sequencias_planejadas, total_variacoes_sequencias]

fig = px.pie(
    values=values,
    names=labels,  # color_discrete_sequence=px.colors.sequential.Electric
)
fig.update_traces(textfont_size=30)
fig.update_layout(legend=dict(font=dict(size=20)))
st.plotly_chart(fig, use_container_width=True)

st.markdown("""#### **2 - Quantidade de Entregas por CEP em cada dia**""")

dfq2 = df.copy()
dfq2["dia_mes"] = dfq2["data_entrega"].dt.date
dfq2_plot = pd.DataFrame(
    dfq2[["dia_mes", "cep", "delivered"]]
    .groupby(["dia_mes", "cep"])
    .agg("sum")
    .to_records()
)

ckb = st.checkbox("Filtrar Dados")
if ckb:
    cep = st.multiselect(
        "CEP", dfq2_plot["cep"].unique(), default=list(dfq2_plot["cep"].unique())
    )
    if cep != []:
        dfq2_plot = dfq2_plot.loc[dfq2_plot["cep"].isin(cep)]

    entregas = st.slider(
        "Total de Entregas",
        0,
        int(dfq2_plot["delivered"].max() * 2),
        (0, int(dfq2_plot["delivered"].max())),
        step=1,
    )  # Getting the input.

    dfq2_plot = dfq2_plot.loc[dfq2_plot["delivered"].between(*entregas)]

    data = st.date_input(
        f"Data",
        value=(
            dfq2_plot["dia_mes"].min(),
            dfq2_plot["dia_mes"].max(),
        ),
    )
    if len(data) == 2:
        user_date_input = tuple(map(pd.to_datetime, data))
        start_date, end_date = user_date_input
        dfq2_plot = dfq2_plot.loc[dfq2_plot["dia_mes"].between(start_date, end_date)]

fig = px.bar(
    data_frame=dfq2_plot,
    x="dia_mes",
    y="delivered",
    color="cep",
    barmode="group",
    labels={
        "cep": "CEP",
        "delivered": "Total de Entregas por CEP",
        "dia_mes": "Data de Entrega",
    },
    color_continuous_scale="Electric",
)
# fig.update_layout(xaxis={"categoryorder": "sum descending"})
fig.update_xaxes(type="category", showgrid=True)
fig.for_each_trace(
    lambda t: t.update(hovertemplate=t.hovertemplate.replace("sum of", ""))
)
fig.for_each_yaxis(lambda a: a.update(title_text=a.title.text.replace("sum of", "")))
fig.update_layout(bargap=0.1, xaxis=dict(tickformat="%a(%d)"))
st.plotly_chart(fig, use_container_width=True)

fig2 = px.bar(
    data_frame=pd.DataFrame(
        dfq2_plot[["dia_mes", "delivered"]].groupby(["dia_mes"]).agg("sum").to_records()
    ),
    x="dia_mes",
    y="delivered",
    labels={
        "cep": "CEP",
        "delivered": "Total de Entregas",
        "dia_mes": "Data de Entrega",
    },
    color_continuous_scale="Electric",
    text_auto=True,
)
fig2.update_xaxes(type="category", showgrid=True)
fig2.for_each_trace(
    lambda t: t.update(hovertemplate=t.hovertemplate.replace("sum of", ""))
)
fig2.for_each_yaxis(lambda a: a.update(title_text=a.title.text.replace("sum of", "")))
fig2.update_layout(bargap=0.1, xaxis=dict(tickformat="%a(%d)"))
st.plotly_chart(fig2, use_container_width=True)


st.markdown("""#### **3 - Horas para cada entrega por dia**""")
_, mid, _ = st.columns(3)
dfq3 = df.copy()
dfq3["dia_mes"] = dfq3["data_entrega"].dt.date
dfq3 = dfq3[["dia_mes", "horas_entrega"]]
dias = st.multiselect("Dias", dfq3["dia_mes"].unique())
if dias != []:
    dfq3 = dfq3.loc[dfq3["dia_mes"].isin(dias)]

fig = px.box(
    data_frame=dfq3,
    y="horas_entrega",
    x="dia_mes",
    # points="all",
    labels={"horas_entrega": "Horas", "dia_mes": "Data de Entrega"},
)
fig.update_xaxes(type="category", showgrid=True)
st.plotly_chart(fig, use_container_width=True)


st.markdown("""#### **4 - Média de Horas por Distância de Rota em cada CEP**""")
dfq5 = df.copy()

fig = px.density_heatmap(
    dfq5,
    x="cep",
    y="distancia_rota",
    z="horas_entrega",
    histfunc="avg",
    color_continuous_scale="Electric",
    labels={"cep": "CEP", "distancia_rota": "Distância por Rota"},
)
fig.update_xaxes(type="category", showgrid=True)
st.plotly_chart(fig, use_container_width=True)

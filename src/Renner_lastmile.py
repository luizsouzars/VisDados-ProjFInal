import streamlit as st
import pandas as pd
import numpy as np

import plotly.figure_factory as ff
import plotly.express as px
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

st.set_page_config(
    page_title="Last Mile - Renner", page_icon="chart_with_upwards_trend", layout="wide"
)


@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(r"data\dados_entregas_last_mile.csv", sep=";")


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

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
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
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
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df


st.markdown(
    """# Operação Last-Mile - Renner SA
### Ferramentas de visualização de dados para auxílio à tomada de decisão

## Conteúdo
1. [Disciplina](#disciplina)
2. [Overview](#overview)
3. [Perguntas de negócio](#perguntas)
4. [Dados](#dados)
## Disciplina<a name="disciplina"></a>
**Visualização de Dados**  
Profª.: [Isabel Harb Manssour](https://www.pucrs.br/pesquisadores/isabel-harb-manssour/)

**Alunos**:  
Florensa Dimer  
Leandra Torbes  
[Luiz Eduardo](https://github.com/luizsouzars)

## Overview <a name="overview"></a>
Operação Last-mile é a última etapa da malha logística, ou seja, a entrega para o cliente final.  
Por tratar-se de transporte, rotas e disponibilidade de entrega, é a etapa mais custosa da operação.  
Para aumentar a eficiância desta parte do processo, o time do TP (transit point) faz roteirização dos pedidos prontos e os disponibiliza aos motoristas para que a entrega seja feita.

## Perguntas de negócio<a name="perguntas"></a>
Dadas as características da operação, algumas questões que se impõem são:
- Qual é a qualidade da roteirização?
- Quais são as principais regiões, horários e dias em que há mais entregas?
- Quantas remessas estão sendo entregues na média e no máximo?
- Como o tempo de deslocamento influencia nas entregas?

## Dados <a name="dados"></a>
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
**veiculo**: Dois tipos de veículos foram utilizados para fazer as entregas, veículo médio e veículo pequeno.

# Ideias:
- Utilizar o [**streamlit**](https://streamlit.io/) para montar uma página com visualizações simples.
    - Manter o repositório do github como parte da entrega
- Definir o que queremos e podemos mostrar:
    - Exibir o dataset completo e permitir que se façam filtros
    - Exibir gráficos que se alteram conforme os filtros sejam aplicados
        - Quantidade de entregas por cep
        - Quantidade de entregas por rota
        - Distância total e média de cada rota, em um dado período de tempo""",
    True,
)

df = get_data()
df["codigo_rota"] = pd.Categorical(df["codigo_rota"].astype("string"))

df_plot = filter_dataframe(df)
st.dataframe(df_plot)

fig = px.bar(
    df_plot,
    x="codigo_rota",
    y="distancia",
)
st.plotly_chart(fig, use_container_width=True)

# st.bar_chart(dataframe,x=dataframe['cep'],y=dataframe['remessa'].sum())

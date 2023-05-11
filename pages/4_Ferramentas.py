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


st.markdown("# Ferramentas utilizadas")
st.markdown(
    """O desenvolvimento do trabalho foi através da linguagem de programação **Python**, realizado na plataforma colaboratory do google, onde foi feito um notebook desde a etapa de importação dos dados até a resposta das perguntas de negócio.\

Para todas as etapas serem construídas com sucesso, foi necessário o uso das bibliotecas *pandas*, *numpy*, *matplotlib*, *plotly* e *streamlit*.

Para apresentação, criamos uma página em núvem através do [Streamlit](https://streamlit.io/). Utilizando linguagem python, é possível criar uma página dinâmica, com filtros, apresentação de Dataframes e gráficos interativos.

Esta página está disponível neste [link](https://luizsouzars-visdados-projfinal-renner-lastmile-8mhj9f.streamlit.app/)."""
)

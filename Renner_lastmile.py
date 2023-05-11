import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Last Mile - Renner",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)

st.markdown(
    """# Operação Last-Mile - **:red[Renner SA]**
## Ferramentas de visualização de dados para auxílio à tomada de decisão"""
)
st.markdown(
    """#### Operação Last-mile é a última etapa da malha logística da **:red[Renner]**, ou seja, a entrega para o cliente final. Por tratar-se de transporte, rotas e disponibilidade de entrega, é a etapa mais custosa da operação. Para aumentar a eficiância desta parte do processo, o time do **TP (transit point)** faz roteirização dos pedidos prontos e os disponibiliza aos motoristas para que a entrega seja feita."""
)

rot1 = Image.open(r"img/roteir1.jpg")
st.image(rot1)

st.markdown(
    """## Perguntas de negócio
### Dadas as características da operação, algumas questões que se impõem são:
- ##### Qual é a qualidade da roteirização?
- ##### Quais são as principais regiões, horários e dias em que há mais entregas?
- ##### Quantas remessas estão sendo entregues na média e no máximo?
- ##### Como o tempo de deslocamento influencia nas entregas?"""
)
st.markdown(
    """##### Buscando entender esta dinâmica e responder à estas questões, foi elaborado um estudo para que fosse possível visualizar os dados de forma mais clara e auxiliar os tomadores de decisão na condução de mudanças necessárias e acompanhamento sumarizado do dia-a-dia."""
)

st.markdown("")
st.markdown("")
st.markdown("")
st.markdown(
    """
> ##### *_Este trabalho faz parte da disciplina de **Visualização de Dados**, lecionada pela professora [Isabel Harb Manssour](https://www.pucrs.br/pesquisadores/isabel-harb-manssour/)._*
> ##### *_**Alunos**: [Leandra Torbes](https://github.com/ltorbes) | [Luiz Eduardo](https://github.com/luizsouzars)_*""",
    True,
)

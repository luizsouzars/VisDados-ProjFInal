# Operação Last-Mile - Renner SA
### Ferramentas de visualização de dados para auxílio à tomada de decisão

## Conteúdo
1. [Disciplina](#disciplica)
2. [Overview](#overview)
3. [Perguntas de negócio](#perguntas)
4. [Dados](#dados)
## Disciplina <a name="disciplica"><a/>
**Visualização de Dados**  
Profª.: [Isabel Harb Manssour](https://www.pucrs.br/pesquisadores/isabel-harb-manssour/)

**Alunos**:  
Florensa Dimer  
Leandra Torbes  
[Luiz Eduardo](https://github.com/luizsouzars)

## Overview <a name="overview"><a/>
Operação Last-mile é a última etapa da malha logística, ou seja, a entrega para o cliente final.  
Por tratar-se de transporte, rotas e disponibilidade de entrega, é a etapa mais custosa da operação.  
Para aumentar a eficiância desta parte do processo, o time do TP (transit point) faz roteirização dos pedidos prontos e os disponibiliza aos motoristas para que a entrega seja feita.

## Perguntas de negócio<a name="perguntas"><a/>
Dadas as características da operação, algumas questões que se impõem são:
- Qual é a qualidade da roteirização?
- Quais são as principais regiões, horários e dias em que há mais entregas?
- Quantas remessas estão sendo entregues na média e no máximo?
- Como o tempo de deslocamento influencia nas entregas?

## Dados <a name="dados"><a/>
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
        - Distância total e média de cada rota, em um dado período de tempo

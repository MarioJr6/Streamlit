# Importando as bibliotecas para utilizar no desenvolvimento do painel
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
import streamlit_extras
import numpy as np

from plotly.subplots import make_subplots
from streamlit_extras.metric_cards import style_metric_cards

# Configuração inicial padrão
st.set_page_config(
    page_title="Painel de Monitoramento Ambiental de SARS-CoV-2",
    page_icon="	:chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state='collapsed'
)

# Definindo o primeiro container
container_1 = st.container()
with container_1: 
    # Definindo as colunas que irei utilizar
    col1, col2, col3 = st.columns([1,4,1])
    # Adicionando as imagens ao painel e o meu título desejado, centralizando dele no meio do painel
    col1.image('https://github.com/MarioJr6/MonitoramentoAmbiental/blob/main/Logo%20CEVS.png?raw=true', width=200)
    col2.markdown("<h2 style='text-align: center;'>Painel de Monitoramento Ambiental de SARS-CoV-2</h2>", unsafe_allow_html=True)
    col3.image('https://github.com/MarioJr6/MonitoramentoAmbiental/blob/main/Logo%20Estado.png?raw=true', width=300)

# Função para tratamento dos meus dados contendo os casos de covid
@st.cache_data
def fetch_and_clean_data(url):
    df_casos = pd.read_csv(url, encoding="UTF-8", sep=";")
    df_casos['DATA_SINTOMAS']=pd.to_datetime(df_casos['DATA_SINTOMAS'], format='%d/%m/%Y')
    df_casos['DATA_CONFIRMACAO']=pd.to_datetime(df_casos['DATA_CONFIRMACAO'], format='%d/%m/%Y')

  # Agrupando os dados de forma que eu tenha todas as datas do ano
    grouped = pd.pivot_table(data=df_casos, index='DATA_SINTOMAS', columns='MUNICIPIO', values='CRITERIO', aggfunc='count').fillna(0).reset_index()
    colunas = ['DATA_SINTOMAS', 'CAPÃO DA CANOA', 'CAXIAS DO SUL', 'PASSO FUNDO',
           'SANTA MARIA', 'SANTA ROSA', 'TORRES']
    grouped = grouped[colunas]
    
    return grouped

# Realizando a leitura dos dados para utilizar no painel
df_casos = fetch_and_clean_data('https://ti.saude.rs.gov.br/covid19/download?2023')
df_esgoto = pd.read_table('https://docs.google.com/spreadsheets/d/e/2PACX-1vTZfjxdY8_x5WNd9_NE3QQPeche-dMdY5KdvNpq8H4W-lmUTidwrKpV0uLzLtihV7UAPIl68WvugMsN/pub?gid=0&single=true&output=tsv')

# Municípios que usarei como filtro
municipio = ['CAPÃO DA CANOA', 'CAXIAS DO SUL', 'PASSO FUNDO', 'SANTA MARIA', 'SANTA ROSA', 'TORRES']

# Formatando para o tipo data
df_esgoto['Data de coleta'] = pd.to_datetime(df_esgoto['Data de coleta'], format='%d/%m/%Y')
# Filtrando para o período selecionado
df_esgoto = df_esgoto[df_esgoto['Data de coleta']>='2023-01-01']
# Transformando a a coluna carga viral para o tipo float
df_esgoto['carga_viral_n1'] = df_esgoto['carga_viral_n1'].astype(float)

# Definindo subplots (gráficos secundários) 
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Definindo o segundo container
container_2 = st.container() 
with container_2:
    col1, col2, col3, col4 = st.columns([1,1,1,1])
    # Borda visual para o selectbox
    col1.markdown(
        """
        <style>
            div[data-baseweb="select"] {
                background-color: #FF0000;
                color: white;
                border-radius: 5px;
            }
            div[data-baseweb="select"] div {
                border: none !important;
            }
        </style>
        """, unsafe_allow_html=True
    )
    # Selectbox para selecionar o município
    muni = col1.selectbox('Selecione o município', municipio)

    # Criando o filtro que utilizarei como base para os meus dados
    filtro = df_esgoto['Município']==muni
    
    # Filtrando as bases de dados
    df_esgoto_filtrado = df_esgoto[filtro]
    df_casos_filtrado = df_casos[muni]

    # Copiando minha base de dados filtrada para realizar as mudanças
    df_esgoto2 = df_esgoto_filtrado.copy()
    # Transformando o tipo de dado da coluna para string
    df_esgoto2['Data de coleta'] = df_esgoto2['Data de coleta'].astype(str)
    # Criando uma lista com as datas de coleta
    lista = df_esgoto2['Data de coleta'].tolist()

    # Formatando a data na ordem correta
    lista_formatada = []
    for i in lista:
        partes = i.split('-')
        data_ordenada = '-'.join(reversed(partes))
        lista_formatada.append(data_ordenada)


    # valor_formatado = int(df_casos_filtrado.tail(7).sum())
    # Métricas para as informações desejadas no painel, distribuidas nas colunas estabelecidas
    col2.metric(label = "Casos de COVID 19 confirmados nos últimos 7 dias", 
                value = int(df_casos_filtrado.tail(7).sum()))
    col3.metric(label = "Carga Viral de SARS-CoV-2 na ultima amostra de esgoto", 
                value = int(df_esgoto_filtrado['carga_viral_n1'].iloc[-1]))
    col4.metric(label = "Data da última análise ambiental", 
                value = lista_formatada[-1])
    
    # Estilo das métricas
    style_metric_cards(border_left_color="#FF0000")

    # Definindo os casos confirmados pela data de sintomas para ser a linha do gráfico
    fig = fig.add_trace(
      go.Scatter(x=df_casos['DATA_SINTOMAS'], y=df_casos[muni], name="Casos confirmados", mode="lines"),
      secondary_y=True,
    )
    # Utilizando minha carga viral para ser a barra do gráfico
    fig = fig.add_trace(
          go.Bar(x=df_esgoto_filtrado['Data de coleta'], y=df_esgoto_filtrado['carga_viral_n1'], name="Carga viral N1 (cópias genômicas/L)",
          marker=dict(color='red')),
          secondary_y=False, 
    )
    # Texto do gráfico
    fig = fig.update_layout(
          title_text="Carga viral no esgoto bruto e Casos de COVID 19"
    )

    # Ajustando a configuração dos eixos do gráfico
    fig.update_yaxes(title_text="<b>Carga viral N1 (cópias genômicas/L)</b>", secondary_y=False, range=[0,df_esgoto['carga_viral_n1'].max()*1.2])
    fig.update_yaxes(title_text="<b>Casos confirmados</b>", secondary_y=True, range=[0, df_casos[muni].max()*1.2])

    # Definindo a altura e largura do gráfico
    fig.update_layout(
        width=1250,  # Definir uma largura fixa
        height=560,  # Definir uma altura fixa
    )
    
    # Plotando meu gráfico
    col1.plotly_chart(fig)
    # Espaço em branco para ajustar o visual do painel
    col4.write("")
    col4.write("")
    col4.write("")

    # Iformativo do laboratório das análises e do muni selecionado no filtro
    col4.write("Análises ambientais realizadas pelo Laboratório de Virologia do ICBS UFRGS")
    col4.write('Município selecionado: {}'.format(muni))

    # Copiando a tabela filtrada para criar uma matriz informativa
    tabela = df_esgoto_filtrado.copy()

    # Extração dos meses da coluna data de coleta e dropando a coluna posteriormente
    tabela['Mês'] = tabela['Data de coleta'].dt.month
    tabela = tabela.drop('Data de coleta', axis=1)

    # Agrupando os dados apartir do mês e calculando a média dos dados
    matriz = tabela.groupby('Mês').mean().reset_index()

    # Calculando a variação absoluta em relação ao Mês anterior
    matriz['Variação absoluta'] = matriz['carga_viral_n1'].diff()
    matriz['Variação absoluta'].fillna("Sem dados", inplace= True)
    
    # Calculando a variação em porcentagem em relação ao Mês anterior
    matriz['Variação em porcentagem'] = matriz['carga_viral_n1'].pct_change() * 100
    matriz['Variação em porcentagem'].fillna("Sem dados", inplace= True)

    # Renomeando a coluna e o tipo 
    matriz = matriz.rename(columns={'carga_viral_n1':'Média da carga viral mensal'})
    matriz['Média da carga viral mensal'] = matriz['Média da carga viral mensal'].astype(int)

    # Função para transformar os valores em inteiro e retornar os que estão em formato texto
    def conversao(valor):
        try:
            return int(float(valor))
        except ValueError:
            return valor
    
    # Função para verificar a presença de valores infinitos na coluna
    def processamento_coluna(coluna): 
        resultado = []
        for valor in coluna: 
            if isinstance(valor, (int, float)) and not np.isinf(valor):
                resultado.append(f"{valor:.1f}%")
            elif isinstance(valor, str): 
                resultado.append(valor)
            else: 
                resultado.append(0)
        return resultado
   
    # Aplicando as funções
    matriz['Variação absoluta'] = matriz['Variação absoluta'].apply(conversao)
    matriz['Coluna teste'] = processamento_coluna(matriz['Variação em porcentagem'])
    
    # Dropando e renomeando as colunas
    matriz = matriz.drop('Variação em porcentagem', axis=1)
    matriz = matriz.rename(columns={'Coluna teste':'Variação em porcentagem'})

    matriz_ = matriz.reset_index(drop=True)

    # Plotando a tabela
    col4.table(matriz_.style.set_table_styles(
    [
        dict(selector="thead th", props=[("background-color", "#3498db"), ("color", "white")]),
        dict(selector="tbody td", props=[("border", "1px solid #dddddd")]),
    ]
    ))

# Importando as bibliotecas para utilizar no desenvolvimento do painel
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
import streamlit_extras
import numpy as np
import webbrowser

from plotly.subplots import make_subplots
from streamlit_extras.metric_cards import style_metric_cards
from datetime import datetime

# Configuração inicial padrão
st.set_page_config(
    page_title="Painel de Monitoramento Ambiental de SARS-CoV-2",
    page_icon="	:chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state='collapsed'
)

def data_atualizacao():
    return datetime.now().strftime("%d/%m/%Y")

# Definindo o primeiro container
container_1 = st.container()
with container_1: 
    # Definindo as colunas que irei utilizar
    col1, col2, col3 = st.columns([1,4,1])
    # Adicionando as imagens ao painel e o meu título desejado, centralizando dele no meio do painel
    col1.image('https://github.com/MarioJr6/MonitoramentoAmbiental/blob/main/Logo%20CEVS.png?raw=true', width=200)
    col2.markdown("<h2 style='text-align: center;'>Painel de Monitoramento Ambiental de SARS-CoV-2</h2>", unsafe_allow_html=True)
    col2.markdown(f"<p style='text-align: center;'>Atualizado em {data_atualizacao()}</p>", unsafe_allow_html=True)
    col3.image('https://github.com/MarioJr6/MonitoramentoAmbiental/blob/main/Logo%20Estado.png?raw=true', width=300)

# Função para tratamento dos meus dados contendo os casos de covid
@st.cache_data
def funcao_covid(url):
    df_casos = pd.read_csv(url, encoding="UTF-8", sep=";")
    df_casos['DATA_SINTOMAS']=pd.to_datetime(df_casos['DATA_SINTOMAS'], format='%d/%m/%Y')
    df_casos['DATA_CONFIRMACAO']=pd.to_datetime(df_casos['DATA_CONFIRMACAO'], format='%d/%m/%Y')

  # Agrupando os dados de forma que eu tenha todas as datas do ano
    grouped = pd.pivot_table(data=df_casos, index='DATA_SINTOMAS', columns='MUNICIPIO', values='CRITERIO', aggfunc='count').fillna(0).reset_index()
    colunas = ['DATA_SINTOMAS', 'CAPÃO DA CANOA', 'CAXIAS DO SUL', 'PASSO FUNDO',
           'SANTA MARIA', 'SANTA ROSA', 'TORRES']
    grouped = grouped[colunas]
    
    return grouped

# Dicionário dos meses
meses = { 1: 'Janeiro', 2: 'Fevereiro', 3: 'Março',
          4: 'Abril', 5: 'Maio', 6: 'Junho',
          7: 'Julho', 8: 'Agosto', 9: 'Setembro',
          10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}

# Realizando a leitura dos dados para utilizar no painel
df_casos = funcao_covid('https://ti.saude.rs.gov.br/covid19/download?2023')
df_esgoto = pd.read_table('https://docs.google.com/spreadsheets/d/e/2PACX-1vTZfjxdY8_x5WNd9_NE3QQPeche-dMdY5KdvNpq8H4W-lmUTidwrKpV0uLzLtihV7UAPIl68WvugMsN/pub?gid=0&single=true&output=tsv')

import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

st.set_page_config(
    page_title="Painel de Monitoramento Ambiental de SARS-CoV-2",
    page_icon="	:snake:",
    layout="wide",
    initial_sidebar_state='collapsed'
)

container_1 = st.container()
container_2 = st.container() 

with container_1: 
    col1, col2, col3 = st.columns([1,4,1])
    col1.image('https://github.com/MarioJr6/MonitoramentoAmbiental/blob/main/Logo%20CEVS.png?raw=true', width=200)
    col2.markdown("<h2 style='text-align: center;'>Painel de Monitoramento Ambiental de SARS-CoV-2</h2>", unsafe_allow_html=True)
    col3.image('https://github.com/MarioJr6/MonitoramentoAmbiental/blob/main/Logo%20Estado.png?raw=true', width=300)

# Leitura dos dados
df_casos = pd.read_table('https://docs.google.com/spreadsheets/d/e/2PACX-1vSB6M4e3McfIwkph-nzq_SefdhzGx_6ycMmj8SHTzcXYrkUMe1P7Nza6BpKPva_HUhpDXBgwKXrHREx/pub?output=tsv')
df_esgoto = pd.read_table('https://docs.google.com/spreadsheets/d/e/2PACX-1vTZfjxdY8_x5WNd9_NE3QQPeche-dMdY5KdvNpq8H4W-lmUTidwrKpV0uLzLtihV7UAPIl68WvugMsN/pub?gid=0&single=true&output=tsv')

municipio = ['CAPÃO DA CANOA', 'CAXIAS DO SUL', 'PASSO FUNDO', 'SANTA MARIA', 'SANTA ROSA', 'SÃO LEOPOLDO', 'TORRES']

df_esgoto['Data de coleta']=pd.to_datetime(df_esgoto['Data de coleta'], format='%d/%m/%Y')
df_esgoto=df_esgoto[df_esgoto['Data de coleta']>='2023-01-01']
df_esgoto['carga_viral_n1'] = df_esgoto['carga_viral_n1'].astype(float)

fig = make_subplots(specs=[[{"secondary_y": True}]])

with container_2: 
    coluna1, coluna2, colun3 = st.columns(3)
    coluna1.metric('teste')

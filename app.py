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

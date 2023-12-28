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

dash_1 = st.container()

with dash_1: 
    st.image('https://github.com/MarioJr6/MonitoramentoAmbiental/blob/main/Logo%20CEVS.png?raw=true', width=200)
    st.markdown("<h2 style='text-align: center;'>Painel de Monitoramento Ambiental de SARS-CoV-2</h2>", unsafe_allow_html=True)
    st.write("")
    st.image('https://github.com/MarioJr6/MonitoramentoAmbiental/blob/main/Logo%20Estado.png?raw=true', width=300)











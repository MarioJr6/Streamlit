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

container_2 = st.container() 
with container_2:
    col1, col2, col3, col4 = st.columns([1.5,1,1,1])
    muni = col1.selectbox('Selecione o município', municipio)
    st.write('Município selecionado:', muni)
    
    filtro = df_esgoto['Município']==muni
    df_esgoto_filtrado = df_esgoto[filtro]
    df_casos_filtrado = df_casos[muni]
    
    # Manipulação do meu data frame df_esgoto_filtrado
    df_esgoto2 = df_esgoto_filtrado.copy()
    df_esgoto2['Data de coleta']=df_esgoto2['Data de coleta'].astype(str)
    lista = df_esgoto2['Data de coleta'].tolist()

    col2.metric(label="Casos de COVID 19 confirmados nos últimos 7 dias", 
                value=df_casos_filtrado.tail(7).sum())
    col3.metric(label="Carga Viral (CG/L) de SARS-CoV-2 na ultima amostra de esgoto", 
                value=df_esgoto_filtrado['carga_viral_n1'].iloc[-1])
    col4.metric(label="Data da última análise ambiental", 
                value=lista[-1])

    fig = fig.add_trace(
      go.Scatter(x=df_casos['DATA_SINTOMAS'], y=df_casos[muni], name="Casos diários", mode="lines"),
      secondary_y=True,
      )
    fig = fig.add_trace(
          go.Bar(x=df_esgoto_filtrado['Data de coleta'], y=df_esgoto_filtrado['carga_viral_n1'], name="Carga Viral no esgoto",
                 ),
          secondary_y=False,
      )
    fig.update_yaxes(title_text="Carga viral", secondary_y=False, range=[0,df_esgoto['carga_viral_n1'].max()*1.2])
    fig.update_yaxes(title_text="Casos diários", secondary_y=True, range=[0,df_casos[muni].max()*1.2])

    # Atualize o layout do gráfico para ocupar toda a largura disponível
    fig.update_layout(
        width=1800,  # Definir uma largura fixa
        height=500,  # Definir uma altura fixa
    )
    st.plotly_chart(fig)


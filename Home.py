# PÁGINA PRINCIPAL (HOME) - GROWTH DASHBOARD CURY COMPANY
# Para rodar todos os 3 dashboards juntos: streamlit run Home.py

import os
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home - Cury Company",
    page_icon="🎲",
    layout="wide"
)

if os.path.exists("logo.png"):
    image = Image.open("logo.png")
    st.sidebar.image(image, width=120)

st.sidebar.markdown("# Cury Company")
st.sidebar.markdown("## Fastest Delivery in Town")
st.sidebar.markdown("""---""")
st.sidebar.markdown("### Powered by Comunidade DS")

st.write("# Curry Company Growth Dashboard")

st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - **Visão Empresa:**
        - *Visão Gerencial:* Métricas gerais de comportamento.
        - *Visão Tática:* Indicadores semanais de crescimento.
        - *Visão Geográfica:* Insights de geolocalização.
    - **Visão Entregador:**
        - Acompanhamento dos indicadores semanais de crescimento.
    - **Visão Restaurante:**
        - Indicadores semanais de crescimento dos restaurantes.
    ### Ask for Help
    - Time de Data Science no Discord
        - @meigarom
"""
)

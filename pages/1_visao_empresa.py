# PÁGINA 1: VISÃO EMPRESA - GROWTH DASHBOARD CURY COMPANY

import os
from datetime import datetime
import pandas as pd
import plotly.express as px
import folium
import streamlit as st
from PIL import Image

st.set_page_config(page_title="Visão Empresa", page_icon="📈", layout="wide")


# 1. DEFINIÇÃO DAS FUNÇÕES (ENTRADA -> PROCESSAMENTO -> SAÍDA)
def clean_code(df):
    """Limpa o DataFrame bruto e retorna o DataFrame pronto para análise."""
    linhas_selecionadas = df["Delivery_person_Age"] != "NaN "
    df = df.loc[linhas_selecionadas, :].copy()
    df["Delivery_person_Age"] = df["Delivery_person_Age"].astype(int)

    df["Delivery_person_Ratings"] = df["Delivery_person_Ratings"].astype(float)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], format="%d-%m-%Y")

    linhas_selecionadas = df["multiple_deliveries"] != "NaN "
    df = df.loc[linhas_selecionadas, :].copy()
    df["multiple_deliveries"] = df["multiple_deliveries"].astype(int)

    df.loc[:, "ID"] = df.loc[:, "ID"].str.strip()
    df.loc[:, "Delivery_person_ID"] = df.loc[:, "Delivery_person_ID"].str.strip()
    df.loc[:, "Weatherconditions"] = df.loc[:, "Weatherconditions"].str.strip()
    df.loc[:, "Road_traffic_density"] = df.loc[:, "Road_traffic_density"].str.strip()
    df.loc[:, "Type_of_order"] = df.loc[:, "Type_of_order"].str.strip()
    df.loc[:, "Type_of_vehicle"] = df.loc[:, "Type_of_vehicle"].str.strip()
    df.loc[:, "City"] = df.loc[:, "City"].str.strip()
    df.loc[:, "Festival"] = df.loc[:, "Festival"].str.strip()

    df = df.loc[df["Weatherconditions"] != "conditions NaN", :].copy()
    df = df.loc[df["Road_traffic_density"] != "NaN", :].copy()
    df = df.loc[df["City"] != "NaN", :].copy()
    df = df.loc[df["Festival"] != "NaN", :].copy()

    df["Time_taken(min)"] = df["Time_taken(min)"].str.replace("(min) ", "", regex=False).astype(int)

    return df.reset_index(drop=True)


def order_metric(df):
    """Entrada: df | Processamento: conta pedidos por dia | Saída: gráfico de barras (fig)"""
    df_aux = df.loc[:, ["ID", "Order_Date"]].groupby("Order_Date").count().reset_index()
    df_aux.columns = ["order_date", "qtde_entregas"]
    fig = px.bar(df_aux, x="order_date", y="qtde_entregas")
    return fig


def traffic_order_share(df):
    """Entrada: df | Processamento: calcula % de pedidos por trânsito | Saída: gráfico de pizza (fig)"""
    df_aux = df.loc[:, ["ID", "Road_traffic_density"]].groupby("Road_traffic_density").count().reset_index()
    df_aux["perc_ID"] = 100 * (df_aux["ID"] / df_aux["ID"].sum())
    fig = px.pie(df_aux, values="perc_ID", names="Road_traffic_density")
    return fig


def traffic_order_city(df):
    """Entrada: df | Processamento: conta pedidos por cidade e trânsito | Saída: gráfico de bolhas (fig)"""
    df_aux = df.loc[:, ["ID", "City", "Road_traffic_density"]].groupby(["City", "Road_traffic_density"]).count().reset_index()
    fig = px.scatter(df_aux, x="City", y="Road_traffic_density", size="ID", color="City")
    return fig


def order_by_week(df):
    """Entrada: df | Processamento: extrai semana do ano e conta pedidos | Saída: gráfico de linhas (fig)"""
    df["week_of_year"] = df["Order_Date"].dt.strftime("%U")
    df_aux = df.loc[:, ["ID", "week_of_year"]].groupby("week_of_year").count().reset_index()
    fig = px.line(df_aux, x="week_of_year", y="ID")
    return fig


def order_share_by_week(df):
    """Entrada: df | Processamento: divide pedidos na semana por entregadores únicos | Saída: gráfico de linhas (fig)"""
    df["week_of_year"] = df["Order_Date"].dt.strftime("%U")
    df_aux1 = df.loc[:, ["ID", "week_of_year"]].groupby("week_of_year").count().reset_index()
    df_aux2 = df.loc[:, ["Delivery_person_ID", "week_of_year"]].groupby("week_of_year").nunique().reset_index()
    df_aux = pd.merge(df_aux1, df_aux2, how="inner")
    df_aux["order_by_delivery"] = df_aux["ID"] / df_aux["Delivery_person_ID"]
    fig = px.line(df_aux, x="week_of_year", y="order_by_delivery")
    return fig


def country_maps(df):
    """Entrada: df | Processamento: calcula mediana de lat/lon e desenha mapa Folium | Saída: exibe o mapa"""
    columns = [
        "City",
        "Road_traffic_density",
        "Delivery_location_latitude",
        "Delivery_location_longitude"
    ]
    columns_groupby = ["City", "Road_traffic_density"]
    data_plot = df.loc[:, columns].groupby(columns_groupby).median().reset_index()

    map_ = folium.Map(zoom_start=11)
    for index, location_info in data_plot.iterrows():
        folium.Marker(
            [location_info["Delivery_location_latitude"], location_info["Delivery_location_longitude"]],
            popup=location_info[["City", "Road_traffic_density"]]
        ).add_to(map_)

    try:
        from streamlit_folium import folium_static
        folium_static(map_, width=1024, height=600)
    except ImportError:
        st.components.v1.html(map_._repr_html_(), height=600)


# 2. INÍCIO DA ESTRUTURA LÓGICA DO CÓDIGO (IMPORTAÇÃO E LIMPEZA)
df_raw = pd.read_csv("base de dados/train.csv")
df = clean_code(df_raw)


# 3. BARRA LATERAL (SIDEBAR) E FILTROS
st.header("Marketplace - Visão Cliente (Empresa)")

if os.path.exists("logo.png"):
    image = Image.open("logo.png")
    st.sidebar.image(image, width=120)

st.sidebar.markdown("# Cury Company")
st.sidebar.markdown("## Fastest Delivery in Town")
st.sidebar.markdown("""---""")

st.sidebar.markdown("## Selecione uma data limite")

date_slider = st.sidebar.slider(
    "Até qual valor?",
    value=datetime(2022, 4, 13),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format="DD-MM-YYYY"
)

st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    "Quais as condições do trânsito?",
    ["Low", "Medium", "High", "Jam"],
    default=["Low", "Medium", "High", "Jam"]
)

st.sidebar.markdown("""---""")
st.sidebar.markdown("### Powered by Comunidade DS")

linhas_selecionadas = df["Order_Date"] < date_slider
df = df.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = df["Road_traffic_density"].isin(traffic_options)
df = df.loc[linhas_selecionadas, :].copy()


# 4. LAYOUT NO STREAMLIT (CHAMANDO AS FUNÇÕES)
tab1, tab2, tab3 = st.tabs(["Visão Gerencial", "Visão Tática", "Visão Geográfica"])

with tab1:
    with st.container():
        st.markdown("# Orders by Day")
        fig = order_metric(df)
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.header("Traffic Order Share")
            fig = traffic_order_share(df)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.header("Traffic Order City")
            fig = traffic_order_city(df)
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    with st.container():
        st.markdown("# Order by Week")
        fig = order_by_week(df)
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown("# Order Share by Week")
        fig = order_share_by_week(df)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("# Country Maps")
    country_maps(df)

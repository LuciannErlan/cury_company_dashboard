# PÁGINA 3: VISÃO RESTAURANTES - GROWTH DASHBOARD CURY COMPANY

import os
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from haversine import haversine
import streamlit as st
from PIL import Image

st.set_page_config(page_title="Visão Restaurantes", page_icon="🍽️", layout="wide")


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


def distance(df, fig=False):
    """Calcula a distância entre restaurantes e locais de entrega usando Haversine."""
    cols = [
        "Restaurant_latitude",
        "Restaurant_longitude",
        "Delivery_location_latitude",
        "Delivery_location_longitude"
    ]
    df["distance"] = df.loc[:, cols].apply(
        lambda x: haversine(
            (x["Restaurant_latitude"], x["Restaurant_longitude"]),
            (x["Delivery_location_latitude"], x["Delivery_location_longitude"])
        ),
        axis=1
    )

    if fig is False:
        avg_distance = np.round(df["distance"].mean(), 2)
        return avg_distance
    else:
        avg_distance = df.loc[:, ["City", "distance"]].groupby("City").mean().reset_index()
        figura = go.Figure(
            data=[
                go.Pie(
                    labels=avg_distance["City"],
                    values=avg_distance["distance"],
                    pull=[0, 0.1, 0]
                )
            ]
        )
        return figura


def avg_std_time_delivery(df, festival, op):
    """Calcula o tempo médio ('avg_time') ou o desvio padrão ('std_time') das entregas."""
    df_aux = (
        df.loc[:, ["Time_taken(min)", "Festival"]]
        .groupby("Festival")
        .agg({"Time_taken(min)": ["mean", "std"]})
    )
    df_aux.columns = ["avg_time", "std_time"]
    df_aux = df_aux.reset_index()
    df_aux = np.round(df_aux.loc[df_aux["Festival"] == festival, op], 2)
    return float(df_aux.iloc[0]) if not df_aux.empty else 0.0


def avg_std_time_graph(df):
    """Retorna o gráfico de barras com barra de erro do tempo médio por cidade."""
    cols = ["Time_taken(min)", "City"]
    df_aux = df.loc[:, cols].groupby("City").agg({"Time_taken(min)": ["mean", "std"]})
    df_aux.columns = ["avg_time", "std_time"]
    df_aux = df_aux.reset_index()

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name="Control",
            x=df_aux["City"],
            y=df_aux["avg_time"],
            error_y=dict(type="data", array=df_aux["std_time"])
        )
    )
    fig.update_layout(barmode="group")
    return fig


def avg_std_time_on_traffic(df):
    """Retorna o gráfico Sunburst de tempo médio e desvio padrão por cidade e tráfego."""
    cols = ["Time_taken(min)", "City", "Road_traffic_density"]
    df_aux = (
        df.loc[:, cols]
        .groupby(["City", "Road_traffic_density"])
        .agg({"Time_taken(min)": ["mean", "std"]})
    )
    df_aux.columns = ["avg_time", "std_time"]
    df_aux = df_aux.reset_index()

    fig = px.sunburst(
        df_aux,
        path=["City", "Road_traffic_density"],
        values="avg_time",
        color="std_time",
        color_continuous_scale="RdBu",
        color_continuous_midpoint=np.average(df_aux["std_time"])
    )
    return fig


# 2. INÍCIO DA ESTRUTURA LÓGICA DO CÓDIGO (IMPORTAÇÃO E LIMPEZA)
df_raw = pd.read_csv("base de dados/train.csv")
df = clean_code(df_raw)


# 3. BARRA LATERAL (SIDEBAR) E FILTROS
st.header("Marketplace - Visão Restaurantes")

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
tab1, tab2, tab3 = st.tabs(["Visão Gerencial", "_", "_"])

with tab1:
    with st.container():
        st.title("Overal Metrics")

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            delivery_unique = len(df.loc[:, "Delivery_person_ID"].unique())
            col1.metric("Entregadores", delivery_unique)

        with col2:
            avg_distance = distance(df, fig=False)
            col2.metric("A distância média", avg_distance)

        with col3:
            df_aux = avg_std_time_delivery(df, "Yes", "avg_time")
            col3.metric("Tempo Médio c/ Festival", df_aux)

        with col4:
            df_aux = avg_std_time_delivery(df, "Yes", "std_time")
            col4.metric("STD Entrega c/ Festival", df_aux)

        with col5:
            df_aux = avg_std_time_delivery(df, "No", "avg_time")
            col5.metric("Tempo Médio s/ Festival", df_aux)

        with col6:
            df_aux = avg_std_time_delivery(df, "No", "std_time")
            col6.metric("STD Entrega s/ Festival", df_aux)

    with st.container():
        st.markdown("""---""")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### Tempo Médio de Entrega por Cidade")
            fig = avg_std_time_graph(df)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("##### Distribuição da Distância")
            cols = ["Time_taken(min)", "City", "Type_of_order"]
            df_aux = (
                df.loc[:, cols]
                .groupby(["City", "Type_of_order"])
                .agg({"Time_taken(min)": ["mean", "std"]})
            )
            df_aux.columns = ["avg_time", "std_time"]
            df_aux = df_aux.reset_index()
            st.dataframe(df_aux)

    with st.container():
        st.markdown("""---""")
        st.title("Distribuição do Tempo")

        col1, col2 = st.columns(2)

        with col1:
            fig = distance(df, fig=True)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = avg_std_time_on_traffic(df)
            st.plotly_chart(fig, use_container_width=True)

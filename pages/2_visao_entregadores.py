# PÁGINA 2: VISÃO ENTREGADORES - GROWTH DASHBOARD CURY COMPANY

import os
from datetime import datetime
import pandas as pd
import streamlit as st
from PIL import Image

st.set_page_config(page_title="Visão Entregadores", page_icon="🚚", layout="wide")


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


def top_delivers(df, top_asc):
    """Calcula o Top 10 entregadores por cidade (top_asc=True para mais rápidos, False para mais lentos)."""
    df2 = (
        df.loc[:, ["Delivery_person_ID", "City", "Time_taken(min)"]]
        .groupby(["City", "Delivery_person_ID"])
        .mean()
        .sort_values(["City", "Time_taken(min)"], ascending=top_asc)
        .reset_index()
    )

    df_aux01 = df2.loc[df2["City"] == "Metropolitian", :].head(10)
    df_aux02 = df2.loc[df2["City"] == "Urban", :].head(10)
    df_aux03 = df2.loc[df2["City"] == "Semi-Urban", :].head(10)

    df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
    return df3


# 2. INÍCIO DA ESTRUTURA LÓGICA DO CÓDIGO (IMPORTAÇÃO E LIMPEZA)
df_raw = pd.read_csv("base de dados/train.csv")
df = clean_code(df_raw)


# 3. BARRA LATERAL (SIDEBAR) E FILTROS
st.header("Marketplace - Visão Entregadores")

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
        st.title("Overall Metrics")

        col1, col2, col3, col4 = st.columns(4, gap="large")

        with col1:
            maior_idade = df.loc[:, "Delivery_person_Age"].max()
            col1.metric("Maior de idade", maior_idade)

        with col2:
            menor_idade = df.loc[:, "Delivery_person_Age"].min()
            col2.metric("Menor de idade", menor_idade)

        with col3:
            melhor_condicao = df.loc[:, "Vehicle_condition"].max()
            col3.metric("Melhor condição", melhor_condicao)

        with col4:
            pior_condicao = df.loc[:, "Vehicle_condition"].min()
            col4.metric("Pior condição", pior_condicao)

    with st.container():
        st.markdown("""---""")
        st.title("Avaliações")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### Avaliação média por Entregador")
            df_avg_ratings_per_deliver = (
                df.loc[:, ["Delivery_person_Ratings", "Delivery_person_ID"]]
                .groupby("Delivery_person_ID")
                .mean()
                .reset_index()
            )
            st.dataframe(df_avg_ratings_per_deliver)

        with col2:
            st.markdown("##### Avaliação média por trânsito")
            df_avg_std_rating_by_traffic = (
                df.loc[:, ["Delivery_person_Ratings", "Road_traffic_density"]]
                .groupby("Road_traffic_density")
                .agg({"Delivery_person_Ratings": ["mean", "std"]})
            )
            df_avg_std_rating_by_traffic.columns = ["delivery_mean", "delivery_std"]
            df_avg_std_rating_by_traffic = df_avg_std_rating_by_traffic.reset_index()
            st.dataframe(df_avg_std_rating_by_traffic)

            st.markdown("##### Avaliação média por clima")
            df_avg_std_rating_by_weather = (
                df.loc[:, ["Delivery_person_Ratings", "Weatherconditions"]]
                .groupby("Weatherconditions")
                .agg({"Delivery_person_Ratings": ["mean", "std"]})
            )
            df_avg_std_rating_by_weather.columns = ["delivery_mean", "delivery_std"]
            df_avg_std_rating_by_weather = df_avg_std_rating_by_weather.reset_index()
            st.dataframe(df_avg_std_rating_by_weather)

    with st.container():
        st.markdown("""---""")
        st.title("Velocidade de Entrega")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### Top Entregadores mais rápidos")
            df3 = top_delivers(df, top_asc=True)
            st.dataframe(df3)

        with col2:
            st.markdown("##### Top Entregadores mais lentos")
            df3 = top_delivers(df, top_asc=False)
            st.dataframe(df3)

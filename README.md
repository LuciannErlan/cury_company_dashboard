# 🍛 Cury Company — Growth Dashboard (Marketplace)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://curycompanydashboard-muwmr5qgrlyr8cycpwi8g8.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)

> 🔗 **Acesse o Dashboard interativo online:** **[Clique aqui para abrir no Streamlit Cloud](https://curycompanydashboard-muwmr5qgrlyr8cycpwi8g8.streamlit.app/)**

---

## 1. Problema de Negócio

A **Cury Company** é uma empresa de tecnologia que criou um aplicativo de delivery que conecta **restaurantes**, **entregadores** e **clientes** através do modelo de negócio de *Marketplace*.

Apesar do crescimento acelerado no volume de entregas, o CEO não possuía visibilidade consolidada dos principais **KPIs estratégicos de crescimento** da operação.

Como Cientista de Dados, o objetivo deste projeto foi estruturar um pipeline completo de **ETL (Extração, Transformação e Carga)** em Python e construir um **Growth Dashboard interativo no Streamlit**, permitindo que o CEO acompanhe as métricas operacionais e tome decisões rápidas baseadas em dados sob três perspectivas:

1. **Visão da Empresa (Crescimento e Demanda)**
2. **Visão dos Entregadores (Performance e Avaliações)**
3. **Visão dos Restaurantes (Tempo e Distância de Entrega)**

---

## 2. Premissas Assumidas na Análise

1. A análise foi realizada com dados operacionais entre **11/02/2022 e 06/04/2022** na Índia.
2. O modelo de negócio considerado foi o de **Marketplace** (intermediação entre restaurantes, entregadores e consumidores).
3. Registros ausentes (`"NaN"`) e espaços em branco nas variáveis categóricas e numéricas foram tratados na etapa de limpeza do pipeline (`clean_code`).
4. A distância entre cada restaurante e o local de entrega foi calculada em quilômetros utilizando a fórmula geodésica de **Haversine** a partir das coordenadas de latitude e longitude.

---

## 3. Estratégia da Solução

O painel estratégico foi planejado utilizando o **Método SAPE (Saída, Processo, Entrada)** e estruturado com base nas três visões principais do negócio:

### 📈 Visão 1: Do lado da Empresa
* **Visão Gerencial:**
  * Quantidade de pedidos por dia (Gráfico de Barras).
  * Distribuição percentual dos pedidos por densidade de tráfego (Gráfico de Pizza).
  * Comparação do volume de pedidos por cidade e tipo de tráfego (Gráfico de Bolhas).
* **Visão Tática:**
  * Quantidade de pedidos por semana (Gráfico de Linhas).
  * Quantidade média de pedidos por entregador por semana (Gráfico de Linhas).
* **Visão Geográfica:**
  * Localização central (mediana de latitude e longitude) de cada cidade por densidade de tráfego em um mapa interativo (`Folium`).

### 🚚 Visão 2: Do lado dos Entregadores
* **Métricas Gerais:** Maior e menor idade dos entregadores; melhor e pior condição dos veículos.
* **Avaliações:** Avaliação média por entregador; avaliação média e desvio padrão por tipo de tráfego e por condições climáticas.
* **Ranking de Velocidade:** Top 10 entregadores mais rápidos e Top 10 entregadores mais lentos por cidade (`Metropolitian`, `Urban` e `Semi-Urban`).

### 🍽️ Visão 3: Do lado dos Restaurantes
* **Métricas Gerais:** Quantidade de entregadores únicos, distância média entre restaurantes e locais de entrega, tempo médio e desvio padrão de entrega durante e fora de períodos de **Festival**.
* **Análise de Tempo e Distância:**
  * Tempo médio e desvio padrão de entrega por cidade (Gráfico de Barras com barra de erro).
  * Tempo médio e desvio padrão por cidade e tipo de pedido (Tabela detalhada).
  * Proporção da distância média por cidade (Gráfico de Pizza).
  * Tempo médio e variabilidade por cidade e densidade de tráfego (Gráfico *Sunburst*).

---

## 4. Principais Insights de Dados

1. **Impacto dos Festivais no Tempo de Entrega:** Durante os períodos de Festival (`Festival == "Yes"`), o tempo médio de entrega sobe significativamente (cerca de **45,5 minutos**), quase o dobro em comparação aos dias normais, indicando necessidade de reforço de frota em datas comemorativas.
2. **Concentração por Tipo de Cidade e Trânsito:** A região `Metropolitian` concentra a maior parte do volume de entregas, enquanto a região `Semi-Urban` apresenta os maiores tempos médios de deslocamento (~49,7 minutos).
3. **Sazonalidade de Pedidos:** A quantidade de pedidos apresenta variações claras ao longo das semanas e dias, permitindo otimizar escalas de entregadores nos dias de pico.

---

## 5. Produto Final do Projeto

Painel online interativo hospedado gratuitamente no **Streamlit Community Cloud** e acessível por qualquer navegador ou dispositivo móvel:

* 🌐 **Link de acesso:** https://curycompanydashboard-muwmr5qgrlyr8cycpwi8g8.streamlit.app/

---

## 6. Tecnologias e Ferramentas Utilizadas

* **Linguagem:** Python 3
* **Manipulação e Limpeza de Dados (ETL):** `pandas`, `numpy`, `haversine`
* **Visualização de Dados e Mapas:** `plotly`, `folium`, `streamlit-folium`, `Pillow`
* **Framework Web / Dashboard:** `streamlit`
* **Controle de Versão e Hospedagem:** Git, GitHub e Streamlit Community Cloud

---

## 7. Estrutura do Repositório

```text
├── base de dados/
│   └── train.csv                  # Base de dados bruta da Cury Company
├── pages/
│   ├── 1_visao_empresa.py         # Página 1: Métricas de crescimento da Empresa
│   ├── 2_visao_entregadores.py    # Página 2: Performance e ranking dos Entregadores
│   └── 3_visao_restaurantes.py    # Página 3: Tempo e distância dos Restaurantes
├── Home.py                        # Página inicial (capa) do Growth Dashboard
├── logo.png                       # Logotipo exibido na barra lateral
└── requirements.txt               # Lista de bibliotecas para recriação do ambiente
```

---

## 8. Como Executar o Projeto Localmente

1. Clone este repositório:
   ```bash
   git clone https://github.com/LuciannErlan/cury_company_dashboard.git
   cd cury_company_dashboard
   ```
2. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o aplicativo no Streamlit:
   ```bash
   streamlit run Home.py
   ```

---

## 9. Autor

Desenvolvido por **Luciann Erlan** durante a formação em Ciência e Análise de Dados da **Comunidade DS**.

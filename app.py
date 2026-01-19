"""Criação de dashboard web interativo para análise de dados de vendas de carros"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.header('Análise de Dados de Vendas de Carros nos EUA')

data_path = Path(__file__).resolve().parent / "vehicles_us.csv"
car_data = pd.read_csv(data_path)

# Convertendo dados para números e valores inválidos para NaN
car_data["model_year"] = pd.to_numeric(car_data["model_year"], errors="coerce")
car_data["odometer"] = pd.to_numeric(car_data["odometer"], errors="coerce")
car_data["price"] = pd.to_numeric(car_data["price"], errors="coerce")

st.subheader('Entenda o que está buscando')
st.caption('Preço vs. quilometragem com filtros por condição e combustível')

# Remoção de ausentes e duplicados, trazendo listas ordenadas e de condições válidas para opções de combustíveis e condições do veículo
condition_options = sorted(car_data["condition"].dropna().unique())
fuel_options = sorted(car_data["fuel"].dropna().unique())

selected_conditions = st.multiselect(
    'Condição',
    options=condition_options,
    default=condition_options,
)
selected_fuels = st.multiselect(
    'Combustível',
    options=fuel_options,
    default=fuel_options,
)

# Criação de cópia para não alterar o car_data original e criação de filtros de seleção
filtered_data = car_data.copy()
if selected_conditions:
    filtered_data = filtered_data[filtered_data["condition"].isin(
        selected_conditions)]
if selected_fuels:
    filtered_data = filtered_data[filtered_data["fuel"].isin(selected_fuels)]

# Criação do gráfico de dispersão com base no filtro selecionado pelo usuário
scatter_fig = px.scatter(
    filtered_data,
    x="odometer",
    y="price",
    color="condition",
    symbol="fuel",
    hover_data=["model", "model_year", "type"],
    title="Preço vs. quilometragem",
)
# Renderização do gráfico
st.plotly_chart(scatter_fig, width=1150, height=650,
                key="scatter_price_odometer")

st.subheader('Bons negócios')
st.caption('Faixa de quilometragem por faixa de preço')

# Definição de maior preço válido e criação de faixas/labels de preço para categorizar os carros
max_price = int(car_data["price"].max(skipna=True)
                ) if car_data["price"].notna().any() else 0
price_bins = [0, 5000, 10000, 15000, 20000, 30000, max_price + 1]
price_labels = ["até 5k", "5k-10k", "10k-15k", "15k-20k", "20k-30k", "30k+"]
# Esse trecho calcula o maior preço válido para definir o limite superior das faixas, cria bins de preço fixos e usa pd.cut para transformar cada preço em uma categoria de faixa (ex.: “5k–10k”). Isso permite agrupar os carros por faixa de preço e comparar a quilometragem em cada faixa no gráfico. Utilizei uma máscara booleana para identificar preços válidos e o if/else evita erro ao calcular o máximo: se houver dados, define max_price com o maior preço; se não houver, usa 0.

# Remoção de linhas sem preço/quilometragem e criação de faixas de preço para agrupar os carros
deal_data = car_data.dropna(subset=["price", "odometer"]).copy()
deal_data["price_range"] = pd.cut(
    deal_data["price"], bins=price_bins, labels=price_labels)
# Fiz novamente uma cópia para manter o DF original e transformei o preço em categoria de faixa

# Criação de box plot comparando quilometragem típica e faixa de preço
box_fig = px.box(
    deal_data,
    x="price_range",
    y="odometer",
    points="outliers",
    title="Quilometragem por faixa de preço",
)
st.plotly_chart(box_fig, width=1150, height=650, key="odometer_by_price_range")
# Para cada faixa de preço no eixo X é exibida a distribuição de quilometragem no eixo Y


st.subheader('Entenda o mercado')
st.caption('Preço médio por ano e depreciação por idade')

# Remoção de dados incompletos e cálculo de preço médio por ano do modelo
year_data = car_data.dropna(subset=["model_year", "price"]).copy()
year_data["model_year"] = year_data["model_year"].astype(int)
price_by_year = year_data.groupby("model_year", as_index=False)["price"].mean()
# Agrupei por model_year, calculei a média de price e usei as_index=False para manter model_year como coluna normal

# Configuração do gráfico de linha
year_fig = px.line(
    price_by_year,
    x="model_year",
    y="price",
    markers=True,
    title="Preço médio por ano do modelo",
)
st.plotly_chart(year_fig, width=1150, height=650, key="avg_price_by_year")

# Montando curva de depreciação por idade
current_year = int(pd.Timestamp.today().year)
year_data["age"] = current_year - year_data["model_year"]
age_price = year_data.groupby("age", as_index=False)["price"].mean()
# Peguei o ano atual do sistema, criei a coluna age calculando a idade do carro e agrupei por idade calculando preço médio

age_fig = px.line(
    age_price,
    x="age",
    y="price",
    markers=True,
    title="Depreciação média por idade do veículo",
)
st.plotly_chart(age_fig, width=1150, height=650, key="depreciation_by_age")

st.subheader('Híbridos valem o hype?')
st.caption('Preço por combustível (gas/diesel/hybrid)')

# Filtragem de combustível/preço válidos e criação de box plot do preço por tipo de combustível
fuel_price = car_data.dropna(subset=["fuel", "price"]).copy()
fuel_fig = px.box(
    fuel_price,
    x="fuel",
    y="price",
    points="outliers",
    title="Distribuição de preço por combustível",
)
st.plotly_chart(fuel_fig, width=1150, height=650, key="price_by_fuel")

"""Criação de dashboard web interativo para análise de dados de vendas de carros"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.header('Análise de Dados de Vendas de Carros nos EUA')

data_path = Path(__file__).resolve().parent / "vehicles_us.csv"
car_data = pd.read_csv(data_path)
hist_button = st.button('Create a Histogram')

if hist_button:
    st.write('Creating a Histogram...')
    fig = px.histogram(car_data, x="odometer")
    st.plotly_chart(fig, width="stretch", key="hist_button_chart")

build_histogram = st.checkbox('Create a histogram')
if build_histogram:
    st.write('Building histogram for odometer column')
    fig = px.histogram(car_data, x="odometer")
    st.plotly_chart(fig, width="stretch", key="hist_checkbox_chart")

build_scatter = st.button('Create a scatter plot')
if build_scatter:
    st.write('Creating scatter plot...')
    fig = px.scatter(car_data, x="odometer", y="price")
    st.plotly_chart(fig, width="stretch", key="scatter_chart")

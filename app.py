import pandas as pd
import plotly.express as px
import streamlit as st

car_data = pd.read_csv(
    '/Users/raimirsilva/Documents/GitHub/Sprints Projects/Sprint-5-project/vehicles_us.csv')
hist_button = st.button('Create a Histogram')

if hist_button:
    st.write('Creating a Histogram...')
    fig = px.histogram(car_data, x="odometer")
    st.plotly_chart(fig, use_container_width=True)

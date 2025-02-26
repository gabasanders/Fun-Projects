import sys
import os
sys.path.append(os.path.abspath(r"C:\Users\gabri\OneDrive\Desktop\Projects\Data Science\MoneyData"))
import streamlit as st
from api_func import *
import re
import pandas as pd
from datetime import datetime


@st.cache_data
def get_raw_data():
    df = get_finance_df()
    return df

raw_df = get_raw_data()
raw_df['Valor'] = raw_df['Valor'].apply(lambda x: re.sub(r"[^\d.]","",x))
raw_df['Valor'] = raw_df['Valor'].astype(float)
raw_df['Data'] = pd.to_datetime(raw_df['Data'],format="%d/%m/%Y")
raw_df['Ano'] = raw_df['Data'].dt.year.astype(int)
raw_df['Mes'] = raw_df['Data'].dt.month.astype(int)

# ====================== Grafico de Categoria ======================
all_categories = raw_df['Categoria'].unique()
cat_select = st.pills('Categoria',all_categories,selection_mode='multi')

line_chart_df = raw_df.copy()
line_chart_df = line_chart_df[line_chart_df['Categoria'] != 'Investimento']

futuro = st.toggle('Incluir futuro')
if not futuro:
    line_chart_df = line_chart_df[line_chart_df['Data'].dt.date <= datetime.today().date()]

if len(cat_select) >= 1:
    line_chart_df = line_chart_df[line_chart_df['Categoria'].isin(cat_select)]

all_months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
month_dict = {
    'Jan': 1, 'Fev': 2, 'Mar': 3, 'Abr': 4, 'Mai': 5, 'Jun': 6, 
    'Jul': 7, 'Ago': 8, 'Set': 9, 'Out': 10, 'Nov': 11, 'Dez': 12
}
month_select = st.sidebar.multiselect('Mes',all_months)
selected_month_nums = [month_dict[month] for month in month_select]

if len(selected_month_nums) >= 1:
    line_chart_df = line_chart_df[line_chart_df['Mes'].isin(selected_month_nums)]

st.line_chart(line_chart_df,x='Data',y='Valor')


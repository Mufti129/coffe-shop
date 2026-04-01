import streamlit as st
from services.sheets_service import connect, get_data
from services.stock_service import calculate_usage
from utils.filter import date_filter
import config

client = connect()

sales = get_data(client, config.SPREADSHEET_ID, config.SHEET_SALES)
recipe = get_data(client, config.SPREADSHEET_ID, config.SHEET_RECIPE)

sales = date_filter(sales)

usage = calculate_usage(sales, recipe)
summary = usage.groupby('produk')['qty'].sum().reset_index()

st.title("📉 Pemakaian Bahan")
st.dataframe(summary)

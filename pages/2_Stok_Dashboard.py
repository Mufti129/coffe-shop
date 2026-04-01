import streamlit as st
from services.sheets_service import connect, get_data
from services.stock_service import calculate_stock
import config

client = connect()

trans = get_data(client, config.SPREADSHEET_NAME, config.SHEET_TRANSACTIONS)
sales = get_data(client, config.SPREADSHEET_NAME, config.SHEET_SALES)
recipe = get_data(client, config.SPREADSHEET_NAME, config.SHEET_RECIPE)

stock = calculate_stock(trans, sales, recipe)

st.title("📊 Stok Saat Ini")
st.dataframe(stock)

low = stock[stock['stok'] < 100]
if not low.empty:
    st.warning("⚠️ Stok menipis!")
    st.dataframe(low)

import streamlit as st
from services.sheets_service import connect, get_data
from utils.filter import date_filter
import config

client = connect()

df = get_data(client, config.SPREADSHEET_ID, config.SHEET_TRANSACTIONS)

user_filter = st.selectbox(
    "Filter User",
    ["Semua"] + list(df['user'].unique())
)

df = date_filter(df)

if user_filter != "Semua":
    df = df[df['user'] == user_filter]

st.title("📜 Histori Transaksi")
st.dataframe(df)

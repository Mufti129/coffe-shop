import streamlit as st
from services.sheets_service import connect, get_data
import config

client = connect()

tables = {
    "products": config.SHEET_PRODUCTS,
    "transactions": config.SHEET_TRANSACTIONS,
    "sales": config.SHEET_SALES,
    "recipe": config.SHEET_RECIPE
}

choice = st.selectbox("Pilih Data", list(tables.keys()))

df = get_data(client, config.SPREADSHEET_ID, tables[choice])

st.dataframe(df)

csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    "Download CSV",
    csv,
    file_name=f"{choice}.csv",
    mime="text/csv"
)

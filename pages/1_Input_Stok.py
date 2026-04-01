import streamlit as st
from services.sheets_service import connect, append_row
import config
from datetime import date

client = connect()

st.title("📥 Input Stok")

produk = st.text_input("Produk")
tipe = st.selectbox("Tipe", ["IN", "OUT"])
qty = st.number_input("Qty", min_value=1)
keterangan = st.text_input("Keterangan")
user = st.text_input("Nama Staff")

if st.button("Simpan"):
    append_row(client, config.SPREADSHEET_NAME, config.SHEET_TRANSACTIONS, [
        str(date.today()), produk, tipe, int(qty), keterangan, user
    ])
    st.success("✅ Data berhasil disimpan")

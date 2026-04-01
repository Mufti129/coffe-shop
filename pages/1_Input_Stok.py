import streamlit as st
from services.sheets_service import connect, append_row
import config
from datetime import datetime

client = connect()

st.title("📥 Input Stok")

# =========================
# MASTER DATA (BISA DIPINDAH KE SHEET NANTI)
# =========================

produk_list = [
    "Gula",
    "Kopi",
    "Susu",
    "Teh"
]

keterangan_list = [
    "Restock Supplier",
    "Return Barang",
    "Penyesuaian Stok",
    "Waste / Rusak"
]

staff_list = [
    "Andi",
    "Budi",
    "Siti"
]

satuan_list = [
    "gram",
    "ml",
    "pcs"
]

# =========================
# INPUT FORM
# =========================

produk = st.selectbox("Produk", produk_list)

tipe = st.selectbox("Tipe", ["IN", "OUT"])

qty = st.number_input("Qty", min_value=1, step=1)

satuan = st.selectbox("Satuan", satuan_list)

keterangan = st.selectbox("Keterangan", keterangan_list)

staff = st.selectbox("Nama Staff", staff_list)

tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# =========================
# SUBMIT
# =========================

if st.button("Simpan"):

    row = [
        tanggal,
        produk,
        tipe,
        qty,
        satuan,
        keterangan,
        staff
    ]

    success = append_row(
        client,
        config.SPREADSHEET_ID,
        config.SHEET_TRANSACTIONS,
        row
    )

    if success:
        st.success("Data berhasil disimpan")
    else:
        st.error("Gagal simpan data")

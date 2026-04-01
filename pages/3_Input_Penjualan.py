import streamlit as st
import pandas as pd
from services.sheets_service import connect, append_row
import config

client = connect()

st.title("📊 Upload / Input Penjualan")

mode = st.radio("Mode", ["Upload CSV (Moka)", "Manual"])

# =========================
# MENU MAPPING (WAJIB)
# =========================
menu_mapping = {
    "Kopi Susu Gula Aren": "Kopi Susu",
    "Ice Tea": "Es Teh"
}

# =========================
# 1. UPLOAD CSV
# =========================
if mode == "Upload CSV (Moka)":

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file is not None:
        df = pd.read_csv(file)

        st.subheader("Preview Data")
        st.dataframe(df)

        st.subheader("Mapping Kolom")

        col_tanggal = st.selectbox("Tanggal", df.columns)
        col_menu = st.selectbox("Menu", df.columns)
        col_qty = st.selectbox("Qty", df.columns)
        col_harga = st.selectbox("Harga", df.columns)
        col_channel = st.selectbox("Channel", df.columns)
        col_user = st.selectbox("User", df.columns)

        if st.button("Proses Upload"):

            success_count = 0
            error_count = 0

            for _, row in df.iterrows():

                # =========================
                # VALIDASI TANGGAL
                # =========================
                tanggal = pd.to_datetime(
                    row[col_tanggal],
                    errors="coerce"
                )

                if pd.isna(tanggal):
                    error_count += 1
                    continue

                # =========================
                # VALIDASI QTY & HARGA
                # =========================
                try:
                    qty = int(row[col_qty])
                    harga = float(row[col_harga])
                except:
                    error_count += 1
                    continue

                # =========================
                # MAPPING MENU
                # =========================
                menu_raw = str(row[col_menu])
                menu = menu_mapping.get(menu_raw, menu_raw)

                # =========================
                # DATA FINAL
                # =========================
                data = [
                    tanggal.strftime("%Y-%m-%d %H:%M:%S"),
                    menu,
                    qty,
                    harga,
                    str(row[col_channel]),
                    str(row[col_user])
                ]

                result = append_row(
                    client,
                    config.SPREADSHEET_ID,
                    "sales",
                    data
                )

                if result:
                    success_count += 1
                else:
                    error_count += 1

            st.success(f"✅ Success: {success_count}")
            st.error(f"❌ Error/Skip: {error_count}")

# =========================
# 2. MANUAL INPUT
# =========================
else:

    from datetime import datetime

    menu_list = ["Es Teh", "Kopi Susu"]
    channel_list = ["Offline", "GoFood", "GrabFood"]
    user_list = ["Kasir1", "Kasir2"]

    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    menu = st.selectbox("Menu", menu_list)
    qty = st.number_input("Qty", min_value=1)
    harga = st.number_input("Harga", min_value=0)
    channel = st.selectbox("Channel", channel_list)
    user = st.selectbox("User", user_list)

    if st.button("Simpan"):

        data = [
            tanggal,
            menu,
            qty,
            harga,
            channel,
            user
        ]

        result = append_row(
            client,
            config.SPREADSHEET_ID,
            "sales",
            data
        )

        if result:
            st.success("Data tersimpan")
        else:
            st.error("Gagal simpan")

import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


# =============================
# CONNECT TO GOOGLE SHEETS
# =============================
def connect():
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]

        # Ambil dari Streamlit Secrets
        creds_dict = st.secrets["gcp_service_account"]

        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            creds_dict, scope
        )

        client = gspread.authorize(creds)

        return client

    except Exception as e:
        st.error(f"Gagal koneksi ke Google Sheets: {e}")
        return None


# =============================
# GET DATA
# =============================
def get_data(client, spreadsheet_id, sheet_name):
    try:
        sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        return df

    except Exception as e:
        st.error(f"Gagal ambil data dari sheet {sheet_name}: {e}")
        return pd.DataFrame()


# =============================
# APPEND DATA
# =============================
def append_row(client, spreadsheet_id, sheet_name, row_data):
    try:
        sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
        sheet.append_row(row_data)
        return True

    except Exception as e:
        st.error(f"Gagal tambah data ke sheet {sheet_name}: {e}")
        return False


# =============================
# CLEAR SHEET (OPTIONAL)
# =============================
def clear_sheet(client, spreadsheet_id, sheet_name):
    try:
        sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
        sheet.clear()
        return True

    except Exception as e:
        st.error(f"Gagal clear sheet {sheet_name}: {e}")
        return False

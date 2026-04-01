import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def connect():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope
    )
    return gspread.authorize(creds)

def get_data(client, sheet, worksheet):
    ws = client.open(sheet).worksheet(worksheet)
    return pd.DataFrame(ws.get_all_records())

def append_row(client, sheet, worksheet, row):
    ws = client.open(sheet).worksheet(worksheet)
    ws.append_row(row)

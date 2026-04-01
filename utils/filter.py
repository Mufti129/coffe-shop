import streamlit as st
import pandas as pd

def date_filter(df):
    start = st.date_input("Dari")
    end = st.date_input("Sampai")

    df['tanggal'] = pd.to_datetime(df['tanggal'])

    return df[
        (df['tanggal'] >= pd.to_datetime(start)) &
        (df['tanggal'] <= pd.to_datetime(end))
    ]

import streamlit as st
import pandas as pd
import time
import os

st.set_page_config(layout="wide")

st.title("📈 Statistical Arbitrage Dashboard")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_equity():
    if os.path.exists("equity.csv"):
        return pd.read_csv("equity.csv", index_col=0)
    return pd.DataFrame()

@st.cache_data
def load_logs():
    if os.path.exists("trades.log"):
        with open("trades.log", "r") as f:
            return f.readlines()[-20:]
    return []


# =========================
# AUTO REFRESH
# =========================
placeholder = st.empty()

while True:

    with placeholder.container():

        st.subheader("📊 Equity Curve")

        equity = load_equity()

        if not equity.empty:
            st.line_chart(equity)
        else:
            st.write("No equity data yet.")

        st.subheader("📜 Recent Trades")

        logs = load_logs()

        for line in logs[::-1]:
            st.text(line.strip())

    time.sleep(5)
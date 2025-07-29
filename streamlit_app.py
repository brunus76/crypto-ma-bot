
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from app.backtest.backtest import run_backtest

st.set_page_config(layout="wide")
st.title("📈 Crypto MA Crossover Bot Dashboard")

product = st.selectbox("Choose product", ["BTC-USD", "ETH-USD", "SOL-USD"])

if st.button("Run Backtest"):
    metrics = run_backtest(product)
    if not metrics:
        st.error("No trades found.")
    else:
        df = pd.read_csv(f"app/backtest/results/backtest_results_{product.replace('-', '_')}.csv")
        st.metric("Final Equity", f"${metrics['final_equity']:.2f}")
        st.metric("ROI", f"{metrics['roi']:.2f}%")
        st.metric("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")
        st.metric("Max Drawdown", f"{metrics['max_drawdown']:.2%}")

        st.line_chart(df.set_index("timestamp")["equity"])

        st.subheader("Trade Log")
        st.dataframe(df[["timestamp", "signal", "price", "action"]].sort_values("timestamp", ascending=False))

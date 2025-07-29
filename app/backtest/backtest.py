# backtest.py

from google.cloud import bigquery
import pandas as pd
import matplotlib.pyplot as plt
from backtest_config import START_CASH, TRADE_FEE, SLIPPAGE, ALLOCATION
import numpy as np
import os

def run_backtest(product="BTC-USD"):
    client = bigquery.Client()
    query = f"""
        SELECT * FROM crypto_bot.trades
        WHERE product = '{product}'
        ORDER BY trade_time ASC
    """
    trades = client.query(query).to_dataframe()
    if trades.empty:
        print(f"No trades for {product}.")
        return None

    cash = START_CASH
    position = 0.0
    equity_curve = []
    history = []

    for _, row in trades.iterrows():
        ts, signal, price = row["trade_time"], row["signal"], row["price"]
        eff_price = price * (1 + SLIPPAGE if signal == "BUY" else 1 - SLIPPAGE)

        if signal == "BUY" and cash > 0:
            used_cash = cash * ALLOCATION
            btc = (used_cash * (1 - TRADE_FEE)) / eff_price
            position += btc
            cash -= used_cash
            action = f"BUY {btc:.5f} @ ${eff_price:.2f}"

        elif signal == "SELL" and position > 0:
            sold_cash = position * eff_price * (1 - TRADE_FEE)
            cash += sold_cash * ALLOCATION
            position *= (1 - ALLOCATION)
            action = f"SELL → ${sold_cash:.2f}"

        else:
            action = "HOLD"

        value = cash + position * eff_price
        equity_curve.append((ts, value))
        history.append((ts, signal, eff_price, cash, position, value, action))

    df = pd.DataFrame(history, columns=["timestamp", "signal", "price", "cash", "position", "equity", "action"])
    out_csv = f"results/backtest_results_{product.replace('-', '_')}.csv"
    df.to_csv(out_csv, index=False)

    plot_equity_curve(equity_curve, product)
    metrics = compute_metrics(equity_curve, product)
    return metrics

def compute_metrics(equity_data, product):
    df = pd.DataFrame(equity_data, columns=["timestamp", "equity"])
    df["returns"] = np.log(df["equity"] / df["equity"].shift(1))
    df.dropna(inplace=True)

    peak = df["equity"].cummax()
    drawdown = (df["equity"] - peak) / peak
    max_drawdown = drawdown.min()

    sharpe = df["returns"].mean() / df["returns"].std() * np.sqrt(365) if len(df) > 1 else 0

    start = df["equity"].iloc[0]
    end = df["equity"].iloc[-1]
    roi = (end - start) / start * 100

    print(f"\n📈 {product} Results:")
    print(f"  Final Equity: ${end:.2f}")
    print(f"  ROI: {roi:.2f}%")
    print(f"  Max Drawdown: {max_drawdown:.2%}")
    print(f"  Sharpe Ratio: {sharpe:.2f}")

    return {
        "product": product,
        "final_equity": end,
        "roi": roi,
        "max_drawdown": max_drawdown,
        "sharpe_ratio": sharpe,
    }

def plot_equity_curve(equity_data, product):
    df = pd.DataFrame(equity_data, columns=["timestamp", "equity"])
    plt.figure(figsize=(12, 6))
    plt.plot(df["timestamp"], df["equity"], label=product)
    plt.title(f"{product} – Equity Curve")
    plt.xlabel("Time")
    plt.ylabel("USD")
    plt.grid(True)
    plt.tight_layout()
    out_img = f"results/equity_curve_{product.replace('-', '_')}.png"
    plt.savefig(out_img)
    print(f"Saved → {out_img}")
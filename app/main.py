# main.py
import pandas as pd
from datetime import datetime
from secrets import get_coinbase_credentials
from strategy import fetch_candles, check_crossover
# for plotting
from chart import plot_crossover_chart

df, signals = check_crossover(df)
plot_crossover_chart(df, signals)

def paper_trade():
    creds = get_coinbase_credentials()
    df = fetch_candles("BTC-USD", creds)
    signal = check_crossover(df)
    last_price = df["close"].iloc[-1]
    timestamp = datetime.utcnow().isoformat()


 
    if signal in ["BUY", "SELL"]:
      log_trade_bq("BTC-USD", last_price, signal)
        print(f"[{timestamp}] {signal} @ ${last_price:.2f}")
        with open("trade_log.csv", "a") as f:
            f.write(f"{timestamp},{signal},{last_price:.2f}\n")
    else:
        print(f"[{timestamp}] HOLD @ ${last_price:.2f}")

if __name__ == "__main__":
    paper_trade()
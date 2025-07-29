# strategy.py
import hmac, time, hashlib, requests
import pandas as pd

SHORT = 5
LONG = 15

def fetch_candles(product_id, creds):
    url = f"https://api.coinbase.com/api/v3/brokerage/products/{product_id}/candles"
    params = {
        "granularity": "ONE_MINUTE",
        "limit": 100
    }

    path = f"/api/v3/brokerage/products/{product_id}/candles?granularity=ONE_MINUTE&limit=100"
    timestamp = str(int(time.time()))
    message = f"{timestamp}GET{path}"
    signature = hmac.new(
        creds["api_secret"].encode(), message.encode(), hashlib.sha256
    ).hexdigest()

    headers = {
        "CB-ACCESS-KEY": creds["api_key"],
        "CB-ACCESS-SIGN": signature,
        "CB-ACCESS-TIMESTAMP": timestamp,
        "CB-ACCESS-PASSPHRASE": creds["api_passphrase"]
    }

    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    data = r.json()["candles"]
    df = pd.DataFrame(data)
    df.columns = ["start", "low", "high", "open", "close", "volume"]
    df = df.sort_values("start")
    return df

def check_crossover(df):
    df["short_ma"] = df["close"].rolling(window=SHORT).mean()
    df["long_ma"] = df["close"].rolling(window=LONG).mean()
    signals = {}

    for i in range(LONG, len(df)):
        prev = df.iloc[i-1]
        curr = df.iloc[i]
        if prev["short_ma"] <= prev["long_ma"] and curr["short_ma"] > curr["long_ma"]:
            signals[i] = "BUY"
        elif prev["short_ma"] >= prev["long_ma"] and curr["short_ma"] < curr["long_ma"]:
            signals[i] = "SELL"
    return df, signals
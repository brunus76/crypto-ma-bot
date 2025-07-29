# log_trade.py
from google.cloud import bigquery
from datetime import datetime

def log_trade_bq(product: str, price: float, signal: str):
    client = bigquery.Client()
    row = {
        "trade_time": datetime.utcnow().isoformat(),
        "product": product,
        "price": price,
        "signal": signal
    }
    errors = client.insert_rows_json("crypto_bot.trades", [row])
    if errors:
        raise Exception(f"BigQuery insert error: {errors}")
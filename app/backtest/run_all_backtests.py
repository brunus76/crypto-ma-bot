# run_all_backtests.py

from backtest import run_backtest

PRODUCTS = ["BTC-USD", "ETH-USD", "SOL-USD"]

def main():
    metrics_all = []
    for product in PRODUCTS:
        print(f"\n🔁 Running backtest for {product}...")
        metrics = run_backtest(product)
        if metrics:
            metrics_all.append(metrics)

    print("\n📊 Summary:")
    for m in metrics_all:
        print(f"{m['product']:8s} | ROI: {m['roi']:.2f}% | Sharpe: {m['sharpe_ratio']:.2f} | Max DD: {m['max_drawdown']:.2%}")

if __name__ == "__main__":
    main()
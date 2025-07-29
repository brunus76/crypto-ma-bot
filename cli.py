
import argparse
from app.backtest.run_all_backtests import run_backtest
from app.backtest.generate_report import generate_html_report

PRODUCTS = ["BTC-USD", "ETH-USD", "SOL-USD"]

def cli():
    parser = argparse.ArgumentParser(description="Crypto MA Bot CLI")
    parser.add_argument("command", choices=["backtest", "report", "all"], help="Task to run")
    parser.add_argument("--product", default=None, help="e.g. BTC-USD")

    args = parser.parse_args()

    if args.command == "backtest":
        if args.product:
            run_backtest(args.product)
        else:
            for p in PRODUCTS:
                run_backtest(p)

    elif args.command == "report":
        img_paths = [f"app/backtest/results/equity_curve_{p.replace('-', '_')}.png" for p in PRODUCTS]
        metrics = [run_backtest(p) for p in PRODUCTS]
        generate_html_report(metrics, img_paths)

    elif args.command == "all":
        metrics = []
        img_paths = []
        for p in PRODUCTS:
            m = run_backtest(p)
            if m: metrics.append(m)
            img_paths.append(f"app/backtest/results/equity_curve_{p.replace('-', '_')}.png")
        generate_html_report(metrics, img_paths)

if __name__ == "__main__":
    cli()

# chart.py
import matplotlib.pyplot as plt

def plot_crossover_chart(df, signals):
    plt.figure(figsize=(12, 6))
    plt.plot(df["start"], df["close"], label="Price")
    plt.plot(df["start"], df["short_ma"], label="Short MA")
    plt.plot(df["start"], df["long_ma"], label="Long MA")

    for idx, signal in signals.items():
        plt.scatter(df["start"].iloc[idx], df["close"].iloc[idx],
                    label=signal, marker="^" if signal == "BUY" else "v")

    plt.title("MA Crossover Strategy")
    plt.xlabel("Time")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("crossover_chart.png")
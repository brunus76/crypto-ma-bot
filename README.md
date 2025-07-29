# Crypto MA Bot

Self-hosted MA crossover bot with BigQuery logging and full backtesting.

# 📈 Crypto Moving Average Bot

A serverless, secure, and backtestable MA crossover bot using:
- 🟨 Python
- ☁️ Google Cloud (Run, Secret Manager, BigQuery)
- 📊 Visual reports (charts, ROI, Sharpe, Drawdown)

## ✅ Features

- Coinbase Advanced API Integration
- Moving Average Crossover Strategy
- Secure Secret Management via Google Secret Manager
- Serverless Deployment (Cloud Run)
- Paper Trading Mode
- Real-Time Logging to BigQuery
- Advanced Backtesting (ROI, Sharpe, MDD, equity curve)
- HTML Reporting + Looker Dashboard Support

---

## 🛠️ Setup

```bash
git clone https://github.com/YOU/crypto-ma-bot.git
cd crypto-ma-bot
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

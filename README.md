# 🤖 Binance Futures Testnet Trading Bot

A lightweight Python CLI application to place **MARKET** and **LIMIT** orders
on Binance Futures Testnet (USDT-M) with clean logging and error handling.

---

## 📁 Project Structure
trading_bot/
├── bot/
│   ├── init.py
│   ├── client.py          # Binance API connection wrapper
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging setup
├── logs/
│   └── trading_bot.log    # Auto-generated log file
├── cli.py                 # CLI entry point (run this)
├── .env                   # Your API keys (never share!)
├── .gitignore
├── requirements.txt
└── README.md

---

## ⚙️ Setup Steps

### Step 1 — Clone the repository

git clone <your-repo-url>
cd trading_bot

### Step 2 — Create virtual environment

python -m venv venv

Activate it:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

### Step 3 — Install dependencies

pip install -r requirements.txt

### Step 4 — Create your `.env` file
Create a file named `.env` in the root folder and add:
Api Key:JHv*****znLDCwVenMbm4b

> ⚠️ Get your free API keys from https://testnet.binancefuture.com

---

## 🚀 How to Run

### Test your connection first

python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.001 --test-connection

python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.001

Expected output:

🔌 Connecting to Binance Futures Testnet...
✅ Connected to Binance Futures Testnet successfully!

---

### Place a MARKET order
🔌 Connecting to Binance Futures Testnet...
🔍 Validating your inputs...
=============================================
📋 ORDER REQUEST SUMMARY
Symbol    : BTCUSDT
Side      : BUY
Type      : MARKET
Quantity  : 0.001
=============================================
✅ ORDER PLACED SUCCESSFULLY!
Order ID     : 123456789
Status       : FILLED
Executed Qty : 0.001
Avg Price    : 50000.00

---

### Place a LIMIT order
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --qty 0.001 --price 50000

python cli.py --symbol BTCUSDT --side BUY --type LIMIT --qty 0.001 --price 50000

Expected output:
🔌 Connecting to Binance Futures Testnet...
🔍 Validating your inputs...
=============================================
📋 ORDER REQUEST SUMMARY
Symbol    : BTCUSDT
Side      : BUY
Type      : LIMIT
Quantity  : 0.001
Price     : 50000
=============================================
✅ ORDER PLACED SUCCESSFULLY!
Order ID     : 987654321
Status       : NEW
Executed Qty : 0.0
Avg Price    : 50000

---

### Place a STOP_LIMIT order


python cli.py --symbol BTCUSDT --side SELL --type STOP_LIMIT --qty 0.003 --price 54800 --stop-price 55000

python cli.py --symbol BTCUSDT --side SELL --type STOP_LIMIT --qty 0.003 --price 54800 --stop-price 55000




Expected output:
📋 ORDER REQUEST SUMMARY
Symbol     : BTCUSDT
Side       : SELL
Type       : STOP_LIMIT
Quantity   : 0.003
Price      : 54800.0
Stop Price : 55000.0
✅ ORDER PLACED SUCCESSFULLY!
Order ID     : 123456789
Status       : NEW
Executed Qty : 0.0
Stop Price   : 55000.0

> Note: Order value must be at least $100. 
> qty × price must be >= 100

---

### Place a SELL order
python cli.py --symbol BTCUSDT --side SELL --type MARKET --qty 0.001

---

### Test validation (intentional errors)
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --qty 0.001
Expected:
⚠️  Input Error: Price is required for LIMIT orders. Use --price.

---


## 📋 All Arguments

| Argument | Required | Description | Example |
|---|---|---|---|
| --symbol | ✅ Yes | Trading pair | BTCUSDT |
| --side | ✅ Yes | BUY or SELL | BUY |
| --type | ✅ Yes | MARKET or LIMIT | MARKET |
| --qty | ✅ Yes | Quantity to trade | 0.001 |
| --price | LIMIT only | Limit price | 50000 |
| --test-connection | ❌ No | Test API and exit | — |

---

## 📝 Logging

All activity is automatically saved to `logs/trading_bot.log`.

Every log line looks like this:
2024-01-15 10:30:45 | INFO     | client     | BinanceClient initialized.
2024-01-15 10:30:45 | INFO     | validators | Validation passed: symbol=BTCUSDT...
2024-01-15 10:30:46 | INFO     | orders     | Placing order → {...}
2024-01-15 10:30:47 | INFO     | orders     | Order response → {...}
2024-01-15 10:30:47 | ERROR    | orders     | BinanceAPIException: {...}

Log levels used:
- `INFO` — normal operations
- `WARNING` — bad user input caught
- `ERROR` — API or network failures

---

## 🛡️ Error Handling

The bot handles these error types gracefully:

| Error Type | Example | Handled By |
|---|---|---|
| Invalid input | Wrong side, missing price | validators.py |
| Binance API error | Wrong symbol, low balance | orders.py |
| Network failure | No internet connection | orders.py |
| Missing API keys | Empty .env file | client.py |

---

## 📦 Dependencies

| Library | Purpose |
|---|---|
| python-binance | Binance API wrapper |
| python-dotenv | Load .env file safely |

Install all with:
pip install -r requirements.txt

---

## 💡 Assumptions

- Uses **Binance Futures Testnet** only — no real money involved
- LIMIT orders use **GTC** (Good Till Cancelled) by default
- Symbol input is automatically converted to uppercase
- Python 3.x is required
- Log file is auto-created on first run

---

## 👨‍💻 Author--Anil Rasani

Built as part of a Python Developer application task.


You are 100% done! 🎉🎉🎉

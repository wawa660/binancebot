# Binance Futures Trading Bot

A Python CLI application for placing orders on Binance Futures Testnet (USDT-M).

## Features

- Place MARKET and LIMIT orders (BUY/SELL)
- CLI with argument validation
- Comprehensive logging to file
- Error handling for invalid input, API errors, and network failures

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API credentials:**
   
   Edit `.env` file with your Binance Futures Testnet API keys:
   ```
   BINANCE_API_KEY=your_api_key_here
   BINANCE_SECRET_KEY=your_secret_key_here
   ```

3. **Get Testnet API Keys:**
   - Register at [Binance Futures Testnet](https://testnet.binancefuture.com)
   - Generate API keys from your account settings

## Usage

### Place a Market Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Place a Limit Order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 50000
```

### Command Line Options

| Option | Required | Description |
|--------|----------|-------------|
| `--symbol` | Yes | Trading symbol (e.g., BTCUSDT) |
| `--side` | Yes | BUY or SELL |
| `--type` | Yes | MARKET or LIMIT |
| `--quantity` | Yes | Order quantity |
| `--price` | Yes* | Price (required for LIMIT orders) |
| `--api-key` | No | API key (uses .env if not provided) |
| `--secret-key` | No | Secret key (uses .env if not provided) |

## Logging

Logs are written to the `logs/` directory with timestamps. Each run creates a new log file.

## Assumptions

- Using Binance Futures Testnet
- USDT-M futures contracts
- GTC (Good Till Cancel) time-in-force for LIMIT orders

## Project Structure

```
binancebot/
├── bot/
│   ├── __init__.py
│   ├── client.py         # Binance client wrapper
│   ├── orders.py         # Order placement logic
│   ├── validators.py     # Input validation
│   └── logging_config.py # Logging setup
├── cli.py                # CLI entry point
├── .env                  # Environment variables
├── requirements.txt      # Dependencies
└── README.md
```

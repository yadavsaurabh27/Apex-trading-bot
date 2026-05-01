# Apex Trading Bot — Binance Futures Testnet

A Python CLI application to place Market, Limit, and Stop-Limit orders on the Binance Futures Testnet (USDT-M).

## Setup

1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure credentials** — create a `.env` file in the root directory:
   ```env
   BINANCE_API_KEY=your_testnet_api_key
   BINANCE_API_SECRET=your_testnet_api_secret
   ```
   Get your testnet credentials from: https://testnet.binancefuture.com

## How to Run

### Market Order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.001
```

### Limit Order
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.001 --price 85000
```

### Stop-Limit Order (Bonus)
```bash
python cli.py --symbol BTCUSDT --side BUY --type STOP_LIMIT --qty 0.002 --price 105000 --stop_price 100000
```

### Stop-Market Order (Bonus)
```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --qty 0.002 --stop_price 90000
```

## CLI Arguments

| Argument | Required | Description |
|---|---|---|
| `--symbol` | Yes | Trading pair, e.g. `BTCUSDT` |
| `--side` | Yes | `BUY` or `SELL` |
| `--type` | Yes | `MARKET`, `LIMIT`, `STOP_LIMIT`, or `STOP_MARKET` |
| `--qty` | Yes | Order quantity |
| `--price` | For LIMIT / STOP_LIMIT | Limit price |
| `--stop_price` | For STOP_LIMIT / STOP_MARKET | Trigger price |

## Project Structure

```
trading_bot/
  bot/
    __init__.py
    client.py         # Binance client wrapper + credential loading
    orders.py         # Order placement logic
    validators.py     # Input validation
    logging_config.py # Centralized logging setup
  cli.py              # CLI entry point
  README.md
  requirements.txt
```

## Logging

All requests, responses, and errors are logged to `trading_bot.log` and the console. Each successful order logs the Order ID, Status, Executed Qty, and Avg Price.

## Assumptions

- Targets the Binance USDT-M Futures Testnet at `https://testnet.binancefuture.com`.
- Stop-Limit orders require both `--price` (limit) and `--stop_price` (trigger).
- Minimum order notional on testnet is $100 (Binance exchange rule).

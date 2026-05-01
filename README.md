# Binance Futures Testnet Trading Bot

A simplified Python application to place Market and Limit orders on the Binance Futures Testnet (USDT-M).

## Setup

1. **Clone the repository**.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables**:
   Create a `.env` file in the root directory (based on `.env.example`) with your Binance Testnet API credentials:
   ```env
   BINANCE_API_KEY=your_testnet_api_key
   BINANCE_API_SECRET=your_testnet_api_secret
   ```

## How to Run

### Market Order Example
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.001
```

### Limit Order Example
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.001 --price 60000
```

## Project Structure
- `bot/client.py`: Binance client wrapper and credential management.
- `bot/orders.py`: Core logic for order placement.
- `bot/validators.py`: Input validation logic.
- `bot/logging_config.py`: Centralized logging setup.
- `cli.py`: Command-line interface entry point.

## Logging
All API requests, successful responses, and errors are logged to `trading_bot.log` and the console.
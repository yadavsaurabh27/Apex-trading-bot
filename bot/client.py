import os
from binance.client import Client
from dotenv import load_dotenv
from .logging_config import logger

class BinanceFuturesClient:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')
        
        if not api_key or not api_secret:
            logger.error("API credentials missing in .env")
            raise ValueError("Credentials not found.")

        # Initialize for Testnet as per instructions
        self.client = Client(api_key, api_secret, testnet=True)
        # Using the specific testnet endpoint from the assignment
        self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi/v1'
        
        logger.info(f"Binance Futures Testnet Client initialized at {self.client.FUTURES_URL}")

    def place_futures_order(self, symbol, side, order_type, qty, price=None, stop_price=None):
        """
        Handles Market, Limit, Stop-Limit, and Stop-Market orders.
        """
        try:
            # Common parameters for all order types
            params = {
                "symbol": symbol.upper(),
                "side": side.upper(),
                "quantity": qty,
            }

            order_type_upper = order_type.upper()

            if order_type_upper == "MARKET":
                params["type"] = "MARKET"

            elif order_type_upper == "LIMIT":
                if not price:
                    raise ValueError("Limit orders require a --price")
                params.update({
                    "type": "LIMIT",
                    "price": str(price),
                    "timeInForce": "GTC"
                })

            elif order_type_upper == "STOP_LIMIT":
                if not price or not stop_price:
                    raise ValueError("STOP_LIMIT requires both --price and --stop_price")
                params.update({
                    "type": "STOP",  # 'STOP' in Binance Futures executes as a Stop-Limit
                    "price": str(price),
                    "stopPrice": str(stop_price),
                    "timeInForce": "GTC"
                })

            elif order_type_upper == "STOP_MARKET":
                if not stop_price:
                    raise ValueError("STOP_MARKET requires a --stop_price")
                params.update({
                    "type": "STOP_MARKET",
                    "stopPrice": str(stop_price)
                })
            
            else:
                raise ValueError(f"Unsupported order type: {order_type}")

            logger.info(f"Attempting {side} {order_type_upper} for {qty} {symbol}")
            response = self.client.futures_create_order(**params)
            return response

        except Exception as e:
            logger.error(f"Binance API Error: {e}")
            raise
from .logging_config import logger
from binance.exceptions import BinanceAPIException
 
def place_order(client, symbol, side, order_type, quantity, price=None, stop_price=None):
    try:
        # Binance Futures uses 'STOP' as the API type for Stop-Limit orders
        api_order_type = 'STOP' if order_type.upper() == 'STOP_LIMIT' else order_type.upper()
 
        params = {
            'symbol': symbol.upper(),
            'side': side.upper(),
            'type': api_order_type,
            'quantity': f"{quantity:f}",  # Format to avoid scientific notation
        }
 
        if order_type.upper() == 'LIMIT':
            params['price'] = f"{price:f}"
            params['timeInForce'] = 'GTC'
        elif order_type.upper() == 'STOP_MARKET':
            params['stopPrice'] = f"{stop_price:f}"
        elif order_type.upper() == 'STOP_LIMIT':
            params['price'] = f"{price:f}"
            params['stopPrice'] = f"{stop_price:f}"
            params['timeInForce'] = 'GTC'
 
        logger.info(f"Attempting {side} {order_type} for {quantity} {symbol}")
 
        response = client.futures_create_order(**params)
 
        logger.info(
            f"Success! Order ID: {response.get('orderId')} | "
            f"Status: {response.get('status')} | "
            f"Executed Qty: {response.get('executedQty')} | "
            f"Avg Price: {response.get('avgPrice')}"
        )
        return response
 
    except BinanceAPIException as e:
        logger.error(f"Binance API Error: {e.message}")
        return None
    except Exception as e:
        logger.error(f"Unexpected Error: {str(e)}")
        return None
 
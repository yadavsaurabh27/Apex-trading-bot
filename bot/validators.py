def validate_inputs(symbol, side, order_type, quantity, price):
    if side.upper() not in ['BUY', 'SELL']:
        raise ValueError("Side must be BUY or SELL.")
    if order_type.upper() not in ['MARKET', 'LIMIT', 'STOP_LIMIT', 'STOP_MARKET']:
        raise ValueError("Order type must be MARKET, LIMIT, STOP_LIMIT, or STOP_MARKET.")
    if order_type.upper() in ['LIMIT', 'STOP_LIMIT'] and not price:
        raise ValueError(f"Price (--price) is required for {order_type} orders.")
    if price is not None and float(price) <= 0:
        raise ValueError("Price must be a positive number.")
    if float(quantity) <= 0:
        raise ValueError("Quantity must be a positive number.")
    return True
import argparse
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from bot.client import BinanceFuturesClient
from bot.orders import place_order
from bot.validators import validate_inputs
from bot.logging_config import logger
 
console = Console()
 
 
def display_summary(symbol, side, order_type, qty, price, stop_price):
    table = Table(title="🚀 Apex Trading Bot | Order Preview", title_style="bold cyan")
    table.add_column("Parameter", style="magenta")
    table.add_column("Value", style="green")
    table.add_row("Symbol", symbol.upper())
    table.add_row("Action", side.upper())
    table.add_row("Execution Type", order_type.upper())
    table.add_row("Quantity", str(qty))
    if price:
        table.add_row("Limit Price", f"${price}")
    if stop_price:
        table.add_row("Stop Trigger", f"${stop_price}")
    console.print(table)
 
 
def main():
    parser = argparse.ArgumentParser(description="Apex Trading Bot CLI")
    parser.add_argument("--symbol", required=True, help="Trading pair (e.g. BTCUSDT)")
    parser.add_argument("--side", choices=["BUY", "SELL"], required=True)
    parser.add_argument("--type", choices=["MARKET", "LIMIT", "STOP_LIMIT", "STOP_MARKET"], required=True)
    parser.add_argument("--qty", type=float, required=True)
    parser.add_argument("--price", type=float, help="Limit price (required for LIMIT and STOP_LIMIT)")
    parser.add_argument("--stop_price", type=float, help="Trigger price (required for STOP_LIMIT and STOP_MARKET)")
 
    args = parser.parse_args()
 
    # Validate inputs
    try:
        validate_inputs(args.symbol, args.side, args.type, args.qty, args.price)
    except ValueError as e:
        console.print(Panel(f"[bold red]❌ Validation Error[/bold red]\n[white]{str(e)}[/white]",
                            title="Input Error", border_style="red"))
        sys.exit(1)
 
    display_summary(args.symbol, args.side, args.type, args.qty, args.price, args.stop_price)
 
    try:
        bot_client = BinanceFuturesClient()
 
        res = place_order(
            bot_client.client,
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.qty,
            price=args.price,
            stop_price=args.stop_price
        )
 
        if res:
            order_id = res.get('orderId', 'N/A')
            status = res.get('status', 'N/A')
            exec_qty = res.get('executedQty', '0')
            avg_price = res.get('avgPrice', '0.0')
 
            # Only show avg price if it's a filled market order
            if float(avg_price) > 0:
                price_line = f"Avg Price: ${avg_price}"
            elif args.type == 'MARKET':
                price_line = "Avg Price: Pending fill (testnet lag)"
            else:
                price_line = "Avg Price: N/A (Order Open)"
 
            console.print(Panel(
                f"[bold green]✅ SUCCESS[/bold green]\n"
                f"Order ID: [yellow]{order_id}[/yellow]\n"
                f"Status: {status}\n"
                f"Executed Qty: {exec_qty}\n"
                f"{price_line}",
                title="Binance Response",
                border_style="green"
            ))
        else:
            console.print(Panel(
                "[bold red]❌ FAILED[/bold red]\nSee trading_bot.log for details.",
                title="Order Failed",
                border_style="red"
            ))
            sys.exit(1)
 
    except Exception as e:
        console.print(Panel(
            f"[bold red]❌ FAILED[/bold red]\n[white]{str(e)}[/white]",
            title="Error Details",
            border_style="red"
        ))
        sys.exit(1)
 
 
if __name__ == "__main__":
    main()
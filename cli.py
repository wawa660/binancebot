import argparse
import sys
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    ValidationError,
)
from bot.client import BinanceClient
from bot.orders import place_order, OrderError
from bot.logging_config import setup_logging

logger = setup_logging()


def main():
    parser = argparse.ArgumentParser(description="Binance Futures Trading Bot")
    parser.add_argument(
        "--symbol", required=True, help="Trading symbol (e.g., BTCUSDT)"
    )
    parser.add_argument("--side", required=True, help="Order side: BUY or SELL")
    parser.add_argument(
        "--type", dest="order_type", required=True, help="Order type: MARKET or LIMIT"
    )
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", help="Order price (required for LIMIT orders)")
    parser.add_argument(
        "--api-key", help="Binance API key (optional, uses .env if not provided)"
    )
    parser.add_argument(
        "--secret-key", help="Binance secret key (optional, uses .env if not provided)"
    )

    args = parser.parse_args()

    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price, order_type)

        print(f"\n{'=' * 50}")
        print(f"ORDER REQUEST SUMMARY")
        print(f"{'=' * 50}")
        print(f"Symbol:     {symbol}")
        print(f"Side:       {side}")
        print(f"Order Type: {order_type}")
        print(f"Quantity:   {quantity}")
        if price:
            print(f"Price:      {price}")
        print(f"{'=' * 50}\n")

        client = BinanceClient(api_key=args.api_key, secret_key=args.secret_key)

        logger.info(
            f"Placing order: {symbol} {side} {order_type} {quantity} @ {price or 'MARKET'}"
        )

        response = place_order(client, symbol, side, order_type, quantity, price)

        print(f"ORDER RESPONSE")
        print(f"{'=' * 50}")
        print(f"Order ID:       {response.get('orderId')}")
        print(f"Status:         {response.get('status')}")
        print(f"Symbol:         {response.get('symbol')}")
        print(f"Side:           {response.get('side')}")
        print(f"Type:           {response.get('type')}")
        print(f"Quantity:       {response.get('origQty')}")
        if response.get("avgPrice"):
            print(f"Avg Price:      {response.get('avgPrice')}")
        if response.get("executedQty"):
            print(f"Executed Qty:   {response.get('executedQty')}")
        if response.get("price"):
            print(f"Price:          {response.get('price')}")
        print(f"{'=' * 50}\n")

        print(f"SUCCESS: Order placed successfully!")

    except ValidationError as e:
        print(f"\nVALIDATION ERROR: {e}")
        logger.error(f"Validation error: {e}")
        sys.exit(1)
    except OrderError as e:
        print(f"\nORDER ERROR: {e}")
        logger.error(f"Order error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\nCONFIGURATION ERROR: {e}")
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {e}")
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

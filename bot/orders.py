from binance.client import Client
from binance.exceptions import BinanceAPIException
from typing import Optional
from bot.logging_config import setup_logging
from bot.client import BinanceClient

logger = setup_logging()


class OrderError(Exception):
    pass


def place_market_order(
    client: BinanceClient, symbol: str, side: str, quantity: float
) -> dict:
    try:
        logger.info(
            f"Placing MARKET order - Symbol: {symbol}, Side: {side}, Quantity: {quantity}"
        )
        order = client.client.futures_create_order(
            symbol=symbol,
            side=side,
            type=Client.FUTURE_ORDER_TYPE_MARKET,
            quantity=quantity,
        )
        logger.info(f"Market order response: {order}")
        return order
    except BinanceAPIException as e:
        logger.error(f"Binance API error placing market order: {e}")
        raise OrderError(f"API Error: {e}")
    except Exception as e:
        logger.error(f"Error placing market order: {e}")
        raise OrderError(f"Error: {e}")


def place_limit_order(
    client: BinanceClient, symbol: str, side: str, quantity: float, price: float
) -> dict:
    try:
        logger.info(
            f"Placing LIMIT order - Symbol: {symbol}, Side: {side}, Quantity: {quantity}, Price: {price}"
        )
        order = client.client.futures_create_order(
            symbol=symbol,
            side=side,
            type=Client.FUTURE_ORDER_TYPE_LIMIT,
            quantity=quantity,
            price=price,
            timeInForce=Client.FUTURE_ORDER_TIME_IN_FORCE_GTC,
        )
        logger.info(f"Limit order response: {order}")
        return order
    except BinanceAPIException as e:
        logger.error(f"Binance API error placing limit order: {e}")
        raise OrderError(f"API Error: {e}")
    except Exception as e:
        logger.error(f"Error placing limit order: {e}")
        raise OrderError(f"Error: {e}")


def place_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
) -> dict:
    if order_type == "MARKET":
        return place_market_order(client, symbol, side, quantity)
    elif order_type == "LIMIT":
        if price is None:
            raise OrderError("Price is required for LIMIT orders")
        return place_limit_order(client, symbol, side, quantity, price)
    else:
        raise OrderError(f"Unsupported order type: {order_type}")

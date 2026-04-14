import re
from typing import Optional


class ValidationError(Exception):
    pass


def validate_symbol(symbol: str) -> str:
    if not symbol:
        raise ValidationError("Symbol cannot be empty")
    symbol = symbol.upper().strip()
    if not re.match(r"^[A-Z0-9]+$", symbol):
        raise ValidationError("Invalid symbol format. Use e.g., BTCUSDT")
    return symbol


def validate_side(side: str) -> str:
    if not side:
        raise ValidationError("Side cannot be empty")
    side = side.upper().strip()
    if side not in ("BUY", "SELL"):
        raise ValidationError("Side must be BUY or SELL")
    return side


def validate_order_type(order_type: str) -> str:
    if not order_type:
        raise ValidationError("Order type cannot be empty")
    order_type = order_type.upper().strip()
    if order_type not in ("MARKET", "LIMIT"):
        raise ValidationError("Order type must be MARKET or LIMIT")
    return order_type


def validate_quantity(quantity: str) -> float:
    if not quantity:
        raise ValidationError("Quantity cannot be empty")
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValidationError("Quantity must be positive")
        return qty
    except ValueError:
        raise ValidationError("Invalid quantity format")


def validate_price(price: Optional[str], order_type: str) -> Optional[float]:
    if order_type == "MARKET":
        return None
    if not price:
        raise ValidationError("Price is required for LIMIT orders")
    try:
        prc = float(price)
        if prc <= 0:
            raise ValidationError("Price must be positive")
        return prc
    except ValueError:
        raise ValidationError("Invalid price format")

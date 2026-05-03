# bot/validators.py

from bot.logging_config import setup_logger

logger = setup_logger("validators")

VALID_SIDES = ["BUY", "SELL"]
VALID_ORDER_TYPES = ["MARKET", "LIMIT", "STOP_LIMIT"]


def validate_inputs(symbol: str, side: str, order_type: str,
                    quantity: float, price: float = None,
                    stop_price: float = None) -> None:
    """
    Validates all user inputs before sending anything to Binance.
    Raises ValueError with a clear message if anything is wrong.
    """

    # 1. Symbol must not be empty
    if not symbol or not symbol.strip():
        raise ValueError("Symbol cannot be empty. Example: BTCUSDT")

    # 2. Symbol must be letters only
    if not symbol.isalpha():
        raise ValueError(f"Invalid symbol '{symbol}'. Use letters only. Example: BTCUSDT")

    # 3. Side must be BUY or SELL
    if side.upper() not in VALID_SIDES:
        raise ValueError(f"Invalid side '{side}'. Must be BUY or SELL.")

    # 4. Order type must be MARKET, LIMIT or STOP_LIMIT
    if order_type.upper() not in VALID_ORDER_TYPES:
        raise ValueError(
            f"Invalid order type '{order_type}'. "
            f"Must be MARKET, LIMIT or STOP_LIMIT."
        )

    # 5. Quantity must be positive
    if quantity <= 0:
        raise ValueError(f"Quantity must be greater than 0. Got: {quantity}")

    # 6. LIMIT orders must have a price
    if order_type.upper() == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders. Use --price.")
        if price <= 0:
            raise ValueError(f"Price must be greater than 0. Got: {price}")

    # 7. STOP_LIMIT orders must have BOTH price and stop_price
    if order_type.upper() == "STOP_LIMIT":
        if price is None:
            raise ValueError("Price is required for STOP_LIMIT orders. Use --price.")
        if stop_price is None:
            raise ValueError("Stop price is required for STOP_LIMIT orders. Use --stop-price.")
        if price <= 0:
            raise ValueError(f"Price must be greater than 0. Got: {price}")
        if stop_price <= 0:
            raise ValueError(f"Stop price must be greater than 0. Got: {stop_price}")

    logger.info(
        f"Validation passed: symbol={symbol.upper()}, side={side.upper()}, "
        f"type={order_type.upper()}, qty={quantity}, "
        f"price={price}, stop_price={stop_price}"
    )
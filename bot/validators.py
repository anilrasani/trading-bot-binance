# bot/validators.py

from bot.logging_config import setup_logger

logger = setup_logger("validators")

# These are the only valid values we accept
VALID_SIDES = ["BUY", "SELL"]
VALID_ORDER_TYPES = ["MARKET", "LIMIT"]


def validate_inputs(symbol: str, side: str, order_type: str,
                    quantity: float, price: float = None) -> None:
    """
    Validates all user inputs before sending anything to Binance.
    Raises ValueError with a clear message if anything is wrong.
    """

    # 1. Symbol must not be empty
    if not symbol or not symbol.strip():
        raise ValueError("Symbol cannot be empty. Example: BTCUSDT")

    # 2. Symbol must be uppercase letters only
    if not symbol.isalpha():
        raise ValueError(f"Invalid symbol '{symbol}'. Use letters only. Example: BTCUSDT")

    # 3. Side must be BUY or SELL
    if side.upper() not in VALID_SIDES:
        raise ValueError(f"Invalid side '{side}'. Must be BUY or SELL.")

    # 4. Order type must be MARKET or LIMIT
    if order_type.upper() not in VALID_ORDER_TYPES:
        raise ValueError(f"Invalid order type '{order_type}'. Must be MARKET or LIMIT.")

    # 5. Quantity must be a positive number
    if quantity <= 0:
        raise ValueError(f"Quantity must be greater than 0. Got: {quantity}")

    # 6. LIMIT orders MUST have a price
    if order_type.upper() == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders. Use --price.")
        if price <= 0:
            raise ValueError(f"Price must be greater than 0. Got: {price}")

    logger.info(
        f"Validation passed: symbol={symbol.upper()}, side={side.upper()}, "
        f"type={order_type.upper()}, qty={quantity}, price={price}"
    )
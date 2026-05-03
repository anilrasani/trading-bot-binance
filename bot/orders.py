# bot/orders.py

from binance.exceptions import BinanceAPIException, BinanceRequestException
from bot.logging_config import setup_logger

logger = setup_logger("orders")


def place_order(client, symbol: str, side: str, order_type: str,
                quantity: float, price: float = None,
                stop_price: float = None) -> dict:
    """
    Places a MARKET, LIMIT or STOP_LIMIT order on Binance Futures Testnet.

    Args:
        client     : raw Binance client from BinanceClient.get_client()
        symbol     : e.g. "BTCUSDT"
        side       : "BUY" or "SELL"
        order_type : "MARKET", "LIMIT" or "STOP_LIMIT"
        quantity   : how much to buy/sell
        price      : required for LIMIT and STOP_LIMIT
        stop_price : required for STOP_LIMIT (the trigger price)

    Returns:
        dict: the full response from Binance
    """

    symbol     = symbol.upper()
    side       = side.upper()
    order_type = order_type.upper()

    # --- Build the request payload ---
    params = {
        "symbol"  : symbol,
        "side"    : side,
        "quantity": quantity,
    }

    if order_type == "MARKET":
        params["type"] = "MARKET"

    elif order_type == "LIMIT":
        params["type"]        = "LIMIT"
        params["price"]       = price
        params["timeInForce"] = "GTC"

    elif order_type == "STOP_LIMIT":
        # Binance API name for Stop-Limit is STOP
        params["type"]        = "STOP"
        params["price"]       = price
        params["stopPrice"]   = stop_price
        params["timeInForce"] = "GTC"

    # --- Log what we are about to send ---
    logger.info(f"Placing order → {params}")

    # --- Print clean summary for the user ---
    print("\n" + "="*45)
    print("         📋 ORDER REQUEST SUMMARY")
    print("="*45)
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Type       : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price:
        print(f"  Price      : {price}")
    if stop_price:
        print(f"  Stop Price : {stop_price}")
    print("="*45)

    try:
        # --- Send order to Binance ---
        response = client.futures_create_order(**params)

        # --- Log the full response ---
        logger.info(f"Order response → {response}")

        # --- Print clean response for the user ---
        print("\n" + "="*45)
        print("         ✅ ORDER PLACED SUCCESSFULLY!")
        print("="*45)
        print(f"  Order ID     : {response.get('orderId')}")
        print(f"  Status       : {response.get('status')}")
        print(f"  Executed Qty : {response.get('executedQty')}")
        avg_price = response.get('avgPrice') or response.get('price', 'N/A')
        print(f"  Avg Price    : {avg_price}")
        if response.get('stopPrice'):
            print(f"  Stop Price   : {response.get('stopPrice')}")
        print("="*45 + "\n")

        return response

    except BinanceAPIException as e:
        logger.error(f"BinanceAPIException: code={e.status_code}, message={e.message}")
        print(f"\n❌ Binance API Error: {e.message}")
        raise

    except BinanceRequestException as e:
        logger.error(f"BinanceRequestException (network issue): {e}")
        print(f"\n❌ Network Error: {e}")
        raise

    except Exception as e:
        logger.error(f"Unexpected error while placing order: {e}")
        print(f"\n❌ Unexpected Error: {e}")
        raise
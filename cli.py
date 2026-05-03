# cli.py

import argparse
import sys
from bot.client import BinanceClient
from bot.validators import validate_inputs
from bot.orders import place_order
from bot.logging_config import setup_logger

logger = setup_logger("cli")


def main():
    # --- Define all CLI arguments ---
    parser = argparse.ArgumentParser(
        description="🤖 Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "--symbol",
        required=True,
        help="Trading pair. Example: BTCUSDT"
    )
    parser.add_argument(
        "--side",
        required=True,
        help="BUY or SELL"
    )
    parser.add_argument(
        "--type",
        required=True,
        dest="order_type",
        help="MARKET or LIMIT"
    )
    parser.add_argument(
        "--qty",
        required=True,
        type=float,
        help="Quantity to trade. Example: 0.001"
    )
    parser.add_argument(
        "--price",
        required=False,
        type=float,
        help="Price (only required for LIMIT orders)"
    )
    parser.add_argument(
        "--test-connection",
        action="store_true",
        help="Test API connection and exit"
    )

    args = parser.parse_args()

    logger.info(
        f"CLI called → symbol={args.symbol}, side={args.side}, "
        f"type={args.order_type}, qty={args.qty}, price={args.price}"
    )

    try:
        # Step 1: Connect to Binance
        print("\n🔌 Connecting to Binance Futures Testnet...")
        binance = BinanceClient()
        client  = binance.get_client()

        # Step 2: If user just wants to test connection
        if args.test_connection:
            binance.test_connection()
            return

        # Step 3: Validate inputs
        print("🔍 Validating your inputs...")
        validate_inputs(
            symbol     = args.symbol,
            side       = args.side,
            order_type = args.order_type,
            quantity   = args.qty,
            price      = args.price
        )

        # Step 4: Place the order
        place_order(
            client     = client,
            symbol     = args.symbol,
            side       = args.side,
            order_type = args.order_type,
            quantity   = args.qty,
            price      = args.price
        )

    except ValueError as e:
        # Validation errors — bad input from user
        logger.warning(f"Validation error: {e}")
        print(f"\n⚠️  Input Error: {e}")
        sys.exit(1)

    except Exception as e:
        # Everything else — already logged inside the function that raised it
        sys.exit(1)


if __name__ == "__main__":
    main()
    
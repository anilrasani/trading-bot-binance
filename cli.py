# cli.py

import argparse
import sys
from bot.client import BinanceClient
from bot.validators import validate_inputs
from bot.orders import place_order
from bot.logging_config import setup_logger

logger = setup_logger("cli")


def main():
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
        help="MARKET, LIMIT or STOP_LIMIT"
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
        help="Limit price (required for LIMIT and STOP_LIMIT)"
    )
    parser.add_argument(
        "--stop-price",
        required=False,
        type=float,
        dest="stop_price",
        help="Stop trigger price (required for STOP_LIMIT)"
    )
    parser.add_argument(
        "--test-connection",
        action="store_true",
        help="Test API connection and exit"
    )

    args = parser.parse_args()

    logger.info(
        f"CLI called → symbol={args.symbol}, side={args.side}, "
        f"type={args.order_type}, qty={args.qty}, "
        f"price={args.price}, stop_price={args.stop_price}"
    )

    try:
        # Step 1: Connect to Binance
        print("\n🔌 Connecting to Binance Futures Testnet...")
        binance = BinanceClient()
        client  = binance.get_client()

        # Step 2: Test connection only
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
            price      = args.price,
            stop_price = args.stop_price
        )

        # Step 4: Place the order
        place_order(
            client     = client,
            symbol     = args.symbol,
            side       = args.side,
            order_type = args.order_type,
            quantity   = args.qty,
            price      = args.price,
            stop_price = args.stop_price
        )

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        print(f"\n⚠️  Input Error: {e}")
        sys.exit(1)

    except Exception as e:
        sys.exit(1)


if __name__ == "__main__":
    main()
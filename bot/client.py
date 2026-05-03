# bot/client.py

import os
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException
from bot.logging_config import setup_logger

# Load the .env file so os.getenv() can read your keys
load_dotenv()

logger = setup_logger("client")


class BinanceClient:
    """
    A wrapper around the python-binance Client.
    Handles connection to the Binance Futures Testnet.
    """

    def __init__(self):
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            logger.error("API keys not found. Check your .env file.")
            raise ValueError("Missing BINANCE_API_KEY or BINANCE_API_SECRET in .env")

        # Connect to Testnet
        self.client = Client(
            api_key=api_key,
            api_secret=api_secret,
            testnet=True
        )

        # Override the futures base URL to point to correct testnet
        self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

        logger.info("BinanceClient initialized. Connected to Futures Testnet.")

    def get_client(self) -> Client:
        """Returns the raw Binance client for use in other modules."""
        return self.client

    def test_connection(self):
        """
        Pings the Binance server to confirm connection works.
        Run this once to make sure your keys and URL are correct.
        """
        try:
            self.client.futures_ping()
            logger.info("Connection test passed. Binance Futures Testnet is reachable.")
            print("\n✅ Connected to Binance Futures Testnet successfully!")
            return True
        except BinanceAPIException as e:
            logger.error(f"Connection test failed: {e}")
            print(f"\n❌ Connection failed: {e}")
            return False
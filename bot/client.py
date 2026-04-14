from binance.client import Client
from binance.exceptions import BinanceAPIException
import os
from dotenv import load_dotenv
from typing import Optional
from bot.logging_config import setup_logging

load_dotenv()

logger = setup_logging()

TESTNET_URL = "https://testnet.binancefuture.com"


class BinanceClient:
    def __init__(self, api_key: Optional[str] = None, secret_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.secret_key = secret_key or os.getenv("BINANCE_SECRET_KEY")

        if not self.api_key or not self.secret_key:
            raise ValueError("API key and secret key are required")

        self.client = Client(self.api_key, self.secret_key, testnet=True)
        self.client.FUTURES_URL = TESTNET_URL
        logger.info("Binance client initialized for testnet")

    def get_balance(self) -> dict:
        try:
            account = self.client.futures_account()
            logger.info(f"Retrieved account balance: {account}")
            return account
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching balance: {e}")
            raise

    def get_symbol_price(self, symbol: str) -> float:
        try:
            price = self.client.futures_symbol_ticker(symbol=symbol)
            logger.info(f"Retrieved price for {symbol}: {price}")
            return float(price["price"])
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching price: {e}")
            raise

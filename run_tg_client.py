import logging
import sys

from bot import start_telegram_client

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    start_telegram_client()

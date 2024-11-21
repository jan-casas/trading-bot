from loguru import logger
from config.config import LOG_FILE

logger.add(LOG_FILE, rotation="500 MB")

def log_trade(action, symbol, quantity, price):
    logger.info(f"{action.upper()} | Symbol: {symbol} | Quantity: {quantity} | Price: {price}")

def log_error(error_message):
    logger.error(error_message)

def log_info(message):
    logger.info(message)

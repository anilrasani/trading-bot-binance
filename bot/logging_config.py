# bot/logging_config.py

import logging
import os

def setup_logger(name: str) -> logging.Logger:
    """
    Creates a logger that writes to both the terminal AND a log file.
    Every module calls this function to get its own named logger.
    """

    # Create a 'logs' folder if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid adding duplicate handlers if logger is reused
    if logger.handlers:
        return logger

    # --- File handler: writes to logs/trading_bot.log ---
    file_handler = logging.FileHandler("logs/trading_bot.log")
    file_handler.setLevel(logging.DEBUG)

    # --- Console handler: prints to terminal ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Format: timestamp | level | module | message
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
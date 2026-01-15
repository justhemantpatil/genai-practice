import logging
import os

def get_app_logger():
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler("logs/app_trace.log")
        formatter = logging.Formatter(
            "%(asctime)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

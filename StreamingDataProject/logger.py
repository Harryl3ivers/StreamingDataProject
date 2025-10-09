# logger.py
import logging

def get_logger(name=__name__, level=logging.INFO):
    """
    Returns a configured logger.
    Works both locally (prints to console) and on AWS Lambda (CloudWatch).
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Add console handler if not already added
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

import logging

logging.basicConfig(
    filename="trades.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def log_trade(msg):
    logging.info(msg)
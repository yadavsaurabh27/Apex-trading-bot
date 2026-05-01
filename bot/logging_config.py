import logging

def setup_logger():
    logger = logging.getLogger("TradingBot")
    logger.setLevel(logging.INFO)
    
    # Required log file for submission
    fh = logging.FileHandler("trading_bot.log")
    # Console output for real-time tracking
    sh = logging.StreamHandler()
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger

logger = setup_logger()
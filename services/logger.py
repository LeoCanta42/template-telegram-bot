# services/logger.py
import logging

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': "\033[94m",    # Blue
        'INFO': "\033[92m",     # Green
        'WARNING': "\033[93m",  # Yellow
        'ERROR': "\033[91m",    # Red
        'CRITICAL': "\033[95m", # Magenta
        'RESET': "\033[0m"
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        record.levelname = f"{color}{record.levelname}{reset}"
        record.name = f"{color}{record.name}{reset}"
        return super().format(record)

def setup_logger(name="telegram_bot"):
    logger = logging.getLogger(name)
    # logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)  # Set to DEBUG for detailed logs

    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        # handler.setLevel(logging.INFO)
        handler.setLevel(logging.DEBUG)
        formatter = ColoredFormatter("[%(asctime)s] %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

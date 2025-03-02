"""Module to create a colorful logger."""
import logging


class ColorfulFormatter(logging.Formatter):
    """Colorful log formatter."""

    # Define ANSI color codes for log levels
    COLORS = {
        logging.DEBUG: "\033[94m",  # Blue
        logging.INFO: "\033[97m",  # White
        logging.WARNING: "\033[93m",  # Yellow
        logging.ERROR: "\033[91m",  # Red
        logging.CRITICAL: "\033[95m",  # Magenta
    }
    RESET = "\033[0m"  # Reset to default

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record."""
        log_color = self.COLORS.get(record.levelno, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"  # Colorize level name
        record.msg = f"{log_color}{record.msg}{self.RESET}"  # Colorize message
        return super().format(record)


logger = logging.getLogger("colorful_logger")
logger.setLevel(logging.DEBUG)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

format = r"%(asctime)s - %(levelname)-7s %(threadName)-12s [%(filename)s:%(lineno)s - %(funcName)s()] - %(message)s"

# Set the formatter
formatter = ColorfulFormatter(format, datefmt="%Y-%m-%d %H:%M:%S")  # Customize format here
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)

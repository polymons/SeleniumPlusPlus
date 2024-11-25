import logging
import logging.handlers
import os
from typing import Optional, Union
from pathlib import Path

"""
Example usage:

from seleniumplusplus.logger import setup_logger, set_log_level, info, error

# Custom setup if needed
logger = setup_logger(
    log_file='selenium.log',
    level=logging.DEBUG,
    log_dir='logs',
    log_format='[%(asctime)s] %(levelname)s: %(message)s'
)

# Or use default logger
info("Starting selenium automation")
error("Something went wrong", exc_info=True)

# Adjust log level as needed
set_log_level("DEBUG") """



def setup_logger(
    log_file: str = 'test.log',
    level: int = logging.INFO,
    max_bytes: int = 5_000_000,  # 5MB
    backup_count: int = 3,
    log_format: Optional[str] = None,
    log_dir: Optional[str] = None
) -> logging.Logger:
    """
    Configure and return a logger with both console and rotating file handlers.
    
    :param log_file: Name of the log file
    :param level: Logging level (default: INFO)
    :param max_bytes: Max size of each log file before rotation
    :param backup_count: Number of backup files to keep
    :param log_format: Custom log format string
    :param log_dir: Directory for log files (default: current directory)
    :return: Configured logger instance
    """
    logger = logging.getLogger()
    logger.setLevel(level)

    # Clear any existing handlers
    logger.handlers.clear()

    # Create log directory if specified
    if log_dir:
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        log_file = str(log_path / log_file)

    # Define formatters
    simple_formatter = logging.Formatter('%(message)s')
    detailed_formatter = logging.Formatter(
        log_format or '[%(asctime)s] %(levelname)s [%(name)s] %(message)s'
    )

    # Console handler (simple format for readability)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)

    # Rotating file handler (detailed format for debugging)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        mode='a',
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)

    def handle_exception(exc_type, exc_value, exc_traceback):
        """Handle uncaught exceptions by logging them"""
        if issubclass(exc_type, KeyboardInterrupt):
            # Call the default handler for KeyboardInterrupt
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    # Set the exception hook
    import sys
    sys.excepthook = handle_exception

    return logger

# Initialize default logger
logger = setup_logger()

# Override print for legacy compatibility
print = logger.info

# Export commonly used logging functions
debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical

def set_log_level(level: Union[str, int]) -> None:
    """
    Set the logging level for all handlers.
    
    :param level: Logging level (can be string name or integer level)
    """
    if isinstance(level, str):
        level = getattr(logging, level.upper())
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)
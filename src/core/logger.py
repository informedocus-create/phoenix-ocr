"""
Logging configuration utility supporting console and per-stage file handlers.
"""

import logging
import sys
from pathlib import Path

from src.core.settings import LOG_FORMAT, LOG_DATE_FORMAT, DEFAULT_LOG_LEVEL


def setup_logger(
    name: str = "phoenix_ocr",
    log_file: Path | None = None,
    level: int = DEFAULT_LOG_LEVEL,
) -> logging.Logger:
    """Configures and returns a logger instance with console and optional file logging handlers.

    Args:
        name: Name of the logger instance.
        log_file: Optional path to a file where log messages should be written.
        level: Minimum logging level (e.g., logging.INFO).

    Returns:
        Configured logging.Logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding duplicate handlers if logger was previously setup
    if logger.handlers:
        logger.handlers.clear()

    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler (if log_file specified)
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

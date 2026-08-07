"""
Core module: Configuration settings, logging, and custom exception handling.
"""

from src.core.settings import *  # noqa: F403
from src.core.logger import setup_logger
from src.core.exceptions import PhoenixOCRError, PDFRenderingError, InvalidPDFError

__all__ = [
    "setup_logger",
    "PhoenixOCRError",
    "PDFRenderingError",
    "InvalidPDFError",
]

"""
Global configuration settings and constants for Phoenix OCR.
"""

from pathlib import Path
import logging

# Directory paths
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent
DEFAULT_INPUT_DIR: Path = PROJECT_ROOT / "input"
DEFAULT_OUTPUT_DIR: Path = PROJECT_ROOT / "output"

# Rendering settings
DEFAULT_DPI: int = 300
PAGE_IMAGE_FORMAT: str = "png"
PAGE_FILENAME_PATTERN: str = "page_{page_num:04d}.png"
DEFAULT_RENDER_ENGINE: str = "PyMuPDF"

# Logging configuration
LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
DEFAULT_LOG_LEVEL: int = logging.INFO

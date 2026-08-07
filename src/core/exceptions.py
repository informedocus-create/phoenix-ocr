"""
Custom exception classes for Phoenix OCR.
"""


class PhoenixOCRError(Exception):
    """Base exception class for all Phoenix OCR errors."""

    pass


class PDFRenderingError(PhoenixOCRError):
    """Raised when an error occurs during PDF page rendering."""

    pass


class InvalidPDFError(PDFRenderingError):
    """Raised when a file is missing, unreadable, or not a valid PDF document."""

    pass

"""
PDF module: Renderer interface, PyMuPDF implementation, and data models.
"""

from src.pdf.interface import BasePDFRenderer
from src.pdf.models import RenderResult, PDFMetadata
from src.pdf.renderer import PyMuPDFRenderer

__all__ = [
    "BasePDFRenderer",
    "RenderResult",
    "PDFMetadata",
    "PyMuPDFRenderer",
]

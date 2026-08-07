"""
Abstract interface definition for PDF rendering engine implementations.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from src.core.settings import DEFAULT_DPI
from src.pdf.models import RenderResult, PDFMetadata


class BasePDFRenderer(ABC):
    """Abstract Base Class defining the contract for PDF page rendering engines."""

    @abstractmethod
    def is_valid_pdf(self, pdf_path: Path) -> bool:
        """Checks whether the specified file path exists and is a valid readable PDF.

        Args:
            pdf_path: Path to the candidate PDF file.

        Returns:
            True if file is a readable PDF, False otherwise.
        """
        pass

    @abstractmethod
    def get_page_count(self, pdf_path: Path) -> int:
        """Returns the total number of pages in the PDF document.

        Args:
            pdf_path: Path to the target PDF file.

        Returns:
            Number of pages.
        """
        pass

    @abstractmethod
    def get_metadata(self, pdf_path: Path) -> PDFMetadata:
        """Extracts document metadata properties from the PDF.

        Args:
            pdf_path: Path to the target PDF file.

        Returns:
            PDFMetadata dataclass instance.
        """
        pass

    @abstractmethod
    def render(
        self,
        pdf_path: Path,
        output_pages_dir: Path,
        dpi: int = DEFAULT_DPI,
        doc_id: str | None = None,
    ) -> RenderResult:
        """Renders every page of the PDF as high-resolution images into the target directory.

        Args:
            pdf_path: Path to the source PDF file.
            output_pages_dir: Path to directory where rendered page images will be saved.
            dpi: Target Resolution (dots per inch).
            doc_id: Unique pipeline identifier for tracking.

        Returns:
            RenderResult containing execution status, output paths, and benchmark metrics.
        """
        pass

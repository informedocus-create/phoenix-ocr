"""
PyMuPDF (fitz) implementation of the BasePDFRenderer interface.
"""

import time
import uuid
from pathlib import Path
import pymupdf as fitz

from src.core.settings import (
    DEFAULT_DPI,
    PAGE_FILENAME_PATTERN,
    DEFAULT_RENDER_ENGINE,
)
from src.core.exceptions import InvalidPDFError, PDFRenderingError
from src.core.logger import setup_logger
from src.pdf.interface import BasePDFRenderer
from src.pdf.models import RenderResult, PDFMetadata

logger = setup_logger("phoenix_ocr.pdf_renderer")


class PyMuPDFRenderer(BasePDFRenderer):
    """PDF rendering engine powered by PyMuPDF (fitz)."""

    def is_valid_pdf(self, pdf_path: Path) -> bool:
        """Checks whether the file exists and can be opened as a valid PDF document."""
        pdf_path = Path(pdf_path)
        if not pdf_path.is_file():
            return False

        try:
            doc = fitz.open(str(pdf_path))
            is_valid = bool(doc.is_pdf) and not doc.is_encrypted
            doc.close()
            return is_valid
        except Exception:
            return False



    def get_page_count(self, pdf_path: Path) -> int:
        """Returns the total number of pages in the PDF document."""
        pdf_path = Path(pdf_path)
        if not self.is_valid_pdf(pdf_path):
            raise InvalidPDFError(f"File is not a valid PDF: '{pdf_path}'")

        try:
            doc = fitz.open(str(pdf_path))
            count = len(doc)
            doc.close()
            return count
        except Exception as e:
            raise PDFRenderingError(
                f"Failed to retrieve page count for '{pdf_path}': {e}"
            ) from e

    def get_metadata(self, pdf_path: Path) -> PDFMetadata:
        """Extracts metadata properties from the PDF document."""
        pdf_path = Path(pdf_path)
        if not self.is_valid_pdf(pdf_path):
            raise InvalidPDFError(f"File is not a valid PDF: '{pdf_path}'")

        try:
            doc = fitz.open(str(pdf_path))
            meta = doc.metadata or {}
            page_count = len(doc)
            doc.close()

            return PDFMetadata(
                page_count=page_count,
                title=meta.get("title", ""),
                author=meta.get("author", ""),
                creator=meta.get("creator", ""),
                producer=meta.get("producer", ""),
                creation_date=meta.get("creationDate", ""),
            )
        except Exception as e:
            raise PDFRenderingError(
                f"Failed to read metadata for '{pdf_path}': {e}"
            ) from e

    def render(
        self,
        pdf_path: Path,
        output_pages_dir: Path,
        dpi: int = DEFAULT_DPI,
        doc_id: str | None = None,
    ) -> RenderResult:
        """Renders all PDF pages to high-resolution PNG images in output_pages_dir.

        Args:
            pdf_path: Path to input PDF document.
            output_pages_dir: Target directory to save rendered page images.
            dpi: Resolution in dots per inch (default: 300).
            doc_id: Optional document UUID string.

        Returns:
            RenderResult containing execution benchmark statistics and rendered page file paths.
        """
        pdf_path = Path(pdf_path)
        output_pages_dir = Path(output_pages_dir)
        assigned_id = doc_id or uuid.uuid4().hex

        if not self.is_valid_pdf(pdf_path):
            logger.error(f"Cannot render invalid or missing PDF: '{pdf_path}'")
            raise InvalidPDFError(f"File is not a valid PDF: '{pdf_path}'")

        output_pages_dir.mkdir(parents=True, exist_ok=True)
        logger.info(
            f"Starting PDF rendering for '{pdf_path.name}' at {dpi} DPI (Doc ID: {assigned_id})"
        )

        start_time = time.perf_counter()
        rendered_paths: list[Path] = []
        first_page_width = 0
        first_page_height = 0

        try:
            doc = fitz.open(str(pdf_path))
            page_count = len(doc)

            for page_index in range(page_count):
                page_num = page_index + 1
                page = doc.load_page(page_index)
                pix = page.get_pixmap(dpi=dpi)

                if page_index == 0:
                    first_page_width = pix.width
                    first_page_height = pix.height

                filename = PAGE_FILENAME_PATTERN.format(page_num=page_num)
                out_file_path = output_pages_dir / filename

                pix.save(str(out_file_path))
                rendered_paths.append(out_file_path)
                logger.debug(f"Rendered page {page_num}/{page_count} -> {out_file_path.name}")

            doc.close()
            elapsed_time = time.perf_counter() - start_time
            avg_sec = elapsed_time / page_count if page_count > 0 else 0.0

            logger.info(
                f"Successfully rendered {page_count} pages in {elapsed_time:.2f}s "
                f"({avg_sec:.3f}s/page) to '{output_pages_dir}'"
            )

            return RenderResult(
                doc_id=assigned_id,
                filename=pdf_path.name,
                pages=rendered_paths,
                page_count=page_count,
                dpi=dpi,
                width=first_page_width,
                height=first_page_height,
                elapsed_time=round(elapsed_time, 4),
                avg_sec_per_page=round(avg_sec, 4),
                render_engine=DEFAULT_RENDER_ENGINE,
                status="completed",
            )
        except Exception as e:
            elapsed_time = time.perf_counter() - start_time
            logger.error(f"Error rendering PDF '{pdf_path.name}': {e}", exc_info=True)
            raise PDFRenderingError(
                f"Failed to render pages for '{pdf_path.name}': {e}"
            ) from e

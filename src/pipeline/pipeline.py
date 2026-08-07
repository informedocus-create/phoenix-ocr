"""
Document Processing Pipeline: Manages workspace directory isolation, UUID generation,
per-stage file logging, rendering orchestration, and metadata serialization.
"""

from datetime import datetime, timezone
import json
from pathlib import Path
import uuid

from src.core.settings import (
    DEFAULT_OUTPUT_DIR,
    DEFAULT_DPI,
)
from src.core.logger import setup_logger
from src.core.exceptions import InvalidPDFError, PDFRenderingError
from src.pdf.interface import BasePDFRenderer
from src.pdf.renderer import PyMuPDFRenderer
from src.pdf.models import RenderResult


class DocumentPipeline:
    """Orchestrates document workspace setup, stage logging, PDF rendering, and metadata tracking."""

    def __init__(
        self,
        renderer: BasePDFRenderer | None = None,
        base_output_dir: Path = DEFAULT_OUTPUT_DIR,
    ):
        """Initializes the document pipeline.

        Args:
            renderer: Optional PDF renderer implementing BasePDFRenderer. Defaults to PyMuPDFRenderer.
            base_output_dir: Base directory for storing per-document output workspaces.
        """
        self.renderer: BasePDFRenderer = renderer or PyMuPDFRenderer()
        self.base_output_dir: Path = Path(base_output_dir)

    def process_document(
        self,
        pdf_path: Path,
        dpi: int = DEFAULT_DPI,
        doc_id: str | None = None,
    ) -> RenderResult:
        """Processes a single PDF document through the rendering stage.

        Creates an isolated output directory structure:
        output/<doc_name>/
          ├── pages/
          │   ├── page_0001.png
          ├── logs/
          │   └── render.log
          └── metadata.json

        Args:
            pdf_path: Path to the target PDF document.
            dpi: Resolution in DPI (default 300).
            doc_id: Optional custom UUID string.

        Returns:
            RenderResult containing pipeline benchmark metrics and page paths.
        """
        pdf_path = Path(pdf_path).resolve()
        doc_uuid = doc_id or uuid.uuid4().hex
        doc_slug = pdf_path.stem

        # Create isolated workspace structure
        doc_workspace_dir = self.base_output_dir / doc_slug
        pages_dir = doc_workspace_dir / "pages"
        logs_dir = doc_workspace_dir / "logs"

        pages_dir.mkdir(parents=True, exist_ok=True)
        logs_dir.mkdir(parents=True, exist_ok=True)

        render_log_file = logs_dir / "render.log"
        logger = setup_logger("phoenix_ocr.pipeline", log_file=render_log_file)

        logger.info(f"Initialized workspace for document '{pdf_path.name}' [UUID: {doc_uuid}]")

        try:
            # Execute Rendering
            result = self.renderer.render(
                pdf_path=pdf_path,
                output_pages_dir=pages_dir,
                dpi=dpi,
                doc_id=doc_uuid,
            )

            # Write Metadata JSON
            self._write_metadata(doc_workspace_dir / "metadata.json", pdf_path, result)
            return result

        except (InvalidPDFError, PDFRenderingError) as err:
            logger.error(f"Pipeline execution failed for '{pdf_path.name}': {err}")
            failure_result = RenderResult(
                doc_id=doc_uuid,
                filename=pdf_path.name,
                dpi=dpi,
                render_engine=getattr(self.renderer, "DEFAULT_RENDER_ENGINE", "PyMuPDF"),
                status="failed",
                error_message=str(err),
            )
            self._write_metadata(doc_workspace_dir / "metadata.json", pdf_path, failure_result)
            raise

    def _write_metadata(
        self,
        metadata_file: Path,
        pdf_path: Path,
        result: RenderResult,
    ) -> None:
        """Serializes pipeline execution metadata into a structured JSON file."""
        metadata = {
            "doc_id": result.doc_id,
            "filename": pdf_path.name,
            "page_count": result.page_count,
            "dpi": result.dpi,
            "render_engine": result.render_engine,
            "dimensions": {
                "width": result.width,
                "height": result.height,
            },
            "benchmarks": {
                "elapsed_time_seconds": result.elapsed_time,
                "avg_sec_per_page": result.avg_sec_per_page,
            },
            "status": result.status,
            "error_message": result.error_message,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)

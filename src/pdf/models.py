"""
Data models for PDF rendering results and document metadata.
"""

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


@dataclass
class RenderResult:
    """Represents the benchmark and execution metrics of a PDF rendering job."""

    doc_id: str
    filename: str
    pages: list[Path] = field(default_factory=list)
    page_count: int = 0
    dpi: int = 300
    width: int = 0
    height: int = 0
    elapsed_time: float = 0.0
    avg_sec_per_page: float = 0.0
    render_engine: str = "PyMuPDF"
    status: str = "pending"  # "completed" | "failed"
    error_message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Converts RenderResult dataclass into a JSON-serializable dictionary."""
        data = asdict(self)
        data["pages"] = [str(p) for p in self.pages]
        return data


@dataclass
class PDFMetadata:
    """Represents core metadata properties of a PDF document."""

    page_count: int
    title: str = ""
    author: str = ""
    creator: str = ""
    producer: str = ""
    creation_date: str = ""

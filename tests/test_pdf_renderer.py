"""
Unit tests for PDF renderer interface, PyMuPDF engine, and Document Pipeline.
"""

import json
from pathlib import Path
import pytest
import pymupdf as fitz

from src.core.exceptions import InvalidPDFError
from src.pdf.renderer import PyMuPDFRenderer
from src.pdf.models import RenderResult
from src.pipeline.pipeline import DocumentPipeline


@pytest.fixture
def sample_pdf(tmp_path: Path) -> Path:
    """Fixture that creates a synthetic 2-page PDF document for testing."""
    pdf_path = tmp_path / "sample_test.pdf"
    doc = fitz.open()

    # Page 1
    page1 = doc.new_page(width=612, height=792)
    page1.insert_text((50, 100), "Phoenix OCR Benchmark Sample Page 1", fontsize=16)

    # Page 2
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text((50, 100), "Phoenix OCR Benchmark Sample Page 2", fontsize=16)

    doc.save(str(pdf_path))
    doc.close()
    return pdf_path


@pytest.fixture
def invalid_file(tmp_path: Path) -> Path:
    """Fixture that creates a non-PDF text file for error handling tests."""
    bad_path = tmp_path / "not_a_pdf.txt"
    bad_path.write_text("This is plain text, not a PDF document.")
    return bad_path


def test_is_valid_pdf_valid_file(sample_pdf: Path):
    """Verifies PDF detection for a valid PDF file."""
    renderer = PyMuPDFRenderer()
    assert renderer.is_valid_pdf(sample_pdf) is True


def test_is_valid_pdf_invalid_file(invalid_file: Path):
    """Verifies PDF detection returns False for invalid files."""
    renderer = PyMuPDFRenderer()
    assert renderer.is_valid_pdf(invalid_file) is False


def test_is_valid_pdf_nonexistent_file(tmp_path: Path):
    """Verifies PDF detection returns False for missing files."""
    renderer = PyMuPDFRenderer()
    missing_path = tmp_path / "does_not_exist.pdf"
    assert renderer.is_valid_pdf(missing_path) is False


def test_get_page_count_success(sample_pdf: Path):
    """Verifies correct page count retrieval for a valid PDF."""
    renderer = PyMuPDFRenderer()
    assert renderer.get_page_count(sample_pdf) == 2


def test_get_page_count_invalid_file(invalid_file: Path):
    """Verifies InvalidPDFError is raised when reading page count of invalid file."""
    renderer = PyMuPDFRenderer()
    with pytest.raises(InvalidPDFError):
        renderer.get_page_count(invalid_file)


def test_render_pdf_pages(sample_pdf: Path, tmp_path: Path):
    """Verifies rendering pages at 300 DPI outputs correctly named image files."""
    renderer = PyMuPDFRenderer()
    output_dir = tmp_path / "pages"

    result = renderer.render(pdf_path=sample_pdf, output_pages_dir=output_dir, dpi=300)

    assert isinstance(result, RenderResult)
    assert result.status == "completed"
    assert result.page_count == 2
    assert len(result.pages) == 2
    assert result.dpi == 300
    assert result.pages[0].name == "page_0001.png"
    assert result.pages[1].name == "page_0002.png"
    assert result.pages[0].is_file()
    assert result.pages[1].is_file()
    assert result.elapsed_time > 0.0


def test_document_pipeline_workspace_and_metadata(sample_pdf: Path, tmp_path: Path):
    """Verifies DocumentPipeline creates isolated workspace, render.log, and metadata.json."""
    pipeline = DocumentPipeline(base_output_dir=tmp_path)
    result = pipeline.process_document(pdf_path=sample_pdf, dpi=300)

    workspace_dir = tmp_path / "sample_test"
    pages_dir = workspace_dir / "pages"
    logs_dir = workspace_dir / "logs"
    metadata_file = workspace_dir / "metadata.json"
    render_log = logs_dir / "render.log"

    assert workspace_dir.is_dir()
    assert pages_dir.is_dir()
    assert logs_dir.is_dir()
    assert metadata_file.is_file()
    assert render_log.is_file()

    with open(metadata_file, "r", encoding="utf-8") as f:
        meta = json.load(f)

    assert meta["filename"] == "sample_test.pdf"
    assert meta["page_count"] == 2
    assert meta["dpi"] == 300
    assert meta["status"] == "completed"
    assert "doc_id" in meta
    assert "benchmarks" in meta
    assert meta["benchmarks"]["elapsed_time_seconds"] == result.elapsed_time

# Phoenix OCR

**Phoenix OCR** is a modular, high-performance document processing pipeline built with Python 3.12+.

---

## Sprint 1 Features

- **Abstract PDF Renderer Interface**: Decoupled engine abstraction (`BasePDFRenderer` -> `PyMuPDFRenderer`) supporting future engine plugins (e.g. Poppler, Ghostscript).
- **High-Resolution Rendering**: Renders PDF pages to crisp PNG images at **300 DPI** (configurable).
- **Isolated Document Workspaces**: Every document creates a dedicated output workspace directory under `output/<document_name>/`.
- **Pipeline Tracking & UUIDs**: Unique `UUID` generated for every processed document for cross-stage traceability.
- **Structured Metadata Serialization**: Emits `metadata.json` for every processed document containing page dimensions, execution status, and benchmark timing.
- **Per-Stage File Logging**: Writes detailed stage logs (`logs/render.log`) alongside console logging.
- **Performance Benchmarks**: Records total execution time, resolution dimensions, and average seconds-per-page metrics.

---

## Directory Structure

```
phoenix-ocr/
├── src/
│   ├── core/
│   │   ├── settings.py       # Centralized configuration constants
│   │   ├── logger.py         # Console & per-stage file logger
│   │   └── exceptions.py     # Custom exception hierarchy
│   ├── pdf/
│   │   ├── interface.py      # Abstract BasePDFRenderer
│   │   ├── renderer.py       # PyMuPDF engine implementation
│   │   └── models.py         # RenderResult & PDFMetadata models
│   ├── pipeline/
│   │   └── pipeline.py       # Document workspace & execution coordinator
│   ├── ocr/                  # Reserved for OCR engine integrations
│   ├── layout/               # Reserved for layout analysis
│   ├── export/               # Reserved for document exporters
│   ├── utils/                # General utility helper functions
│   └── main.py               # CLI entrypoint
├── input/                    # Raw input documents (.pdf)
├── output/                   # Processed workspaces per document
│   └── <document_name>/
│       ├── pages/            # Rendered page images (page_0001.png, ...)
│       ├── logs/             # Stage logs (render.log)
│       └── metadata.json     # Pipeline metadata & benchmark metrics
├── tests/
│   └── test_pdf_renderer.py  # Unit test suite
├── benchmarks/               # Document test dataset categories
├── requirements.txt          # Python dependencies
├── README.md
└── .gitignore
```

---

## Setup Instructions

### 1. Create & Activate Virtual Environment
```powershell
py -3.12 -m venv .venv

# PowerShell:
.venv\Scripts\Activate.ps1

# Command Prompt:
.venv\Scripts\activate
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## Usage

### Run Pipeline on Input Folder
Place `.pdf` files inside `input/`, then run:
```powershell
python -m src.main
```

### Options
- `-i`, `--input`: Custom input directory (default: `input/`).
- `-o`, `--output`: Custom output directory (default: `output/`).
- `-f`, `--file`: Process a specific single PDF file.
- `--dpi`: Rendering resolution (default: `300`).

#### Example
```powershell
python -m src.main --file input/sample_invoice.pdf --dpi 300
```

---

## Sample `metadata.json` Output

```json
{
    "doc_id": "3d742295c98148dea270787269d9d40a",
    "filename": "sample_invoice.pdf",
    "page_count": 2,
    "dpi": 300,
    "render_engine": "PyMuPDF",
    "dimensions": {
        "width": 2550,
        "height": 3300
    },
    "benchmarks": {
        "elapsed_time_seconds": 0.9275,
        "avg_sec_per_page": 0.4637
    },
    "status": "completed",
    "error_message": null,
    "created_at": "2026-08-07T05:41:42.108903+00:00"
}
```

---

## Running Unit Tests

Run the unit test suite using `pytest`:
```powershell
python -m pytest tests/
```

---

## License

This project is licensed under the [MIT License](file:///c:/Users/HP/Desktop/phoenix-ocr/LICENSE).

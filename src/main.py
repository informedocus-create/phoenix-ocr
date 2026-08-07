"""
CLI Entrypoint for Phoenix OCR Document Processing Pipeline.
"""

import argparse
import sys
from pathlib import Path

from src.core.settings import (
    DEFAULT_INPUT_DIR,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_DPI,
)
from src.core.logger import setup_logger
from src.core.exceptions import PhoenixOCRError
from src.pipeline.pipeline import DocumentPipeline

logger = setup_logger("phoenix_ocr.cli")


def parse_args() -> argparse.Namespace:
    """Parses command-line arguments for the Phoenix OCR pipeline CLI."""
    parser = argparse.ArgumentParser(
        description="Phoenix OCR Pipeline: Render PDF documents into high-resolution images."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help=f"Path to input folder containing PDF documents (default: {DEFAULT_INPUT_DIR})",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Path to output root directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=Path,
        default=None,
        help="Path to a specific single PDF file to process",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=DEFAULT_DPI,
        help=f"Target rendering resolution in DPI (default: {DEFAULT_DPI})",
    )
    return parser.parse_args()


def main() -> int:
    """Main execution function orchestrating PDF rendering pipeline."""
    args = parse_args()

    input_dir: Path = args.input.resolve()
    output_dir: Path = args.output.resolve()
    dpi: int = args.dpi

    logger.info("==========================================")
    logger.info(" Starting Phoenix OCR - Document Pipeline ")
    logger.info("==========================================")

    # Determine target PDF files
    pdf_files: list[Path] = []
    if args.file:
        single_file = args.file.resolve()
        if not single_file.is_file():
            logger.error(f"Specified single file not found: '{single_file}'")
            return 1
        pdf_files.append(single_file)
    else:
        input_dir.mkdir(parents=True, exist_ok=True)
        pdf_files = sorted(
            {p.resolve() for p in input_dir.glob("*") if p.is_file() and p.suffix.lower() == ".pdf"}
        )


    if not pdf_files:
        logger.warning(
            f"No PDF files found in '{input_dir}'. Please place PDF documents into '{input_dir}'."
        )
        return 0

    logger.info(f"Discovered {len(pdf_files)} document(s) to process.")

    pipeline = DocumentPipeline(base_output_dir=output_dir)
    successful_count = 0
    failed_count = 0

    for pdf_path in pdf_files:
        try:
            result = pipeline.process_document(pdf_path=pdf_path, dpi=dpi)
            successful_count += 1
            logger.info(
                f"[SUCCESS] '{pdf_path.name}': Rendered {result.page_count} page(s) "
                f"in {result.elapsed_time}s ({result.avg_sec_per_page}s/page)."
            )
        except PhoenixOCRError as err:
            failed_count += 1
            logger.error(f"[FAILURE] Failed to process '{pdf_path.name}': {err}")

    logger.info("------------------------------------------")
    logger.info(
        f"Pipeline Summary: {successful_count} succeeded, {failed_count} failed out of {len(pdf_files)} document(s)."
    )
    logger.info("==========================================")

    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

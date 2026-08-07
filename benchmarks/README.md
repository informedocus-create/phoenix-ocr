# Benchmark Dataset Guidelines

This directory contains test documents across various challenging real-world categories to benchmark OCR performance and accuracy.

## Categories

| Directory | Description | Challenge Type |
| :--- | :--- | :--- |
| `receipts/` | Store receipts, thermal paper prints | Low resolution, thermal fading, narrow width |
| `invoices/` | Standard business invoices | Complex tabular layouts, line items |
| `books/` | Scanned book pages | Curvature, spine shadows, dense text |
| `newspapers/` | Newspaper clippings / columns | Multi-column layouts, tight line spacing |
| `forms/` | Structured & filled forms | Boxed text, checkboxes, mixed printed & handwriting |
| `business_cards/` | Business & contact cards | Small fonts, logos, stylized graphics |
| `handwriting/` | Handwritten notes & documents | Non-standard cursive/print fonts |
| `low_quality/` | Blurry, noisy, low DPI, or degraded scans | Compression artifacts, noise, low contrast |
| `rotated/` | 90°, 180°, 270°, or skewed pages | Orientation & perspective distortion |

## Sample Target Count
- Target: 50–100 test documents total across categories (5–10 per category).
- Annotations / Ground Truth (optional): Store matching `.txt` or `.json` files alongside sample images/PDFs with the same base name (e.g., `receipt_001.png` and `receipt_001.json`).

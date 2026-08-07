# OCR Benchmark Dataset

Real-world, imperfect documents for testing OCR pipeline accuracy — not just clean PDFs.
Each subfolder targets a specific failure mode OCR engines commonly struggle with.

| Folder | Focus |
|---|---|
| receipts/ | Thermal print fade, creases, small fonts |
| invoices/ | Tables, mixed digital/scanned quality |
| books/ | Spine curvature, columns, footnotes |
| newspapers/ | Dense multi-column, low contrast |
| forms/ | Handwriting + checkboxes + printed labels |
| business_cards/ | Tiny size, decorative fonts, logos |
| handwriting/ | Cursive/print, legibility variance |
| low_quality/ | Blur, poor lighting, compression artifacts |
| rotated/ | Skew and 90/180/270 rotation |

## Target
50-100 documents total, collected over time. That's roughly 6-11 per category if spread evenly — but weight it toward whatever category matters most for your actual product (e.g. receipts/forms if this feeds Pennyfy's bill-scanning).

## Where to get documents

**Your own scans** — always preferred when possible, since you control ground truth and know it's representative of your real users' documents (Indian GST invoices, UPI receipts, regional-language forms, etc.).

**Public research datasets** (research-use licensed, not commercial redistribution — read each one's license before using in a commercial product benchmark, though using them locally to *measure your own pipeline* is standard practice):
- `receipts/` — [SROIE](https://github.com/zzzDavid/ICDAR-2019-SROIE): 1,000 real scanned receipts with ground-truth annotations.
- `forms/` — [FUNSD](https://guillaumejaume.github.io/FUNSD/): 199 noisy scanned forms, printed + some handwriting.
- `handwriting/` — [IAM Handwriting Database](https://huggingface.co/datasets/Teklia/IAM-line): 1,539 scanned pages, line-level ground truth.
- `newspapers/` — [Chronicling America](https://www.loc.gov/collections/chronicling-america/) (Library of Congress): public-domain historical newspaper scans.
- `invoices/` — [UCSF Industry Documents Library](https://www.industrydocuments.ucsf.edu/): real scanned business documents with layout noise.
- `books/` — [Internet Archive](https://archive.org/): millions of public-domain scanned book pages, downloadable directly.
- `business_cards/` — no good public dataset exists; collect your own or generate mockups with a design tool.
- `low_quality/`, `rotated/` — don't source these separately. Run `generate_derived.py` to synthesize them from whatever you've already collected in the other folders (blur/compress/downscale for low_quality, rotate/skew for rotated).

## Ground truth
Include a `.txt` or `.json` transcription alongside each sample wherever possible — that's what lets you actually score OCR accuracy (e.g. character/word error rate) rather than eyeballing it. Public datasets above ship with ground truth already; for your own scans, transcribe manually as you add them.

## Workflow
```bash
# after adding a real document to a category folder:
python3 track_progress.py add --file receipts/my_receipt.jpg \
    --category receipts --source "own scan" --license "own document" \
    --ground-truth yes --notes "faded thermal print, creased"

# check progress toward the 50-100 target:
python3 track_progress.py status

# once you have real documents in the other folders, backfill low_quality/ and rotated/:
python3 generate_derived.py
```

## Indian-market bias
If this benchmark is meant to reflect your actual users, don't let it default to English/Western documents just because that's what public datasets skew toward. Deliberately include Hindi/regional-language receipts, GST invoices, and PAN/Aadhaar-style forms with code-mixed text — that's usually where off-the-shelf OCR (trained mostly on Western data) breaks down hardest, and it's the gap that matters for your product.

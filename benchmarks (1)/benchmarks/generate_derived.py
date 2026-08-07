#!/usr/bin/env python3
"""
Generate low_quality/ and rotated/ samples by degrading/rotating images
already collected in the other category folders. Saves you from having
to source these two categories independently.

Usage:
  python3 generate_derived.py

Reads image files from receipts/, invoices/, books/, newspapers/, forms/,
business_cards/, handwriting/ and writes degraded/rotated copies into
low_quality/ and rotated/, prefixed with the source category so you can
trace provenance back through manifest.csv.
"""
import os
import io
import random
from PIL import Image, ImageFilter

BASE = os.path.dirname(__file__)
SOURCE_CATEGORIES = [
    "receipts", "invoices", "books", "newspapers",
    "forms", "business_cards", "handwriting",
]
IMAGE_EXT = (".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp")


def find_source_images():
    found = []
    for cat in SOURCE_CATEGORIES:
        folder = os.path.join(BASE, cat)
        if not os.path.isdir(folder):
            continue
        for fname in os.listdir(folder):
            if fname.lower().endswith(IMAGE_EXT):
                found.append((cat, os.path.join(folder, fname)))
    return found


def make_low_quality(img):
    """Blur + downscale/upscale + heavy JPEG recompression + mild noise."""
    img = img.convert("RGB")
    img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(1.0, 2.5)))
    w, h = img.size
    scale = random.uniform(0.35, 0.55)
    small = img.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.BILINEAR)
    img = small.resize((w, h), Image.BILINEAR)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=random.randint(15, 35))
    buf.seek(0)
    return Image.open(buf).convert("RGB")


def make_rotated(img):
    angle = random.choice([90, 180, 270, random.randint(3, 12), -random.randint(3, 12)])
    return img.convert("RGB").rotate(angle, expand=True, fillcolor=(255, 255, 255)), angle


def main():
    sources = find_source_images()
    if not sources:
        print("No source images found yet in receipts/, invoices/, books/, etc.")
        print("Add real documents to those folders first, then re-run this script.")
        return

    lq_dir = os.path.join(BASE, "low_quality")
    rot_dir = os.path.join(BASE, "rotated")
    os.makedirs(lq_dir, exist_ok=True)
    os.makedirs(rot_dir, exist_ok=True)

    lq_count, rot_count = 0, 0
    for cat, path in sources:
        fname = os.path.splitext(os.path.basename(path))[0]
        try:
            img = Image.open(path)
        except Exception as e:
            print(f"Skipping {path}: {e}")
            continue

        lq = make_low_quality(img)
        lq_path = os.path.join(lq_dir, f"{cat}_{fname}_lowquality.jpg")
        lq.save(lq_path, "JPEG")
        lq_count += 1

        rot, angle = make_rotated(img)
        rot_path = os.path.join(rot_dir, f"{cat}_{fname}_rot{angle}.jpg")
        rot.save(rot_path, "JPEG")
        rot_count += 1

    print(f"Generated {lq_count} low_quality samples -> low_quality/")
    print(f"Generated {rot_count} rotated samples -> rotated/")
    print("Remember to log these in manifest.csv (source = original file + 'synthetic degradation').")


if __name__ == "__main__":
    main()

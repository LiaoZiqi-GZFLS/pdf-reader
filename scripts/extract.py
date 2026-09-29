#!/usr/bin/env python3
"""PDF text extraction and page rendering using PyMuPDF.

Usage:
    python extract.py <pdf_path> [--pages RANGE] [--format FORMAT] [--output DIR]

Options:
    --pages RANGE    Page range, e.g. "1-5", "3", "2,4,6-8". Default: all
    --format FORMAT  Output format: "text" (default), "image" (render pages as PNG)
    --output DIR     Output directory for images (default: ./pdf_output)

Examples:
    python extract.py doc.pdf                     # Extract all pages as text
    python extract.py doc.pdf --pages 1-5         # Extract pages 1-5 as text
    python extract.py doc.pdf --format image --pages 1-3  # Render pages 1-3 as PNG
"""

import sys
import os
import argparse

try:
    import pymupdf
except ImportError:
    print("ERROR: PyMuPDF not installed. Run: pip install pymupdf", file=sys.stderr)
    sys.exit(1)


def parse_page_range(range_str, total_pages):
    """Parse page range string into list of 0-based page indices."""
    pages = set()
    for part in range_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            start = max(1, int(start))
            end = min(total_pages, int(end))
            pages.update(range(start, end + 1))
        else:
            p = int(part)
            if 1 <= p <= total_pages:
                pages.add(p)
    return sorted(pages)


def extract_text(pdf_path, pages=None):
    """Extract text from PDF pages."""
    doc = pymupdf.open(pdf_path)
    total = len(doc)
    page_nums = pages if pages else list(range(1, total + 1))

    print(f"PDF: {os.path.basename(pdf_path)} ({total} pages)", file=sys.stderr)
    print(f"Extracting pages: {page_nums[0]}-{page_nums[-1] if len(page_nums) > 1 else page_nums[0]}"
          if page_nums else "No pages selected", file=sys.stderr)
    print("=" * 60, file=sys.stderr)

    for p in page_nums:
        idx = p - 1
        text = doc[idx].get_text()
        # Write to stdout with explicit UTF-8 encoding
        sys.stdout.buffer.write(f"\n=== Page {p} ===\n".encode("utf-8"))
        if text.strip():
            sys.stdout.buffer.write(text.encode("utf-8"))
            sys.stdout.buffer.write(b"\n")
        else:
            sys.stdout.buffer.write(b"[No extractable text on this page]\n")

    doc.close()
    print(f"\nDone. Extracted {len(page_nums)} page(s).", file=sys.stderr)


def render_images(pdf_path, pages=None, output_dir="./pdf_output"):
    """Render PDF pages as PNG images."""
    doc = pymupdf.open(pdf_path)
    total = len(doc)
    page_nums = pages if pages else list(range(1, total + 1))

    os.makedirs(output_dir, exist_ok=True)

    print(f"PDF: {os.path.basename(pdf_path)} ({total} pages)", file=sys.stderr)
    print(f"Rendering {len(page_nums)} page(s) to {output_dir}/", file=sys.stderr)

    saved = []
    for p in page_nums:
        idx = p - 1
        page = doc[idx]
        # Render at 2x resolution for readability
        mat = pymupdf.Matrix(2, 2)
        pix = page.get_pixmap(matrix=mat)
        out_path = os.path.join(output_dir, f"page_{p:03d}.png")
        pix.save(out_path)
        saved.append(out_path)
        sys.stdout.buffer.write(f"Saved: {out_path}\n".encode("utf-8"))

    doc.close()
    print(f"\nDone. Rendered {len(saved)} page(s).", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="PDF text/image extraction using PyMuPDF")
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument("--pages", default=None, help="Page range, e.g. '1-5' or '3' or '2,4,6-8'")
    parser.add_argument("--format", dest="fmt", default="text", choices=["text", "image"],
                        help="Output format: text (default) or image")
    parser.add_argument("--output", default="./pdf_output", help="Output directory for images")
    args = parser.parse_args()

    if not os.path.exists(args.pdf_path):
        print(f"ERROR: File not found: {args.pdf_path}", file=sys.stderr)
        sys.exit(1)

    doc = pymupdf.open(args.pdf_path)
    total = len(doc)
    doc.close()

    pages = parse_page_range(args.pages, total) if args.pages else None

    if args.fmt == "text":
        extract_text(args.pdf_path, pages)
    else:
        render_images(args.pdf_path, pages, args.output)


if __name__ == "__main__":
    main()

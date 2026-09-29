---
name: pdf-reader
description: Read, extract text, and render PDF files. Use when the user asks to read a PDF, view PDF content, extract text from PDF, convert PDF pages to images, or when a PDF file path appears in the conversation. Supports page range selection and image rendering. Replaces the built-in Read tool for .pdf files which requires poppler-utils.
---

# PDF Reader

Extract text or render pages from PDF files using PyMuPDF. Works on all platforms without external dependencies (no poppler-utils needed).

## Usage

Run the bundled extraction script with Bash:

```bash
python "<skill_dir>/scripts/extract.py" <pdf_path> [options]
```

Options:
- `--pages RANGE` — Page range: `"1-5"`, `"3"`, `"2,4,6-8"`. Default: all pages.
- `--format text|image` — `text` (default) extracts text; `image` renders pages as PNG.
- `--output DIR` — Directory for rendered images (default: `./pdf_output`).

## Workflow

### Read PDF text content

```bash
python "<skill_dir>/scripts/extract.py" "path/to/file.pdf" --pages 1-10
```

Text goes to stdout (UTF-8), progress to stderr. For large PDFs, use `--pages` to limit scope.

### Render PDF pages as images

For scanned PDFs, diagrams, or when text extraction yields poor results:

```bash
python "<skill_dir>/scripts/extract.py" "path/to/file.pdf" --format image --pages 1-3
```

Then use the Read tool on the generated PNG files to view them visually.

## Important Notes

- Output is UTF-8 encoded via `stdout.buffer`; console encoding (GBK on Windows) does not cause errors.
- For PDFs with complex layouts (tables, multi-column), text extraction may lose structure — use image mode instead.
- Progress and metadata print to stderr, so they won't mix with extracted content.

## Prerequisites

- Python 3.8+
- `pymupdf` package (`pip install pymupdf`)

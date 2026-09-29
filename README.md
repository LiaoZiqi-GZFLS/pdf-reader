# pdf-reader

A [Qoder CLI](https://qoder.com) skill that reads PDF files — extracting text or
rendering pages as images — with no external system dependencies.

It uses **PyMuPDF**, so unlike the built-in Read tool it does **not** require
`poppler-utils`. The same skill therefore works unchanged on Windows, macOS, and Linux.

## Features

- Extract text from a PDF, with optional page-range selection.
- Render pages to PNG for scanned PDFs, diagrams, or layouts where text extraction
  loses structure.
- UTF-8 output on stdout, progress on stderr — safe on Windows consoles (GBK) and
  clean to pipe into other tools.

## Requirements

- Python 3.8+
- [`pymupdf`](https://pypi.org/project/PyMuPDF/): `pip install pymupdf`

## Installation

Copy the skill into your Qoder CLI skills directory:

```bash
# macOS / Linux
cp -r pdf-reader ~/.qoder-cn/skills/

# Windows (Git Bash)
cp -r pdf-reader "$USERPROFILE/.qoder-cn/skills/"
```

Qoder CLI discovers skills under that directory automatically. Once installed, ask it to
read a PDF (or just reference a `.pdf` path) and the skill activates.

## Usage

```bash
python scripts/extract.py <pdf_path> [options]
```

| Option | Description |
| --- | --- |
| `--pages RANGE` | Page range: `"1-5"`, `"3"`, `"2,4,6-8"`. Default: all pages. |
| `--format text\|image` | `text` (default) extracts text; `image` renders pages as PNG. |
| `--output DIR` | Directory for rendered images (default: `./pdf_output`). |

### Examples

Extract text from pages 1–10:

```bash
python scripts/extract.py doc.pdf --pages 1-10
```

Render pages 1–3 as PNG (then view them with the Read tool):

```bash
python scripts/extract.py doc.pdf --format image --pages 1-3
```

## Layout

```
pdf-reader/
├── SKILL.md            # skill manifest (name, description, workflow)
└── scripts/
    └── extract.py      # PyMuPDF text extraction + page rendering
```

## Notes

- For PDFs with complex layouts (tables, multi-column text), text extraction may lose
  structure — use `--format image` instead.
- Large PDFs: narrow the scope with `--pages` rather than extracting everything.

## License

No license specified. Add one if you intend others to reuse this work.

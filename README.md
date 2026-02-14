# Bassi LeGani 5711 - German Translation

Bilingual (Hebrew/German) edition of the Lubavitcher Rebbe's first Ma'amar, delivered on 10 Shevat 5711 (1951).

## Prerequisites

- Python 3.14+
- [Pandoc](https://pandoc.org/) (for EPUB)
- [Typst](https://typst.app/) (for PDF)

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Build

```bash
./build a4                        # PDF A4 (two-column)
./build a5                        # PDF A5 (single-column booklet)
./build epub                      # EPUB
./build all                       # all formats
./build a4 --version v1.2.3      # inject version string
```

### Manual build (without wrapper)

```bash
# EPUB
python scripts/build_epub.py input/5711/[0-9]*.md -o output/5711/epub/book.epub

# PDF A4
python scripts/build_pdf.py input/5711/[0-9]*.md -o output/5711/pdf-a4 --template templates/typst/book-a4.typ
typst compile --font-path fonts/ output/5711/pdf-a4/book.typ

# PDF A5
python scripts/build_pdf.py input/5711/[0-9]*.md -o output/5711/pdf-a5 --template templates/typst/book-a5.typ
typst compile --font-path fonts/ output/5711/pdf-a5/book.typ
```

Both `build_pdf.py` and `build_epub.py` accept `--version <version>` to replace `{{VERSION}}` placeholders in the source files (without modifying them). The CI pipeline injects this automatically via git tags.

## Project Structure

```
input/          Source markdown translations (custom format with :::verse, :::commentary blocks)
output/         Generated files (gitignored)
scripts/        Build scripts (markdown -> epub/typst)
templates/      Typst templates (A4/A5) and EPUB CSS
fonts/          Hebrew font (SBL Hebrew)
docs/           Translation guide, output format spec, glossary
```

## Translation Format

See `docs/output-format.md` for the custom markdown block syntax used in chapter files.
See `docs/translation-guide.md` for translation style and terminology conventions.

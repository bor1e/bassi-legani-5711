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

Local output goes to `build/` (gitignored). `--version` is optional; omit it to hide version info.

```bash
./build a4                        # PDF A4 (no version displayed)
./build a4 --version v1.2.3      # PDF A4 (two-column)
./build a5 --version v1.2.3      # PDF A5 (single-column booklet)
./build epub --version v1.2.3    # EPUB
./build all --version v1.2.3     # all formats
```

### Manual build (without wrapper)

```bash
# EPUB
python scripts/build_epub.py input/5711/[0-9]*.md -o build/epub/book.epub --version v1.2.3

# PDF A4
python scripts/build_pdf.py input/5711/[0-9]*.md -o build/pdf-a4 --template templates/typst/book-a4.typ --version v1.2.3
typst compile --font-path fonts/ build/pdf-a4/book.typ

# PDF A5
python scripts/build_pdf.py input/5711/[0-9]*.md -o build/pdf-a5 --template templates/typst/book-a5.typ --version v1.2.3
typst compile --font-path fonts/ build/pdf-a5/book.typ
```

`--version` replaces `{{VERSION}}` placeholders in the source files (without modifying them). When omitted, lines containing `{{VERSION}}` are removed from the output. The CI pipeline injects this automatically via git tags.

## Project Structure

```
input/          Source markdown translations (custom format with :::verse, :::commentary blocks)
build/          Local build output (gitignored)
output/         CI-generated release artifacts (tracked)
scripts/        Build scripts (markdown -> epub/typst)
templates/      Typst templates (A4/A5) and EPUB CSS
fonts/          Hebrew font (SBL Hebrew)
docs/           Translation guide, output format spec, glossary
```

## Translation Format

See `docs/output-format.md` for the custom markdown block syntax used in chapter files.
See `docs/translation-guide.md` for translation style and terminology conventions.

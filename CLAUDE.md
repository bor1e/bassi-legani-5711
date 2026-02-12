# Project Context

Bilingual Hebrew/German book project. Translates a Chassidic discourse (Ma'amar) into German with parallel Hebrew text.

## Pipeline

1. **Input**: Markdown files in `input/5711/` using custom block syntax (:::verse, :::commentary, :::footnote, etc.)
2. **Build**: Python scripts parse markdown and generate either Pandoc-ready HTML (epub) or Typst markup (pdf)
3. **Output**: EPUB via Pandoc, PDF via Typst (A4 two-column or A5 single-column)

## Custom Markdown Format

Chapter files use YAML frontmatter + custom `:::` blocks. See `docs/output-format.md` for the full spec.

Key blocks: `:::verse` (Hebrew + German translation), `:::commentary`, `:::footnote N`, `:::summary`, `:::glossary`, `:::dedication`, `:::infobox`, `:::newpage`.

## Build Commands

```bash
# EPUB
python scripts/build_epub.py input/5711/[0-9]*.md -o output/5711/epub/book.epub

# PDF A4
python scripts/build_pdf.py input/5711/[0-9]*.md -o output/5711/pdf-a4 --template templates/typst/book-a4.typ
typst compile output/5711/pdf-a4/book.typ

# PDF A5
python scripts/build_pdf.py input/5711/[0-9]*.md -o output/5711/pdf-a5 --template templates/typst/book-a5.typ
typst compile output/5711/pdf-a5/book.typ
```

## Conventions

- Hebrew terms in German text: italicized (*Schechina*, *Tora*)
- G-tt with hyphen
- Footnotes: `{{fn:N}}` in text, `:::footnote N` blocks at chapter end
- Files numbered: `1-kapitel.md` through `9-kapitel.md`, `98-sprachguide.md`, `99-glossar.md`

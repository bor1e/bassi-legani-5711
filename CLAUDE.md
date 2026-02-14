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

`--version` is required. Local builds output to `build/` (gitignored).

```bash
./build a4 --version 0.1.0
./build a5 --version 0.1.0
./build epub --version 0.1.0
./build all --version 0.1.0
```

## Conventions

- Hebrew terms in German text: italicized (*Schechina*, *Tora*)
- G-tt with hyphen
- Footnotes: `{{fn:N}}` in text, `:::footnote N` blocks at chapter end
- Files numbered: `1-kapitel.md` through `9-kapitel.md`, `98-sprachguide.md`, `99-glossar.md`

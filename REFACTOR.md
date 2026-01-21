## Plan: Convert LaTeX Ma'amar System to Typst

### Objective
Rewrite the existing LaTeX-based bilingual Ma'amar publishing system to Typst while maintaining the Chayenu-style layout (Hebrew/German columns, highlighted phrases, commentary blocks, footnotes).

---

### Phase 1: Research & Setup

1. **Study Typst Hebrew support**
   - Test RTL text handling
   - Identify Hebrew fonts available in Typst
   - Test bidirectional text in columns

2. **Analyze current LaTeX structure**
   - Document all custom commands (`\hebhl`, `\dehl`, `\germancol`, `\hebrewcol`)
   - List all environments (`verse_block`, `commentary`, `summarybox`)
   - Map LaTeX packages to Typst equivalents

---

### Phase 2: Create Typst Template

1. **Page setup**
   - A4/Letter size, margins matching LaTeX version
   - Headers/footers with book title and page numbers

2. **Typography**
   - Main font (serif) for German
   - Hebrew font with RTL support
   - Define highlight color (#FFF3B0)

3. **Custom functions to create**
   - `#verse()` - two-column Hebrew/German block
   - `#hebhl()` - Hebrew text with yellow highlight
   - `#dehl()` - German text in bold
   - `#commentary()` - full-width italic block with left border
   - `#summary()` - boxed summary section
   - `#srcref()` - source reference in parentheses

4. **Chapter structure**
   - Chapter title (German + Hebrew centered)
   - Content blocks
   - Footnotes at page bottom

---

### Phase 3: Update Markdown Parser

1. **Modify `md-to-latex.py` → `md-to-typst.py`**
   - Keep same input format (OUTPUT_TEMPLATE.md)
   - Change output generation to Typst syntax
   - Update string escaping rules (Typst vs LaTeX)

2. **Mapping table**
   ```
   LaTeX                    → Typst
   \textit{...}            → _..._
   \textbf{...}            → *...*
   \footnote{...}          → #footnote[...]
   \begin{verse_block}     → #verse(...)
   \begin{commentary}      → #commentary[...]
   \glqq...\grqq{}         → „..."
   ```

---

### Phase 4: Create Book Builder

1. **`build-book-typst.py`**
   - Combine chapter files into single `.typ` document
   - Generate table of contents
   - Handle page breaks between chapters

2. **Output structure**
   ```
   output/
   └── 5711/
       └── typst/
           ├── book.typ
           └── chapters/
               ├── 1-kapitel.typ
               └── ...
   ```

---

### Phase 5: Testing & Refinement

1. **Visual comparison**
   - Compile both LaTeX and Typst versions
   - Compare side-by-side with Chayenu reference image
   - Adjust spacing, fonts, colors

2. **Edge cases to test**
   - Long Hebrew phrases wrapping
   - Footnotes spanning pages
   - Mixed Hebrew/German in same line
   - Highlighting across line breaks

3. **Performance**
   - Compilation speed vs LaTeX
   - File size comparison

---

### Deliverables

| File | Description |
|------|-------------|
| `templates/book.typ` | Main Typst book template |
| `templates/chapter.typ` | Chapter template with functions |
| `scripts/md-to-typst.py` | Markdown → Typst converter |
| `scripts/build-book-typst.py` | Book assembly script |
| `OUTPUT_TEMPLATE.md` | Unchanged (same input format) |

---

### Dependencies

- Typst CLI (`typst compile`)
- Python 3.8+ with `pyyaml`
- Hebrew font (bundled or system)

---

### Risk Assessment

| Risk | Mitigation |
|------|------------|
| Typst Hebrew support immature | Test early in Phase 1; fallback to LaTeX |
| Missing equivalent to `paracol` | Build custom two-column function |
| Highlight (`soul` package) not available | Use Typst `highlight()` or `box()` with fill |
| Font availability | Bundle font or use web fonts |
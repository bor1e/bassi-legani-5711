#!/usr/bin/env python3
from __future__ import annotations
import os
import re
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass

try:
    import yaml
except ImportError:
    sys.exit("Error: PyYAML required. Install with: pip install pyyaml")

@dataclass(frozen=True)
class Highlight:
    hebrew: str
    german: str

@dataclass(frozen=True)
class Verse:
    hebrew: str
    translation: str
    source: str | None = None
    highlights: tuple[Highlight, ...] = ()

@dataclass(frozen=True)
class GlossaryEntry:
    term: str
    definition: str

@dataclass(frozen=True)
class Commentary:
    text: str

@dataclass(frozen=True)
class Paragraph:
    text: str

@dataclass(frozen=True)
class Heading:
    level: int
    text: str

@dataclass(frozen=True)
class Footnote:
    number: int
    text: str

@dataclass(frozen=True)
class Summary:
    text: str

@dataclass(frozen=True)
class Dedication:
    text: str

@dataclass(frozen=True)
class Infobox:
    text: str

@dataclass(frozen=True)
class NewPage:
    pass

ContentBlock = Verse | GlossaryEntry | Commentary | Paragraph | Heading | Summary | Dedication | Infobox | NewPage

@dataclass(frozen=True)
class Chapter:
    title: str
    hebrew_title: str
    layout_type: str
    content: tuple[ContentBlock, ...]
    footnotes: tuple[Footnote, ...]

class MarkdownParser:
    def __init__(self, text: str, layout_type: str) -> None:
        self.text = text
        self.lines = text.split('\n')
        self.pos = 0
        self.layout_type = layout_type

    def parse(self) -> Chapter:
        while self.pos < len(self.lines) and not self.lines[self.pos].strip():
            self.pos += 1

        metadata = self._parse_frontmatter()
        content: list[ContentBlock] = []
        footnotes: list[Footnote] = []

        while self.pos < len(self.lines):
            line = self.lines[self.pos].strip()

            if not line:
                self.pos += 1
                continue

            if line.startswith(':::verse'):
                content.append(self._parse_verse())
            elif line.startswith(':::glossary'):
                content.append(self._parse_glossary_entry())
            elif line.startswith(':::commentary'):
                content.append(self._parse_commentary())
            elif line.startswith(':::footnote'):
                footnotes.append(self._parse_footnote(line))
            elif line.startswith(':::summary'):
                content.append(self._parse_summary())
            elif line.startswith(':::dedication'):
                content.append(self._parse_dedication())
            elif line.startswith(':::infobox'):
                content.append(self._parse_infobox())
            elif line.startswith(':::newpage'):
                content.append(NewPage())
                self.pos += 1

            elif line.startswith('#'):
                level = 0
                if line.startswith('###'): level = 3
                elif line.startswith('##'): level = 2
                elif line.startswith('#'): level = 1
                content.append(self._parse_heading(line, level=level))

            elif line.startswith('---'):
                 self.pos += 1

            elif not line.startswith(':::'):
                content.append(self._parse_paragraph())
            else:
                self.pos += 1

        return Chapter(
            title=metadata.get('title', ''),
            hebrew_title=metadata.get('hebrew_title', ''),
            layout_type=self.layout_type,
            content=tuple(content),
            footnotes=tuple(footnotes),
        )

    def _parse_frontmatter(self) -> dict[str, str]:
        if self.pos >= len(self.lines) or self.lines[self.pos].strip() != '---':
            return {}
        self.pos += 1
        yaml_lines: list[str] = []
        while self.pos < len(self.lines) and self.lines[self.pos].strip() != '---':
            yaml_lines.append(self.lines[self.pos])
            self.pos += 1
        self.pos += 1
        try:
            return yaml.safe_load('\n'.join(yaml_lines)) or {}
        except yaml.YAMLError:
            return {}

    def _parse_verse(self) -> Verse:
        self.pos += 1
        hebrew = ""
        translation = ""
        source: str | None = None
        highlights: list[Highlight] = []
        while self.pos < len(self.lines):
            line = self.lines[self.pos].strip()
            if line == ':::':
                self.pos += 1
                break
            elif line == ':hebrew:':
                hebrew = self._parse_until(':/hebrew:')
            elif line == ':translation:':
                translation = self._parse_until(':/translation:')
            elif line == ':source:':
                source = self._parse_until(':/source:').strip()
            elif line == ':highlight:':
                highlights = self._parse_highlights()
            else:
                self.pos += 1
        return Verse(hebrew.strip(), translation.strip(), source, tuple(highlights))

    def _parse_glossary_entry(self) -> GlossaryEntry:
        self.pos += 1
        term = ""
        definition = ""
        while self.pos < len(self.lines):
            line = self.lines[self.pos].strip()
            if line == ':::':
                self.pos += 1
                break
            elif line.startswith(':term:'):
                term = line.replace(':term:', '').strip()
                self.pos += 1
            elif line.startswith(':def:'):
                definition = line.replace(':def:', '').strip()
                self.pos += 1
                while self.pos < len(self.lines) and not self.lines[self.pos].strip().startswith(':'):
                    next_line = self.lines[self.pos].strip()
                    if next_line == ':::':
                        break
                    definition += " " + next_line
                    self.pos += 1
            else:
                self.pos += 1
        return GlossaryEntry(term, definition)

    def _parse_until(self, marker: str) -> str:
        self.pos += 1
        collected: list[str] = []
        while self.pos < len(self.lines):
            if self.lines[self.pos].strip() == marker:
                self.pos += 1
                break
            collected.append(self.lines[self.pos])
            self.pos += 1
        return '\n'.join(collected)

    def _parse_highlights(self) -> list[Highlight]:
        self.pos += 1
        highlights: list[Highlight] = []
        while self.pos < len(self.lines):
            line = self.lines[self.pos].strip()
            if line == ':/highlight:':
                self.pos += 1
                break
            if '|' in line:
                parts = line.split('|', 1)
                highlights.append(Highlight(parts[0].strip(), parts[1].strip()))
            self.pos += 1
        return highlights

    def _collect_block_text(self) -> str:
        self.pos += 1
        collected: list[str] = []
        while self.pos < len(self.lines):
            if self.lines[self.pos].strip() == ':::':
                self.pos += 1
                break
            collected.append(self.lines[self.pos])
            self.pos += 1
        return '\n'.join(collected).strip()

    def _parse_commentary(self) -> Commentary: return Commentary(self._collect_block_text())
    def _parse_summary(self) -> Summary: return Summary(self._collect_block_text())
    def _parse_dedication(self) -> Dedication: return Dedication(self._collect_block_text())
    def _parse_infobox(self) -> Infobox: return Infobox(self._collect_block_text())

    def _parse_footnote(self, line: str) -> Footnote:
        match = re.search(r':::footnote\s+(\d+)', line)
        number = int(match.group(1)) if match else 0
        return Footnote(number, self._collect_block_text())

    def _parse_heading(self, line: str, level: int) -> Heading:
        self.pos += 1
        text = line.lstrip('#').strip()
        return Heading(level, text)

    def _parse_paragraph(self) -> Paragraph:
        collected: list[str] = []
        while self.pos < len(self.lines):
            current = self.lines[self.pos].strip()
            if not current or current.startswith(':::') or current.startswith('#') or current.startswith('---'):
                break
            collected.append(self.lines[self.pos])
            self.pos += 1
        return Paragraph('\n'.join(collected).strip())

class TypstGenerator:
    ESCAPE_CHARS: dict[str, str] = {'#': '\\#', '$': '\\$', '%': '\\%', '&': '\\&', '_': '\\_', '@': '\\@', '<': '\\<', '>': '\\>'}

    def __init__(self, chapter: Chapter) -> None:
        self.chapter = chapter
        self.footnote_map: dict[int, str] = {fn.number: fn.text for fn in chapter.footnotes}

    def generate(self) -> str:
        raw_content = self._generate_inner_content()
        title = self._escape_typst(self.chapter.title)
        hebrew = self.chapter.hebrew_title

        if self.chapter.layout_type == 'intro':
            return f'#layout_intro(title: "{title}", [\n{raw_content}\n])'
        return f'#layout_main(title: "{title}", hebrew-title: "{hebrew}", [\n{raw_content}\n])'

    def _generate_inner_content(self) -> str:
        parts: list[str] = []
        for item in self.chapter.content:
            if isinstance(item, Verse): parts.append(self._generate_verse(item))
            elif isinstance(item, GlossaryEntry): parts.append(self._generate_glossary_entry(item))
            elif isinstance(item, Commentary): parts.append(self._generate_commentary(item))
            elif isinstance(item, Summary): parts.append(self._generate_summary(item))
            elif isinstance(item, Dedication): parts.append(self._generate_dedication(item))
            elif isinstance(item, Infobox): parts.append(self._generate_infobox(item))
            elif isinstance(item, Heading): parts.append(self._generate_heading(item))
            elif isinstance(item, Paragraph): parts.append(self._generate_paragraph(item))
            elif isinstance(item, NewPage): parts.append("#colbreak()")
        return '\n\n'.join(parts)

    def _generate_verse(self, verse: Verse) -> str:
        hebrew = self._process_hebrew(verse.hebrew, verse.highlights)
        german = self._process_german(verse.translation, verse.highlights)
        source = f', source: "{self._escape_typst(verse.source)}"' if verse.source else ''
        return f'#verse(hebrew: [{hebrew}], german: [{german}]{source})'

    def _generate_glossary_entry(self, entry: GlossaryEntry) -> str:
        return f'#glossary-term("{self._escape_typst(entry.term)}", [\n{self._process_markdown(entry.definition)}\n])'

    def _generate_commentary(self, commentary: Commentary) -> str: return f'#commentary[\n{self._process_markdown(commentary.text)}\n]'
    def _generate_summary(self, summary: Summary) -> str: return f'#summary[\n{self._process_markdown(summary.text)}\n]'
    def _generate_dedication(self, dedication: Dedication) -> str: return f'#dedication[\n{self._process_markdown(dedication.text)}\n]'
    def _generate_infobox(self, infobox: Infobox) -> str: return f'#infobox[\n{self._process_markdown(infobox.text)}\n]'
    def _generate_heading(self, heading: Heading) -> str: return f'{"=" * heading.level} {self._escape_typst(heading.text)}'
    def _generate_paragraph(self, paragraph: Paragraph) -> str: return self._process_markdown(paragraph.text)

    def _process_hebrew(self, text: str, highlights: tuple[Highlight, ...]) -> str:
        for highlight in highlights:
            text = text.replace(highlight.hebrew, f'#hebhl[{highlight.hebrew}]')
        return '\n'.join([f'#heb[{line.strip()}]' if '#hebhl' not in line and line.strip() else line for line in text.split('\n')])

    def _process_german(self, text: str, highlights: tuple[Highlight, ...]) -> str:
        for highlight in highlights:
            text = text.replace(highlight.german, f'#dehl[{self._escape_typst(highlight.german)}]')
        return self._process_markdown(text)

    def _process_markdown(self, text: str) -> str:
        text = re.sub(r'\[(\d+)\]', lambda match: f'#footnote[{self._process_markdown(self.footnote_map.get(int(match.group(1)), ""))}]' if int(match.group(1)) in self.footnote_map else match.group(0), text)
        lines: list[str] = []
        for line in text.split('\n'):
            if line.startswith('* '): line = '- ' + line[2:]
            line = re.sub(r'\*\*([^*]+)\*\*', r'__BOLD__\1__BOLD__', line)
            line = re.sub(r'(?<![*\w])\*([^*\s][^*]*[^*\s]|\S)\*(?![*\w])', r'_\1_', line)
            line = line.replace('__BOLD__', '*')
            line = line.replace('@', '\\@')
            line = line.replace('\u201e', '"').replace('\u201c', '"').replace('\u201d', '"')
            line = line.replace('G-tt', 'G\u2011tt')
            lines.append(line)
        return '\n'.join(lines)

    def _escape_typst(self, text: str) -> str:
        for char, escaped in self.ESCAPE_CHARS.items():
            text = text.replace(char, escaped)
        return text

def build_book(chapter_files: list[Path], output_dir: Path, template_path: Path, version: str | None = None) -> None:
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        sys.exit(f"Error: Template file not found at {template_path}")

    vorwort_typ: list[str] = []
    chapters_typ: list[str] = []
    sorted_files = sorted(chapter_files)

    for chapter_file in sorted_files:
        print(f"Processing: {chapter_file}")

        fname = chapter_file.name.lower()
        if fname.startswith("00") or "vorwort" in fname or "intro" in fname:
            mode = "intro"
        else:
            mode = "main"

        with open(chapter_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        if version:
            md_content = md_content.replace('{{VERSION}}', version)

        parser = MarkdownParser(md_content, layout_type=mode)
        chapter = parser.parse()
        generator = TypstGenerator(chapter)
        generated = generator.generate()

        if mode == "intro":
            vorwort_typ.append(generated)
        else:
            chapters_typ.append(generated)

    book_typ = template.replace('{{VORWORT}}', '\n'.join(vorwort_typ))
    book_typ = book_typ.replace('{{CHAPTERS}}', '\n'.join(chapters_typ))

    output_file = output_dir / 'book.typ'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(book_typ)
    print(f"\nGenerated: {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='+', help='Input markdown files')
    parser.add_argument('-o', '--output', help='Output dir')
    parser.add_argument('--template', default=os.path.join(os.path.dirname(__file__), '..', 'templates', 'typst', 'book-a4.typ'), help='Template file')
    parser.add_argument('--version', default=None, help='Version string to inject (replaces {{VERSION}} in content)')
    args = parser.parse_args()

    if args.input:
        out = Path(args.output) if args.output else Path('.')
        out.mkdir(parents=True, exist_ok=True)
        build_book([Path(p) for p in args.input], out, Path(args.template), version=args.version)

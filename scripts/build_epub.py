#!/usr/bin/env python3
from __future__ import annotations

import re
import os
import subprocess
import argparse
from pathlib import Path

try:
    import yaml
except ImportError:
    import sys
    sys.exit("Error: PyYAML required. Install with: pip install pyyaml")

EPUB_CSS = os.path.join(os.path.dirname(__file__), '..', 'templates', 'epub.css')
METADATA = """---
title: "Bassi LeGani 5711"
author: "Der Lubawitscher Rebbe"
language: de
direction: ltr
---
"""

BLOCK_OPENERS: dict[str, tuple[str, str]] = {
    ':::commentary': ('commentary', '<div class="commentary">'),
    ':::summary': ('summary', '<div class="summary"><strong>Zusammenfassung</strong>'),
    ':::infobox': ('infobox', '<div class="infobox">'),
    ':::dedication': ('dedication', '<div class="dedication">'),
}

COLLECTED_BLOCKS = ('verse', 'glossary', 'footnote')
TEMP_MARKDOWN_FILE = "temp_book.md"


def strip_typst_syntax(text: str) -> str:
    text = re.sub(r'#hebhl\[(.*?)\]', r'<span class="hebrew">\1</span>', text)
    text = re.sub(r'#heb\[(.*?)\]', r'<span class="hebrew">\1</span>', text)
    text = text.replace("#strong[", "**").replace("#emph[", "*")
    return text


def convert_inline(line: str, chapter_index: int) -> str:
    line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
    line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)
    line = re.sub(
        r'\[(\d+)\]',
        lambda match: f'<a href="#fn-{chapter_index}-{match.group(1)}"><sup>{match.group(1)}</sup></a>',
        line,
    )
    return line + "\n"


def parse_verse_content(lines: list[str], chapter_index: int) -> str:
    full_text = " ".join(lines)
    hebrew = ""
    german = ""

    hebrew_match = re.search(r':hebrew:(.*?):/hebrew:', full_text, re.DOTALL)
    if hebrew_match:
        hebrew_part = hebrew_match.group(1).strip()
        hebrew_part = re.sub(r'\|(.*?)\|', r'<span class="hebrew">\1</span>', hebrew_part)
        hebrew = f'<span class="hebrew-line hebrew">{hebrew_part}</span>'

    translation_match = re.search(r':translation:(.*?):/translation:', full_text, re.DOTALL)
    if translation_match:
        german_part = convert_inline(translation_match.group(1).strip(), chapter_index).strip()
        german = f'<span class="german-line">{german_part}</span>'

    return f'<div class="verse">{hebrew}{german}</div>'


def parse_glossary_entry(lines: list[str], chapter_index: int) -> str:
    term = ""
    definition = ""
    for line in lines:
        if line.startswith(':term:'):
            term = line.replace(':term:', '').strip()
        elif line.startswith(':def:'):
            definition = line.replace(':def:', '').strip()

    definition_html = convert_inline(definition, chapter_index).strip()
    return f'<div class="glossary-entry"><strong>{term}</strong><br/>{definition_html}</div>'


def parse_footnote(lines: list[str], chapter_index: int) -> str:
    num = lines[0]
    content = " ".join(lines[1:]).strip()
    content_html = convert_inline(content, chapter_index).strip()
    return f'<div class="footnote" id="fn-{chapter_index}-{num}"><sup>{num}</sup> {content_html}</div>'


def convert_markdown_to_html(text: str, chapter_index: int) -> str:
    text = strip_typst_syntax(text)
    lines = text.split('\n')
    output: list[str] = []
    in_block: str | None = None
    block_content: list[str] = []

    for line in lines:
        line = line.strip()

        if line.startswith(':::verse'):
            in_block = 'verse'
            continue

        for prefix, (block_type, opening_tag) in BLOCK_OPENERS.items():
            if line.startswith(prefix):
                in_block = block_type
                output.append(opening_tag)
                break
        else:
            if line.startswith(':::glossary'):
                in_block = 'glossary'
                block_content = []
                continue
            elif line.startswith(':::footnote'):
                footnote_num = line.replace(':::footnote', '').strip()
                in_block = 'footnote'
                block_content = [footnote_num]
                continue
            elif line.startswith(':::newpage'):
                output.append('<div style="page-break-after: always;"></div>')
                continue
            elif line == ':::':
                output.append(close_block(in_block, block_content, chapter_index))
                in_block = None
                block_content = []
                continue

            if in_block:
                if in_block in COLLECTED_BLOCKS:
                    block_content.append(line)
                else:
                    output.append(convert_inline(line, chapter_index))
            else:
                output.append(convert_inline(line, chapter_index))
            continue
        continue

    return '\n'.join(output)


def close_block(block_type: str | None, block_content: list[str], chapter_index: int) -> str:
    if block_type == 'verse':
        return parse_verse_content(block_content, chapter_index)
    if block_type == 'glossary':
        return parse_glossary_entry(block_content, chapter_index)
    if block_type == 'footnote':
        return parse_footnote(block_content, chapter_index)
    if block_type:
        return '</div>'
    return ''


def extract_frontmatter(content: str) -> tuple[dict[str, str], str]:
    match = re.match(r'^---\s*\n([\s\S]+?)\n---\s*\n?', content)
    if not match:
        return {}, content
    try:
        metadata = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        metadata = {}
    body = content[match.end():]
    return metadata, body


def combine_chapters(input_files: list[Path]) -> str:
    combined = METADATA + "\n"
    for chapter_index, file_path in enumerate(sorted(input_files)):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        metadata, body = extract_frontmatter(content)
        title = metadata.get('title', '')
        if title:
            combined += f"## {title}\n\n"
        combined += convert_markdown_to_html(body, chapter_index) + "\n\n"
    return combined


def run_pandoc(source_path: str, output_file: Path) -> None:
    cmd = [
        "pandoc",
        source_path,
        "-o", str(output_file),
        "--css", EPUB_CSS,
        "--toc",
        "--toc-depth=2",
        "--metadata", "title=Bassi LeGani 5711"
    ]
    print(f"Generating EPUB: {output_file}...")
    subprocess.run(cmd, check=True)
    print("Success!")


def build_epub(input_files: list[Path], output_file: Path) -> None:
    combined_markdown = combine_chapters(input_files)

    temp_md = TEMP_MARKDOWN_FILE
    try:
        with open(temp_md, 'w', encoding='utf-8') as f:
            f.write(combined_markdown)
        run_pandoc(temp_md, output_file)
    finally:
        if os.path.exists(temp_md):
            os.remove(temp_md)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='+', help='Input markdown files')
    parser.add_argument('-o', '--output', default='book.epub', help='Output file')
    args = parser.parse_args()

    build_epub([Path(p) for p in args.input], Path(args.output))

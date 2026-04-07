"""Markdown/HTML document parser for Confluence pages."""

import logging
import re
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class DocChunk:
    chunk_type: str  # "section", "table", "code_block", "full_page"
    title: str
    content: str
    page_title: str = ""
    page_id: str = ""
    doc_type: str = ""  # "tech_review", "prd"
    heading_level: int = 0

    @property
    def metadata(self) -> dict:
        return {
            "chunk_type": self.chunk_type,
            "title": self.title,
            "page_title": self.page_title,
            "page_id": self.page_id,
            "doc_type": self.doc_type,
            "language": "markdown",
        }


def parse_confluence_page(
    content: str,
    page_title: str = "",
    page_id: str = "",
    doc_type: str = "tech_review",
    max_chunk_size: int = 4000,
) -> list[DocChunk]:
    """Split a Confluence page into semantic chunks by headings."""
    chunks: list[DocChunk] = []

    if not content.strip():
        return chunks

    if len(content) <= max_chunk_size:
        chunks.append(DocChunk(
            chunk_type="full_page",
            title=page_title,
            content=f"# {page_title}\n\n{content}",
            page_title=page_title,
            page_id=page_id,
            doc_type=doc_type,
        ))
        return chunks

    sections = _split_by_headings(content)

    for section in sections:
        section_content = section["content"].strip()
        if not section_content:
            continue

        heading = section.get("heading", page_title)
        full_content = f"# {page_title}\n## {heading}\n\n{section_content}"

        if len(full_content) > max_chunk_size:
            for i, sub in enumerate(_split_text(full_content, max_chunk_size)):
                chunks.append(DocChunk(
                    chunk_type="section",
                    title=f"{heading} (part {i + 1})",
                    content=sub,
                    page_title=page_title,
                    page_id=page_id,
                    doc_type=doc_type,
                    heading_level=section.get("level", 2),
                ))
        else:
            chunks.append(DocChunk(
                chunk_type="section",
                title=heading,
                content=full_content,
                page_title=page_title,
                page_id=page_id,
                doc_type=doc_type,
                heading_level=section.get("level", 2),
            ))

    if not chunks:
        chunks.append(DocChunk(
            chunk_type="full_page",
            title=page_title,
            content=content[:max_chunk_size],
            page_title=page_title,
            page_id=page_id,
            doc_type=doc_type,
        ))

    return chunks


def _split_by_headings(content: str) -> list[dict]:
    sections = []
    pattern = r"^(#{1,4})\s+(.+)$"
    lines = content.split("\n")
    current_heading = "Introduction"
    current_level = 1
    current_lines: list[str] = []

    for line in lines:
        m = re.match(pattern, line)
        if m:
            if current_lines:
                sections.append({
                    "heading": current_heading,
                    "level": current_level,
                    "content": "\n".join(current_lines),
                })
            current_heading = m.group(2).strip()
            current_level = len(m.group(1))
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        sections.append({
            "heading": current_heading,
            "level": current_level,
            "content": "\n".join(current_lines),
        })

    return sections


def _split_text(text: str, max_size: int) -> list[str]:
    parts = []
    while len(text) > max_size:
        split_at = text.rfind("\n\n", 0, max_size)
        if split_at == -1:
            split_at = text.rfind("\n", 0, max_size)
        if split_at == -1:
            split_at = max_size
        parts.append(text[:split_at])
        text = text[split_at:].lstrip()
    if text:
        parts.append(text)
    return parts

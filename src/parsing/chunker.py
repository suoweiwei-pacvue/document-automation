"""Unified chunker that coordinates all parsers and produces LangChain Documents."""

import logging
from typing import Optional

from langchain_core.documents import Document

from src.config import Settings
from src.parsing.java_parser import parse_java_file
from src.parsing.markdown_parser import parse_confluence_page
from src.parsing.vue_parser import parse_js_file, parse_vue_file
from src.sources.confluence_source import ConfluencePage
from src.sources.github_source import GitHubFile
from src.sources.local_source import SourceFile

logger = logging.getLogger(__name__)


def chunk_backend_files(files: list[SourceFile]) -> list[Document]:
    """Convert backend Java files into LangChain Documents."""
    docs: list[Document] = []
    for f in files:
        if f.file_type == "java":
            chunks = parse_java_file(f.content, f.relative_path)
            for chunk in chunks:
                docs.append(Document(
                    page_content=chunk.content,
                    metadata={
                        **chunk.metadata,
                        "source_type": "backend",
                        "module": f.module,
                        "relative_path": f.relative_path,
                    },
                ))
        elif f.file_type in ("resource", "pom"):
            if len(f.content) > 5000:
                content = f.content[:5000] + "\n# ... (truncated)"
            else:
                content = f.content
            docs.append(Document(
                page_content=content,
                metadata={
                    "chunk_type": f.file_type,
                    "name": f.relative_path.rsplit("/", 1)[-1],
                    "source_type": "backend",
                    "module": f.module,
                    "relative_path": f.relative_path,
                    "language": "yaml" if f.file_type == "resource" else "xml",
                },
            ))

    logger.info("Chunked %d backend files into %d documents", len(files), len(docs))
    return docs


def chunk_frontend_files(files: list[GitHubFile]) -> list[Document]:
    """Convert frontend Vue/JS files into LangChain Documents."""
    docs: list[Document] = []
    for f in files:
        if f.file_type == "vue":
            chunks = parse_vue_file(f.content, f.path)
        elif f.file_type in ("js", "ts", "jsx", "tsx"):
            chunks = parse_js_file(f.content, f.path)
        elif f.file_type == "json":
            docs.append(Document(
                page_content=f.content[:5000],
                metadata={
                    "chunk_type": "config",
                    "name": f.path,
                    "source_type": "frontend",
                    "file_path": f.path,
                    "language": "json",
                },
            ))
            continue
        else:
            continue

        for chunk in chunks:
            docs.append(Document(
                page_content=chunk.content,
                metadata={
                    **chunk.metadata,
                    "source_type": "frontend",
                },
            ))

    logger.info("Chunked %d frontend files into %d documents", len(files), len(docs))
    return docs


def chunk_confluence_pages(pages: list[ConfluencePage]) -> list[Document]:
    """Convert Confluence pages into LangChain Documents."""
    docs: list[Document] = []
    for page in pages:
        chunks = parse_confluence_page(
            page.content,
            page_title=page.title,
            page_id=page.page_id,
            doc_type=page.doc_type,
        )
        for chunk in chunks:
            docs.append(Document(
                page_content=chunk.content,
                metadata={
                    **chunk.metadata,
                    "source_type": "confluence",
                    "url": page.url,
                },
            ))

    logger.info("Chunked %d Confluence pages into %d documents", len(pages), len(docs))
    return docs

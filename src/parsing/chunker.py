"""Unified chunker that coordinates all parsers and produces LangChain Documents."""

import logging
from typing import Union

from langchain_core.documents import Document

from src.config import DOC_TYPE_TO_SOURCE, Settings
from src.parsing.java_parser import parse_java_file
from src.parsing.markdown_parser import parse_confluence_page
from src.parsing.vue_parser import parse_js_file, parse_vue_file
from src.sources.confluence_source import ConfluencePage
from src.sources.figma_source import FigmaNode
from src.sources.github_source import GitHubFile

logger = logging.getLogger(__name__)


def chunk_backend_files(files: list[GitHubFile]) -> list[Document]:
    """Convert backend Java/resource files into LangChain Documents."""
    docs: list[Document] = []
    for f in files:
        if f.file_type == "java":
            chunks = parse_java_file(f.content, f.path)
            for chunk in chunks:
                docs.append(Document(
                    page_content=chunk.content,
                    metadata={
                        **chunk.metadata,
                        "source_type": "backend",
                        "module": f.module,
                        "relative_path": f.path,
                    },
                ))
        elif f.file_type in ("resource", "pom", "sql"):
            if len(f.content) > 5000:
                content = f.content[:5000] + "\n# ... (truncated)"
            else:
                content = f.content
            docs.append(Document(
                page_content=content,
                metadata={
                    "chunk_type": f.file_type,
                    "name": f.path.rsplit("/", 1)[-1],
                    "source_type": "backend",
                    "module": f.module,
                    "relative_path": f.path,
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
        source_type = DOC_TYPE_TO_SOURCE.get(page.doc_type, "confluence-tech")
        for chunk in chunks:
            docs.append(Document(
                page_content=chunk.content,
                metadata={
                    **chunk.metadata,
                    "source_type": source_type,
                    "url": page.url,
                },
            ))

    logger.info("Chunked %d Confluence pages into %d documents", len(pages), len(docs))
    return docs


def chunk_figma_nodes(nodes: list[FigmaNode]) -> list[Document]:
    """Convert Figma design nodes into LangChain Documents."""
    docs: list[Document] = []
    for node in nodes:
        if not node.content.strip():
            continue

        content = node.content
        if len(content) > 5000:
            content = content[:5000] + "\n... (truncated)"

        docs.append(Document(
            page_content=content,
            metadata={
                "chunk_type": node.node_type.lower(),
                "name": node.name,
                "source_type": "figma",
                "file_key": node.file_key,
                "file_name": node.file_name,
                "page_name": node.page_name,
                "node_id": node.node_id,
            },
        ))

    logger.info("Chunked %d Figma nodes into %d documents", len(nodes), len(docs))
    return docs

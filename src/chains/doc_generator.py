"""Document generation chain: produces full module documentation."""

import json
import logging
from pathlib import Path

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

from src.config import MODULE_DEFINITIONS, Settings
from src.rag.retriever import MultiSourceRetriever

logger = logging.getLogger(__name__)

PROMPT_PATH = Path(__file__).parent.parent.parent / "prompts" / "generate_doc.txt"


def generate_module_doc(
    module_key: str,
    skeleton: dict,
    retriever: MultiSourceRetriever,
    settings: Settings,
) -> str:
    """Generate complete documentation for a module."""
    module_def = MODULE_DEFINITIONS[module_key]
    prompt_template = PROMPT_PATH.read_text(encoding="utf-8")

    keywords = module_def.get("keywords", [])
    backend_modules = module_def.get("backend_modules", [])

    code_docs = retriever.retrieve(
        query=" ".join(keywords[:5]),
        k=15,
        source_types=["backend", "frontend"],
    )

    prd_docs = retriever.retrieve(
        query=f"{module_def['title']} {' '.join(keywords[:3])}",
        k=8,
        source_types=["confluence"],
        doc_type_filter="prd",
    )

    tech_docs = retriever.retrieve(
        query=f"{module_def['title']} {' '.join(keywords[:3])}",
        k=8,
        source_types=["confluence"],
        doc_type_filter="tech_review",
    )

    figma_docs = retriever.retrieve(
        query=f"{module_def['title']} {' '.join(keywords[:3])}",
        k=6,
        source_types=["figma"],
    )

    code_context = _format_docs(code_docs, max_chars=15000)
    prd_context = _format_docs(prd_docs, max_chars=8000)
    tech_context = _format_docs(tech_docs, max_chars=8000)
    figma_context = _format_docs(figma_docs, max_chars=5000)

    skeleton_str = json.dumps(skeleton, ensure_ascii=False, indent=2, default=str)
    if len(skeleton_str) > 5000:
        skeleton_str = skeleton_str[:5000] + "\n..."

    prompt = prompt_template.format(
        module_title=module_def["title"],
        module_description=module_def["description"],
        module_skeleton=skeleton_str,
        code_context=code_context,
        prd_context=prd_context,
        tech_context=tech_context,
        figma_context=figma_context,
    )

    llm = ChatOpenAI(
        **settings.get_llm_kwargs(),
        temperature=0.1,
        max_tokens=8000,
    )

    logger.info("Generating documentation for module: %s", module_key)
    response = llm.invoke(prompt)
    return response.content


def _format_docs(docs: list[Document], max_chars: int = 10000) -> str:
    if not docs:
        return "(无相关文档)"

    parts: list[str] = []
    total = 0
    for doc in docs:
        source = doc.metadata.get("source_type", "")
        name = doc.metadata.get("name", doc.metadata.get("title", ""))
        header = f"\n### [{source}] {name}\n"
        content = doc.page_content

        if total + len(header) + len(content) > max_chars:
            remaining = max_chars - total - len(header)
            if remaining > 200:
                content = content[:remaining] + "\n... (truncated)"
            else:
                break

        parts.append(header + content)
        total += len(header) + len(content)

    return "\n".join(parts)

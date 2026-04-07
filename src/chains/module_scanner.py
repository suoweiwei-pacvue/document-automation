"""Module scanner chain: analyzes code and produces a module skeleton."""

import json
import logging
from pathlib import Path

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

from src.config import MODULE_DEFINITIONS, Settings
from src.rag.retriever import MultiSourceRetriever

logger = logging.getLogger(__name__)

PROMPT_PATH = Path(__file__).parent.parent.parent / "prompts" / "scan_module.txt"


def scan_module(
    module_key: str,
    retriever: MultiSourceRetriever,
    settings: Settings,
) -> dict:
    """Scan a module and produce a structured skeleton."""
    module_def = MODULE_DEFINITIONS[module_key]
    prompt_template = PROMPT_PATH.read_text(encoding="utf-8")

    docs = retriever.retrieve_for_module(
        module_id=module_key,
        keywords=module_def.get("keywords", []),
        backend_modules=module_def.get("backend_modules"),
        k_per_query=8,
        max_total=40,
    )

    context = _build_context(docs, max_tokens=12000)

    prompt = prompt_template.format(
        module_title=module_def["title"],
        module_description=module_def["description"],
        context=context,
    )

    llm = ChatOpenAI(
        **settings.get_llm_kwargs(),
        temperature=0,
    )

    response = llm.invoke(prompt)
    content = response.content

    try:
        json_start = content.find("{")
        json_end = content.rfind("}") + 1
        if json_start != -1 and json_end > json_start:
            skeleton = json.loads(content[json_start:json_end])
        else:
            skeleton = {"raw_response": content}
    except json.JSONDecodeError:
        logger.warning("Failed to parse scanner response as JSON for %s", module_key)
        skeleton = {"raw_response": content}

    skeleton["module_key"] = module_key
    skeleton["module_def"] = module_def
    logger.info("Scanned module %s: found %d docs", module_key, len(docs))
    return skeleton


def _build_context(docs: list[Document], max_tokens: int = 12000) -> str:
    """Build a context string from retrieved documents, respecting token limits."""
    parts: list[str] = []
    total_len = 0
    char_limit = max_tokens * 3  # rough chars-to-tokens ratio

    for doc in docs:
        source = doc.metadata.get("source_type", "unknown")
        name = doc.metadata.get("name", doc.metadata.get("title", ""))
        path = doc.metadata.get("relative_path", doc.metadata.get("file_path", ""))

        header = f"\n--- [{source}] {name} ({path}) ---\n"
        content = doc.page_content

        if total_len + len(header) + len(content) > char_limit:
            remaining = char_limit - total_len - len(header)
            if remaining > 200:
                content = content[:remaining] + "\n... (truncated)"
            else:
                break

        parts.append(header + content)
        total_len += len(header) + len(content)

    return "\n".join(parts)

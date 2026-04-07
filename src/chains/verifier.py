"""Document verification chain: cross-checks generated docs against code."""

import json
import logging
from pathlib import Path

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

from src.config import Settings
from src.rag.retriever import MultiSourceRetriever

logger = logging.getLogger(__name__)

PROMPT_PATH = Path(__file__).parent.parent.parent / "prompts" / "verify_doc.txt"


def verify_document(
    document: str,
    module_key: str,
    retriever: MultiSourceRetriever,
    settings: Settings,
) -> dict:
    """Verify a generated document against the source code."""
    from src.config import MODULE_DEFINITIONS
    module_def = MODULE_DEFINITIONS[module_key]

    code_docs = retriever.retrieve(
        query=" ".join(module_def.get("keywords", [])[:5]),
        k=10,
        source_types=["backend"],
    )

    code_context = "\n\n".join(
        f"--- {d.metadata.get('name', '')} ---\n{d.page_content[:2000]}"
        for d in code_docs[:8]
    )

    prompt_template = PROMPT_PATH.read_text(encoding="utf-8")
    prompt = prompt_template.format(
        document=document[:8000],
        code_context=code_context[:10000],
    )

    llm = ChatOpenAI(
        **settings.get_llm_kwargs(),
        temperature=0,
        max_tokens=3000,
    )

    response = llm.invoke(prompt)
    content = response.content

    try:
        json_start = content.find("{")
        json_end = content.rfind("}") + 1
        if json_start != -1 and json_end > json_start:
            result = json.loads(content[json_start:json_end])
        else:
            result = {"raw_response": content, "accuracy_score": -1}
    except json.JSONDecodeError:
        result = {"raw_response": content, "accuracy_score": -1}

    logger.info(
        "Verified module %s: accuracy_score=%s",
        module_key, result.get("accuracy_score", "N/A"),
    )
    return result


def apply_corrections(document: str, verification: dict) -> str:
    """Apply corrections from verification to the document."""
    corrections = verification.get("corrections", "")
    if corrections and isinstance(corrections, str) and len(corrections) > 100:
        document += f"\n\n---\n\n> **自动审核备注**: 准确性评分 {verification.get('accuracy_score', 'N/A')}/100\n"

        issues = verification.get("issues", [])
        if issues:
            document += ">\n> **待修正项**:\n"
            for issue in issues[:5]:
                severity = issue.get("severity", "info")
                desc = issue.get("description", "")
                document += f"> - [{severity}] {desc}\n"

    return document

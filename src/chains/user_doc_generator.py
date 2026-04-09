"""User-facing document generator: rewrites technical docs into end-user guides."""

import logging
from pathlib import Path

from langchain_openai import ChatOpenAI

from src.config import MODULE_DEFINITIONS, USER_DOC_DEFINITIONS, Settings

logger = logging.getLogger(__name__)

PROMPT_PATH = Path(__file__).parent.parent.parent / "prompts" / "generate_user_doc.txt"

MAX_TECH_CHARS_PER_MODULE = 15000
MAX_TECH_CHARS_TOTAL = 60000


def generate_user_doc(user_doc_key: str, settings: Settings) -> str:
    """Read generated tech docs for source_modules and rewrite as a user guide."""
    user_def = USER_DOC_DEFINITIONS[user_doc_key]
    prompt_template = PROMPT_PATH.read_text(encoding="utf-8")

    tech_content = _collect_tech_content(user_def["source_modules"], settings)
    if not tech_content.strip():
        raise FileNotFoundError(
            f"No tech docs found for user-doc '{user_doc_key}'. "
            f"Run 'generate' first to create tech docs."
        )

    prompt = prompt_template.format(
        chapter_title=user_def["title"],
        chapter_description=user_def["description"],
        tech_content=tech_content,
    )

    llm = ChatOpenAI(
        **settings.get_llm_kwargs(),
        temperature=0.2,
        max_tokens=12000,
    )

    logger.info("Generating user doc for chapter: %s", user_doc_key)
    response = llm.invoke(prompt)
    return response.content


def _collect_tech_content(source_modules: list[str], settings: Settings) -> str:
    """Read and concatenate tech doc files for the given module keys."""
    parts: list[str] = []
    total = 0

    for mod_key in source_modules:
        if mod_key not in MODULE_DEFINITIONS:
            logger.warning("Unknown source module '%s', skipping", mod_key)
            continue

        mod_def = MODULE_DEFINITIONS[mod_key]
        tech_file = settings.output_path / f"{mod_def['id']}.md"

        if not tech_file.exists():
            logger.warning("Tech doc not found: %s", tech_file)
            continue

        content = tech_file.read_text(encoding="utf-8")
        if len(content) > MAX_TECH_CHARS_PER_MODULE:
            content = content[:MAX_TECH_CHARS_PER_MODULE] + "\n\n... (truncated)"

        header = f"\n{'='*60}\n技术文档参考: {mod_def['title']}\n{'='*60}\n\n"

        if total + len(header) + len(content) > MAX_TECH_CHARS_TOTAL:
            remaining = MAX_TECH_CHARS_TOTAL - total - len(header)
            if remaining > 500:
                content = content[:remaining] + "\n\n... (truncated)"
            else:
                break

        parts.append(header + content)
        total += len(header) + len(content)

    return "\n".join(parts)

"""Mermaid diagram generator chain."""

import logging
from pathlib import Path

from langchain_openai import ChatOpenAI

from src.config import Settings

logger = logging.getLogger(__name__)

PROMPT_PATH = Path(__file__).parent.parent.parent / "prompts" / "generate_diagram.txt"


def generate_diagrams(
    module_info: str,
    settings: Settings,
) -> str:
    """Generate Mermaid diagrams for a module."""
    prompt_template = PROMPT_PATH.read_text(encoding="utf-8")
    prompt = prompt_template.format(module_info=module_info[:6000])

    llm = ChatOpenAI(
        **settings.get_llm_kwargs(),
        temperature=0,
        max_tokens=2000,
    )

    response = llm.invoke(prompt)
    return response.content


def inject_diagrams(document: str, diagrams: str) -> str:
    """Inject generated diagrams into the document at the flow chart section."""
    if "## 4. 核心业务流程" in document and "```mermaid" not in document:
        insert_point = document.find("## 4. 核心业务流程")
        section_end = document.find("\n## 5.", insert_point)
        if section_end == -1:
            section_end = len(document)

        section = document[insert_point:section_end]
        if "```mermaid" not in section and diagrams.strip():
            new_section = section.rstrip() + "\n\n" + diagrams + "\n\n"
            document = document[:insert_point] + new_section + document[section_end:]

    return document

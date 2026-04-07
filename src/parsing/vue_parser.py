"""Vue Single File Component parser for semantic chunking."""

import logging
import re
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class VueChunk:
    chunk_type: str  # "component", "script", "template", "style", "method", "computed", "store_action"
    name: str
    content: str
    file_path: str = ""
    section: str = ""  # "template", "script", "style"

    @property
    def metadata(self) -> dict:
        return {
            "chunk_type": self.chunk_type,
            "name": self.name,
            "file_path": self.file_path,
            "section": self.section,
            "language": "vue",
        }


def parse_vue_file(content: str, file_path: str = "") -> list[VueChunk]:
    """Parse a Vue SFC into semantic chunks."""
    chunks: list[VueChunk] = []
    component_name = _extract_component_name(file_path)

    template = _extract_section(content, "template")
    script = _extract_section(content, "script")
    style = _extract_section(content, "style")

    if template:
        if len(template) > 5000:
            template = template[:5000] + "\n<!-- ... (truncated) -->"
        chunks.append(VueChunk(
            chunk_type="template",
            name=component_name,
            content=template,
            file_path=file_path,
            section="template",
        ))

    if script:
        chunks.append(VueChunk(
            chunk_type="script",
            name=component_name,
            content=script[:8000] if len(script) > 8000 else script,
            file_path=file_path,
            section="script",
        ))

        for method in _extract_js_functions(script):
            chunks.append(VueChunk(
                chunk_type="method",
                name=f"{component_name}.{method['name']}",
                content=method["content"],
                file_path=file_path,
                section="script",
            ))

    return chunks


def parse_js_file(content: str, file_path: str = "") -> list[VueChunk]:
    """Parse a plain JS/TS file (e.g., store.js, router.js)."""
    chunks: list[VueChunk] = []
    file_name = file_path.rsplit("/", 1)[-1] if file_path else "unknown"

    if len(content) > 10000:
        chunks.append(VueChunk(
            chunk_type="file_overview",
            name=file_name,
            content=content[:10000] + "\n// ... (truncated)",
            file_path=file_path,
            section="script",
        ))
    else:
        chunks.append(VueChunk(
            chunk_type="file",
            name=file_name,
            content=content,
            file_path=file_path,
            section="script",
        ))

    for fn in _extract_js_functions(content):
        chunks.append(VueChunk(
            chunk_type="method",
            name=f"{file_name}.{fn['name']}",
            content=fn["content"],
            file_path=file_path,
            section="script",
        ))

    for exp in _extract_exports(content):
        chunks.append(VueChunk(
            chunk_type="export",
            name=f"{file_name}.{exp['name']}",
            content=exp["content"],
            file_path=file_path,
            section="script",
        ))

    return chunks


def _extract_component_name(file_path: str) -> str:
    if not file_path:
        return "Unknown"
    name = file_path.rsplit("/", 1)[-1]
    return name.replace(".vue", "").replace(".js", "").replace(".ts", "")


def _extract_section(content: str, tag: str) -> str:
    pattern = rf"<{tag}[^>]*>(.*?)</{tag}>"
    m = re.search(pattern, content, re.DOTALL)
    return m.group(1).strip() if m else ""


def _extract_js_functions(script: str) -> list[dict]:
    """Extract named functions and methods from JS/TS code."""
    functions = []
    patterns = [
        r"(?:async\s+)?(\w+)\s*\([^)]*\)\s*\{",
        r"(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>)\s*",
        r"(\w+)\s*:\s*(?:async\s+)?function\s*\(",
    ]

    for pattern in patterns:
        for m in re.finditer(pattern, script):
            name = m.group(1)
            if name in ("if", "for", "while", "switch", "catch", "return", "function", "else"):
                continue
            start = m.start()
            brace = script.find("{", m.end() - 1)
            if brace == -1:
                continue
            end = _find_matching_brace_js(script, brace)
            if end == -1:
                end = min(brace + 2000, len(script))

            fn_content = script[start:end + 1].strip()
            if len(fn_content) > 3000:
                fn_content = fn_content[:3000] + "\n// ... (truncated)"

            functions.append({"name": name, "content": fn_content})

    return functions


def _extract_exports(content: str) -> list[dict]:
    exports = []
    for m in re.finditer(r"export\s+(?:default\s+)?(?:const|let|var|function|class)\s+(\w+)", content):
        name = m.group(1)
        start = m.start()
        end = min(start + 500, len(content))
        exports.append({"name": name, "content": content[start:end].strip()})
    return exports


def _find_matching_brace_js(content: str, open_pos: int) -> int:
    depth = 0
    in_string = None
    in_template = False
    i = open_pos

    while i < len(content):
        c = content[i]
        prev = content[i - 1] if i > 0 else ""

        if in_string:
            if c == in_string and prev != "\\":
                in_string = None
        elif in_template:
            if c == "`" and prev != "\\":
                in_template = False
        else:
            if c in ('"', "'"):
                in_string = c
            elif c == "`":
                in_template = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return i
        i += 1

    return -1

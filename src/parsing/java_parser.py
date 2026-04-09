"""Java source code parser using tree-sitter for semantic chunking."""

import logging
import re
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class JavaChunk:
    # 核心就是解析出如下的java的结构体对象
    chunk_type: str  # "class", "method", "interface", "enum", "field_group"
    name: str
    qualified_name: str
    content: str
    package: str = ""
    class_name: str = ""
    annotations: list[str] = field(default_factory=list)
    modifiers: list[str] = field(default_factory=list)
    file_path: str = ""
    start_line: int = 0
    end_line: int = 0

    @property
    def metadata(self) -> dict:
        return {
            "chunk_type": self.chunk_type,
            "name": self.name,
            "qualified_name": self.qualified_name,
            "package": self.package,
            "class_name": self.class_name,
            "annotations": ",".join(self.annotations),
            "file_path": self.file_path,
            "language": "java",
        }


def parse_java_file(content: str, file_path: str = "") -> list[JavaChunk]:
    """Parse a Java file into semantic chunks using regex-based parsing.

    Falls back from tree-sitter to regex for broader compatibility.
    """
    chunks: list[JavaChunk] = []

    package = _extract_package(content)
    imports = _extract_imports(content)
    class_info = _extract_class_info(content)

    if not class_info:
        if content.strip():
            chunks.append(JavaChunk(
                chunk_type="file",
                name=file_path.rsplit("/", 1)[-1] if file_path else "unknown",
                qualified_name=f"{package}.{file_path}" if package else file_path,
                content=content,
                package=package,
                file_path=file_path,
            ))
        return chunks

    class_name = class_info["name"]
    class_annotations = class_info.get("annotations", [])
    qualified = f"{package}.{class_name}" if package else class_name

    header = f"package {package};\n\n" if package else ""
    header += "\n".join(imports[:10]) + "\n\n" if imports else ""
    header += "\n".join(f"@{a}" for a in class_annotations) + "\n" if class_annotations else ""
    header += f"{class_info.get('declaration', '')}"

    chunks.append(JavaChunk(
        chunk_type=class_info.get("type", "class"),
        name=class_name,
        qualified_name=qualified,
        content=header,
        package=package,
        class_name=class_name,
        annotations=class_annotations,
        file_path=file_path,
    ))

    methods = _extract_methods(content)
    for method in methods:
        method_qualified = f"{qualified}.{method['name']}"
        chunks.append(JavaChunk(
            chunk_type="method",
            name=method["name"],
            qualified_name=method_qualified,
            content=method["content"],
            package=package,
            class_name=class_name,
            annotations=method.get("annotations", []),
            file_path=file_path,
            start_line=method.get("start_line", 0),
        ))

    return chunks


def _extract_package(content: str) -> str:
    m = re.search(r"^package\s+([\w.]+)\s*;", content, re.MULTILINE)
    return m.group(1) if m else ""


def _extract_imports(content: str) -> list[str]:
    return re.findall(r"^(import\s+[\w.*]+\s*;)", content, re.MULTILINE)


def _extract_class_info(content: str) -> dict:
    annotations = []
    for m in re.finditer(r"^(@\w+(?:\([^)]*\))?)\s*$", content, re.MULTILINE):
        annotations.append(m.group(1).lstrip("@").split("(")[0])

    pattern = (
        r"(?:public|protected|private)?\s*(?:abstract\s+)?(?:static\s+)?"
        r"(?:final\s+)?(class|interface|enum)\s+(\w+)"
        r"(?:\s+extends\s+[\w<>,\s]+)?(?:\s+implements\s+[\w<>,\s]+)?\s*\{"
    )
    m = re.search(pattern, content)
    if not m:
        return {}

    return {
        "type": m.group(1),
        "name": m.group(2),
        "declaration": m.group(0).rstrip("{").strip(),
        "annotations": annotations,
    }


def _extract_methods(content: str) -> list[dict]:
    """Extract method signatures and bodies from Java source."""
    methods = []
    pattern = (
        r"(?:(?:@\w+(?:\([^)]*\))?)\s*\n\s*)*"
        r"(?:(?:public|protected|private)\s+)?"
        r"(?:(?:static|final|abstract|synchronized|native)\s+)*"
        r"(?:<[\w\s,?]+>\s+)?"
        r"([\w<>\[\],\s?]+)\s+"
        r"(\w+)\s*\("
    )

    for m in re.finditer(pattern, content):
        method_name = m.group(2)
        if method_name in ("if", "for", "while", "switch", "catch", "return", "class", "new"):
            continue

        start = m.start()
        line_start = content[:start].count("\n") + 1

        ann_start = start
        preceding = content[max(0, start - 500):start]
        ann_matches = list(re.finditer(r"@\w+(?:\([^)]*\))?\s*\n", preceding))
        if ann_matches:
            first_ann = ann_matches[0]
            ann_start = max(0, start - 500) + first_ann.start()

        brace_pos = content.find("{", m.end())
        if brace_pos == -1:
            semi_pos = content.find(";", m.end())
            if semi_pos != -1:
                method_content = content[ann_start:semi_pos + 1].strip()
                annotations = re.findall(r"@(\w+)", content[ann_start:start])
                methods.append({
                    "name": method_name,
                    "content": method_content,
                    "annotations": annotations,
                    "start_line": line_start,
                })
            continue

        end_pos = _find_matching_brace(content, brace_pos)
        if end_pos == -1:
            end_pos = min(brace_pos + 2000, len(content))

        method_content = content[ann_start:end_pos + 1].strip()
        if len(method_content) > 3000:
            method_content = method_content[:3000] + "\n    // ... (truncated)"

        annotations = re.findall(r"@(\w+)", content[ann_start:start])
        methods.append({
            "name": method_name,
            "content": method_content,
            "annotations": annotations,
            "start_line": line_start,
        })

    return methods


def _find_matching_brace(content: str, open_pos: int) -> int:
    depth = 0
    in_string = False
    in_char = False
    in_line_comment = False
    in_block_comment = False
    i = open_pos

    while i < len(content):
        c = content[i]
        prev = content[i - 1] if i > 0 else ""

        if in_line_comment:
            if c == "\n":
                in_line_comment = False
        elif in_block_comment:
            if c == "/" and prev == "*":
                in_block_comment = False
        elif in_string:
            if c == '"' and prev != "\\":
                in_string = False
        elif in_char:
            if c == "'" and prev != "\\":
                in_char = False
        else:
            if c == "/" and i + 1 < len(content):
                next_c = content[i + 1]
                if next_c == "/":
                    in_line_comment = True
                elif next_c == "*":
                    in_block_comment = True
            elif c == '"':
                in_string = True
            elif c == "'":
                in_char = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return i
        i += 1

    return -1

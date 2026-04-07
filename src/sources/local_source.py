"""Local filesystem source for reading backend Java code."""

import logging
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

logger = logging.getLogger(__name__)

JAVA_EXTENSIONS = {".java"}
RESOURCE_EXTENSIONS = {".yml", ".yaml", ".xml", ".properties"}
SKIP_DIRS = {".git", ".idea", "target", "build", "node_modules", ".gradle"}


class SourceFile(BaseModel):
    path: str
    relative_path: str
    content: str
    module: str
    file_type: str  # "java", "resource", "sql", "pom"
    source_type: str = "backend"


def collect_files(
    root: Path,
    modules: Optional[list[str]] = None,
) -> list[SourceFile]:
    """Walk the local backend repo and collect source files."""
    files: list[SourceFile] = []
    if not root.exists():
        logger.error("Backend path does not exist: %s", root)
        return files

    for item in sorted(root.iterdir()):
        if item.name in SKIP_DIRS or not item.is_dir():
            if item.name == "pom.xml":
                files.append(_read_file(item, root, "root", "pom"))
            continue

        module_name = item.name
        if modules and module_name not in modules and "*" not in modules:
            continue

        module_files = _walk_module(item, root, module_name)
        files.extend(module_files)
        logger.info("Collected %d files from module %s", len(module_files), module_name)

    logger.info("Total collected %d backend files", len(files))
    return files


def _walk_module(module_dir: Path, root: Path, module_name: str) -> list[SourceFile]:
    files: list[SourceFile] = []
    for path in sorted(module_dir.rglob("*")):
        if not path.is_file():
            continue
        if any(skip in path.parts for skip in SKIP_DIRS):
            continue

        suffix = path.suffix.lower()
        if suffix in JAVA_EXTENSIONS:
            files.append(_read_file(path, root, module_name, "java"))
        elif suffix in RESOURCE_EXTENSIONS:
            files.append(_read_file(path, root, module_name, "resource"))
        elif suffix == ".sql":
            files.append(_read_file(path, root, module_name, "sql"))
        elif path.name == "pom.xml":
            files.append(_read_file(path, root, module_name, "pom"))
    return files


def _read_file(
    path: Path, root: Path, module: str, file_type: str
) -> SourceFile:
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        logger.warning("Failed to read %s: %s", path, e)
        content = ""

    return SourceFile(
        path=str(path),
        relative_path=str(path.relative_to(root)),
        content=content,
        module=module,
        file_type=file_type,
        source_type="backend",
    )

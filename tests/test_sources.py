"""Tests for data sources."""

from src.sources.figma_source import FigmaNode, _collect_texts
from src.sources.github_source import (
    BACKEND_EXTENSIONS,
    FRONTEND_EXTENSIONS,
    GitHubFile,
    _classify_file_type,
    _extract_module,
)


def test_extract_module_from_path():
    assert _extract_module("custom-dashboard-api/src/main/java/Foo.java") == "custom-dashboard-api"
    assert _extract_module("custom-dashboard-base/pom.xml") == "custom-dashboard-base"
    assert _extract_module("pom.xml") == "root"


def test_classify_file_type():
    assert _classify_file_type(".java") == "java"
    assert _classify_file_type(".yml") == "resource"
    assert _classify_file_type(".yaml") == "resource"
    assert _classify_file_type(".properties") == "resource"
    assert _classify_file_type(".sql") == "sql"
    assert _classify_file_type(".vue") == "vue"


def test_github_file_model():
    f = GitHubFile(
        path="custom-dashboard-api/src/Main.java",
        content="public class Main {}",
        file_type="java",
        source_type="backend",
        module="custom-dashboard-api",
    )
    assert f.source_type == "backend"
    assert f.module == "custom-dashboard-api"


def test_extensions_sets():
    assert ".java" in BACKEND_EXTENSIONS
    assert ".xml" in BACKEND_EXTENSIONS
    assert ".vue" in FRONTEND_EXTENSIONS
    assert ".java" not in FRONTEND_EXTENSIONS


# --- Figma source tests ---


def test_figma_node_model():
    node = FigmaNode(
        file_key="abc123",
        file_name="My Design",
        node_id="6580:843",
        name="Sprint6/Header",
        node_type="FRAME",
        page_name="26Q1 Sprint6",
        content="[FRAME] Sprint6/Header\nChildren (3):\n  - Logo\n  - Nav\n  - Search",
    )
    assert node.source_type == "figma"
    assert node.file_key == "abc123"
    assert node.page_name == "26Q1 Sprint6"
    assert node.node_type == "FRAME"


def test_figma_node_defaults():
    node = FigmaNode(
        file_key="key1",
        node_id="0:1",
        name="Page",
        node_type="CANVAS",
        content="Some content",
    )
    assert node.file_name == ""
    assert node.page_name == ""
    assert node.source_type == "figma"


def test_collect_texts_basic():
    tree = {
        "type": "FRAME",
        "name": "Root",
        "children": [
            {"type": "TEXT", "name": "Label", "characters": "Hello World"},
            {
                "type": "FRAME",
                "name": "Inner",
                "children": [
                    {"type": "TEXT", "name": "Sub", "characters": "Nested Text"},
                ],
            },
        ],
    }
    texts = _collect_texts(tree, max_depth=3)
    assert "Hello World" in texts
    assert "Nested Text" in texts


def test_collect_texts_max_depth():
    tree = {
        "type": "FRAME",
        "children": [
            {
                "type": "FRAME",
                "children": [
                    {"type": "TEXT", "characters": "Deep Text"},
                ],
            },
        ],
    }
    shallow = _collect_texts(tree, max_depth=1)
    assert "Deep Text" not in shallow

    deep = _collect_texts(tree, max_depth=3)
    assert "Deep Text" in deep


def test_collect_texts_skips_short():
    tree = {
        "type": "FRAME",
        "children": [
            {"type": "TEXT", "characters": "X"},
            {"type": "TEXT", "characters": "OK text here"},
        ],
    }
    texts = _collect_texts(tree, max_depth=2)
    assert "X" not in texts
    assert "OK text here" in texts
